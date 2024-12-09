import numpy as np
from copy import deepcopy
from numpy.polynomial.polynomial import Polynomial
from skimage import exposure
from scipy.signal import savgol_filter
from scipy.ndimage import affine_transform
from plotly import graph_objects as go

# Local imports
from qimchi.logger import logger
from qimchi.state import (
    DEFAULT_SAVGOL_OPTS,
    DEFAULT_SMA_WINDOW,
    DEFAULT_NORM_OPTS,
    DEFAULT_GC_OPTS,
    DEFAULT_LC_OPTS,
    DEFAULT_SC_OPTS,
    DEFAULT_POLYFIT_OPTS,
    DEFAULT_RI_OPTS,
    DEFAULT_ROTA_OPTS,
)


def _safe_init(options: dict, key: str, default: dict) -> dict:
    """
    Helper function to safely initialize the options.

    Args:
        options (dict): Options dict.
        key (str): Key to get the value from the options dict.
        default (dict): Default options dict.

    Returns:
        dict: Safe options dict.

    """
    return options.get(key, default) if options else default


def _pprint_poly(poly: Polynomial, x_var: str):
    """
    Helper function to pretty-print a polynomial equation in LaTeX.

    Args:
        poly (Polynomial): Polynomial object.
        x_var (str): Variable name for the polynomial.

    Returns:
        str: Pretty-printed polynomial equation in LaTeX

    """
    # TODOLATER: Add support for auto-wrapped text
    for i, coef in enumerate(poly.coef):
        if i == 0:
            poly_str = f"{coef:.2f}"
        else:
            sign = "+" if coef >= 0 else "-"
            poly_str += f" {sign} {abs(coef):.2f}({x_var})^{i}"

    logger.debug(f"Pretty-printed polynomial equation: {poly_str}")
    return rf"${poly_str}$"


def _safe_init(options: dict, key: str, default: dict) -> dict:
    """
    Helper function to safely initialize the options.

    Args:
        options (dict): Options dict.
        key (str): Key to get the value from the options dict.
        default (dict): Default options dict.

    Returns:
        dict: Safe options dict.

    """
    return options.get(key, default) if options else default


def _pprint_poly(poly: Polynomial, x_var: str):
    """
    Helper function to pretty-print a polynomial equation in LaTeX.

    Args:
        poly (Polynomial): Polynomial object.
        x_var (str): Variable name for the polynomial.

    Returns:
        str: Pretty-printed polynomial equation in LaTeX

    """
    # TODOLATER: Add support for auto-wrapped text
    for i, coef in enumerate(poly.coef):
        if i == 0:
            poly_str = f"{coef:.2f}"
        else:
            sign = "+" if coef >= 0 else "-"
            poly_str += f" {sign} {abs(coef):.2f}({x_var})^{i}"

    logger.debug(f"Pretty-printed polynomial equation: {poly_str}")
    return rf"${poly_str}$"


class Filter:
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Filter Base Class

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure
            options (dict, optional): Options for the filter. Default is None.

        """
        self._name = self.__class__.__name__

        self.figure = figure
        self.new_fig = deepcopy(figure)
        self.data = figure["data"]
        self.num_axes = num_axes
        self.options = options

        dat = figure["data"][0]
        self.x_axis = np.array(dat["x"])
        self.y_axis = np.array(dat["y"])
        self.x_label = figure["layout"]["xaxis"]["title"]["text"]
        self.y_label = figure["layout"]["yaxis"]["title"]["text"]
        self.title = figure["layout"]["title"]["text"]
        if self.num_axes == 2:
            self.z_axis = np.array(dat["z"])
            self.z_label = figure["layout"]["coloraxis"]["colorbar"]["title"]["text"]

    def apply(self, *args, **kwargs):
        """
        Calls the appropriate apply method based on the number of axes.

        Raises:
            NotImplementedError: If the number of axes is not 1 or 2.

        """
        try:
            match self.num_axes:
                case 1:
                    self.apply_1d(*args, **kwargs)
                case 2:
                    self.apply_2d(*args, **kwargs)
                case _:
                    logger.error(
                        f"Filtering not supported for {self.num_axes}D plots. Only 1D and 2D plots are supported."
                    )
                    raise NotImplementedError(
                        f"Filtering not supported for {self.num_axes}D plots. Only 1D and 2D plots are supported."
                        # Re-scale the colorbar
                    )
        except (NotImplementedError, Exception) as err:
            # TODOLATER: Connect to Toast notifications
            logger.error(err, exc_info=True)

        return self.new_fig

    def _update_title(self, fil: str) -> None:
        """
        Updates the plot title with the filter name.

        Args:
            fil (str): Filter name to append to plot title.

        """
        ttl = self.title
        title_default = " ".join(ttl.split(" ")[:4])
        tfl: str = fil
        if "Filters" in ttl:
            # NOTE: plot_title - Filters: fil1 fil2 ...
            # Default title - f"{_state.device_type} {_state.wafer_id} {_state.device_id} {_state.measurement}",
            # [4] is "Fil:"
            tfl: list[str] = ttl.split(" ")[6:]
            tfl.insert(0, fil)
            tfl: str = " ".join(tfl)

        # Update the title
        self.new_fig["layout"]["title"]["text"] = f"{title_default} <br> Filters: {tfl}"

    def _hmap_update(self, z_data: np.ndarray, fil: str) -> None:
        """
        Updates the 2D HeatMap plot with new Z-axis data & label and re-scales the colorbar.

        Args:
            z_data (np.ndarray): Z-axis data.
            fil (str): Filter name to append to plot title.

        Returns:
            go.Figure: Updated figure.

        """
        fig_caxis = self.new_fig["layout"]["coloraxis"]
        fig_caxis["colorbar"]["title"]["text"] = (
            f"Filters {self.z_label}" if "Filters" not in self.z_label else self.z_label
        )

        fig_caxis["cmin"] = z_data.min()
        fig_caxis["cmax"] = z_data.max()

        # Update the figure
        self.new_fig["data"][0]["z"] = z_data
        self.new_fig["layout"]["coloraxis"] = fig_caxis
        self._update_title(fil)


class Differentiate(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Differentiation Filter

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)

    def apply_1d(self, *_):
        """
        Applies the differentiation filter to a 1D plot.

        """
        self.new_fig["data"][0]["y"] = np.gradient(
            self.y_axis, abs(self.x_axis[1] - self.x_axis[0])
        )
        self.new_fig["layout"]["yaxis"]["title"]["text"] = f"d{self.y_label}"
        self._update_title("d")

    def apply_2d(self, twod_axis=0):
        """
        Apples the differentiation filter to a 2D plot.

        Args:
            twod_axis (int): Axis along which to differentiate

        """
        z_data = np.gradient(
            self.z_axis,
            abs(self.x_axis[1] - self.x_axis[0]),
            abs(self.y_axis[1] - self.y_axis[0]),
        )[twod_axis]

        match twod_axis:
            case 0:
                twod_axis_label = (
                    f"d{self.x_label}" if "$" not in self.x_label else "dx"
                )
            case 1:
                twod_axis_label = (
                    f"d{self.y_label}" if "$" not in self.y_label else "dy"
                )
            case _:
                err = f"Invalid value of `twod_axis={twod_axis}` for differentiation."
                logger.error(err)
                raise ValueError(err)

        # Update the figure
        self._hmap_update(z_data, fil=twod_axis_label)


class Smooth(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Smoothing Filter

        Features:
            - Savitzky-Golay filter

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.window = _safe_init(options, "window", DEFAULT_SAVGOL_OPTS["window"])
        self.polyorder = _safe_init(
            options, "polyorder", DEFAULT_SAVGOL_OPTS["polyorder"]
        )

    def apply_1d(self):
        """
        Applies the smoothing filter to a 1D plot.

        """
        self.new_fig["data"][0]["y"] = savgol_filter(
            self.y_axis,
            window_length=self.window,
            polyorder=self.polyorder,
        )
        self.new_fig["layout"]["yaxis"]["title"]["text"] = f"Sm {self.y_label}"
        self._update_title("Sm")

    def apply_2d(self):
        """
        Applies the smoothing filter to a 2D plot.

        """
        z_data = savgol_filter(
            self.z_axis,
            window_length=self.window,
            polyorder=self.polyorder,
        )

        # Update the figure
        self._hmap_update(z_data, fil="Sm")


class SimpleMovingAverage(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Simple Moving Average Filter.
        NOTE: Trailing: Output length is `window - 1` less than the input length.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.window = _safe_init(options, "window", DEFAULT_SMA_WINDOW)

    def apply_1d(self):
        """
        Applies the simple moving average filter to a 1D plot.

        """
        # NOTE: Trailing: Output length is `window - 1` less than the input length.
        self.new_fig["data"][0]["y"] = np.convolve(
            self.y_axis, np.ones(self.window) / self.window, mode="valid"
        )
        self.new_fig["layout"]["yaxis"]["title"]["text"] = f"SMA {self.y_label}"
        self._update_title("SMA")

    def apply_2d(self):
        """
        Not supported for 2D plots.

        """
        raise NotImplementedError("Simple Moving Average not supported for 2D plots.")


class Normalize(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Normalization Filter

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        # str: "x" or "y" or "z"
        self.axis = _safe_init(options, "axis", DEFAULT_NORM_OPTS["axis"])
        # float: value along the `axis` to slice data along z-axis, only for "x" or "y"
        self.axis_idx = _safe_init(options, "axis_idx", DEFAULT_NORM_OPTS["axis_idx"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Normalization not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the normalization filter to a 2D plot.

        """
        logger.debug(
            f"Normalizing 2D plot along axis `{self.axis}` at index `{self.axis_idx}`."
        )

        match self.axis:
            case "z":
                z_data = self.z_axis / np.max(self.z_axis)
            # NOTE: [i, j] = [row, col] = [y, x]
            case "x":
                z_data = self.z_axis / np.max(self.z_axis[:, self.axis_idx])
            case "y":
                z_data = self.z_axis / np.max(self.z_axis[self.axis_idx, :])
            case _:
                err = f"Invalid value of `axis={self.axis}` for normalization."
                logger.error(err)

        # Update the figure
        self._hmap_update(z_data, fil=f"Norm({self.axis})")


class GammaCorrection(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Gamma Correction Filter. Uses `skimage.exposure.adjust_gamma()`.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.gamma = _safe_init(options, "gamma", DEFAULT_GC_OPTS["gamma"])
        self.gain = _safe_init(options, "gain", DEFAULT_GC_OPTS["gain"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Gamma Correction not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the gamma correction filter to a 2D plot.

        """
        logger.debug(
            f"Applying Gamma Correction with gamma={self.gamma}, gain={self.gain}..."
        )
        z_data = exposure.adjust_gamma(self.z_axis, self.gamma, self.gain)

        # Update the figure
        self._hmap_update(z_data, fil="γC")


class LogCorrection(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Logarithmic Correction Filter. Uses `skimage.exposure.adjust_log()`.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.gain = _safe_init(options, "gain", DEFAULT_LC_OPTS["gain"])
        self.inv = _safe_init(options, "inv", DEFAULT_LC_OPTS["inv"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Logarithmic Correction not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the logarithmic correction filter to a 2D plot.

        """
        logger.debug(
            "Applying Logarithmic Correction with gain={self.gain}, inv={self.inv}..."
        )
        z_data = exposure.adjust_log(self.z_axis, gain=self.gain, inv=self.inv)

        # Update the figure
        self._hmap_update(z_data, fil="logC")


class SigmoidCorrection(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Sigmoid Correction Filter. Uses `skimage.exposure.adjust_sigmoid()`.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.cutoff = _safe_init(options, "cutoff", DEFAULT_SC_OPTS["cutoff"])
        self.gain = _safe_init(options, "gain", DEFAULT_SC_OPTS["gain"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Sigmoid Correction not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the sigmoid correction filter to a 2D plot.

        """
        logger.debug(
            "Applying Sigmoid Correction with cutoff={self.cutoff}, gain={self.gain}..."
        )
        z_data = exposure.adjust_sigmoid(
            self.z_axis, cutoff=self.cutoff, gain=self.gain
        )
        # Update the figure
        self._hmap_update(z_data, fil="σC")


class RescaleIntensity(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Rescale Intensity Filter. Uses `skimage.exposure.rescale_intensity()`.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.in_range = _safe_init(options, "in_range", DEFAULT_RI_OPTS["in_range"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Rescale Intensity not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the rescale intensity filter to a 2D plot. Uses the min-max scaling method.
        # TODOLATER: Can allow specifying the range to scale to. See: https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.rescale_intensity

        """
        logger.debug("Applying Rescale Intensity...")
        z_data = exposure.rescale_intensity(self.z_axis)

        # Update the figure
        self._hmap_update(z_data, fil="ReC")


class LogScale(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Logarithmic Scaling Filter.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)

    def apply_1d(self):
        """
        Applies the logarithmic scaling filter to a 1D plot.

        """
        self.new_fig["data"][0]["y"] = np.log(self.y_axis)
        self.new_fig["layout"]["yaxis"]["title"]["text"] = f"log {self.y_label}"
        self._update_title("log")

    def apply_2d(self):
        """
        Applies the logarithmic scaling filter to a 2D plot.

        """
        self._hmap_update(np.log(self.z_axis), fil="log")


class PolyFit(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Polynomial Fitting Filter. Uses `numpy.polynomial.polynomial.Polynomial.fit()`.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.deg = _safe_init(options, "deg", DEFAULT_POLYFIT_OPTS["deg"])
        self.window = _safe_init(options, "window", DEFAULT_POLYFIT_OPTS["window"])

    def apply_1d(self):
        """
        Applies the polynomial fitting filter to a 1D plot.

        """
        # Fit the data to a polynomial
        poly = Polynomial.fit(
            self.x_axis,
            self.y_axis,
            deg=self.deg,
            window=self.window,
        )
        fit_line = poly(self.x_axis)

        # Add the fit line to the plot
        self.new_fig.add_trace(
            go.Scatter(
                x=self.x_axis,
                y=fit_line,
                mode="lines",
                # TODOLATER: @s.anupam Standardize the color scheme & name etc.
                line=dict(color="rebeccapurple", width=2),
                # TODOLATER: Add to legend if needed. CUrrently hidden.
                showlegend=False,
                name=f"Fit (deg={self.deg})",
            )
        )

        # Add the equation to the plot
        # TODOLATER: Add a helper function that does the following::
        # TODOLATER: - [x] Add pretty-printed (LaTeX) polynomial equation with wrapped text
        # TODOLATER: - [ ] Add support for auto-wrapped text - See _pprint_poly()
        self.new_fig.add_annotation(
            # Center
            x=0.95,
            y=0.95,
            xref="paper",
            yref="paper",
            text=f"{_pprint_poly(poly, self.x_label)}",
            showarrow=False,
            font=dict(size=16, color="rebeccapurple"),
            bgcolor="white",
            # TODOLATER: Add if needed
            # BUG: Displaces the LaTeX-ified text
            # bordercolor="rebeccapurple",
            # borderwidth=1,
            # borderpad=4,
            # opacity=0.8,
            # width=200,  # To fit the text (text can overflow and get cut off)
        )

    def apply_2d(self):
        """
        Not supported for 2D plots.

        """
        raise NotImplementedError("Polynomial Fitting not supported for 2D plots.")


class RotateHeatMap(Filter):
    def __init__(self, figure: go.Figure, num_axes: int, options: dict = None) -> None:
        """
        Rotates HeatMap by specified angle.

        Args:
            figure (go.Figure): Plotly Figure object to apply filters to.
            num_axes (int): Number of axes in the figure.

        """
        super().__init__(figure, num_axes, options)
        self.angle = _safe_init(options, "angle", DEFAULT_ROTA_OPTS["angle"])

    def apply_1d(self):
        """
        Not supported for 1D plots.

        """
        raise NotImplementedError("Rotate HeatMap not supported for 1D plots.")

    def apply_2d(self):
        """
        Applies the rotate heatmap filter to a 2D plot.

        """
        logger.debug(f"Rotating HeatMap by {self.angle} degrees...")

        # Translate the data to the origin and then rotate
        z_data = self.z_axis

        logger.debug(f"z_data.shape: {z_data.shape}")

        angle_rad = np.deg2rad(self.angle)
        c, s = np.cos(angle_rad), np.sin(angle_rad)
        transform_matrix = np.array([[c, s], [-s, c]])
        center = np.array(z_data.shape) / 2
        # Align rotation around center
        offset = center - transform_matrix @ center
        # TODONOW: #StopTheCrop
        logger.debug(f"offset: {offset}")
        logger.debug(
            f"z_data.shape + offset: {z_data.shape + + 2 * np.round(np.abs(offset)).astype(int)}"
        )

        # TODONOW: #StopTheCrop
        # img_shape = np.asarray(z_data.shape)
        # in_plane_shape = img_shape[axes]
        # iy, ix = in_plane_shape
        # out_bounds = rot_matrix @ [[0, 0, iy, iy], [0, ix, 0, ix]]
        # # Compute the shape of the transformed input plane
        # out_plane_shape = (np.ptp(out_bounds, axis=1) + 0.5).astype(int)

        # out_center = rot_matrix @ ((out_plane_shape - 1) / 2)
        # in_center = (in_plane_shape - 1) / 2
        # offset = in_center - out_center

        # output_shape = img_shape
        # output_shape[axes] = out_plane_shape
        # output_shape = tuple(output_shape)

        z_data = affine_transform(
            z_data,
            transform_matrix,
            # Expand the data to avoid cropping, center the data # TODONOW: #StopTheCrop
            output_shape=z_data.shape,  # TODONOW: + 2 * np.round(np.abs(offset)).astype(int),
            offset=offset,  # TODONOW: - np.round(np.abs(offset)).astype(int),
            order=0,
            mode="constant",
            cval=np.nan,
            prefilter=False,
        )

        # Update the axis labels
        self.new_fig["layout"]["xaxis"]["title"][
            "text"
        ] = rf"${c:.3f}{self.x_label} + {-s:.3f}{self.y_label}\:({self.angle}^{{\circ}})$"
        self.new_fig["layout"]["yaxis"]["title"][
            "text"
        ] = rf"${s:.3f}{self.x_label} + {c:.3f}{self.y_label}\:({self.angle}^{{\circ}})$"

        # Update the figure
        self._hmap_update(z_data, fil=f"Rot({self.angle}°)")


def apply_filters(
    filters_order: list, filters_opts: dict, fig: go.Figure, fig_num_axes: int
) -> go.Figure:
    """
    # TODONOW: docs
    Applies the filters to the figure.

    Args:
        filters_order (list): List of filters to apply, in order.
        filters_opts (dict): Dict of filters to apply, with corresponding options.
        fig (go.Figure): Plotly Figure object to apply filters to.
        fig_num_axes (int): Number of axes in the figure.

    Returns:
        go.Figure: Filtered figure.

    """
    # TODONOW: filters_opts

    filt_fig = None
    fig_tmp = deepcopy(fig)
    for fil in filters_order:
        # `filter_opts` is a nested dict. Get the required dict and then pass it
        opts = filters_opts[fil]
        logger.debug(f"apply_filters | Filter: {fil} | Options: {opts}")
        match fil:
            case "diff":
                logger.debug("apply_filters | Applying `Differentiate` (1D) filter...")
                filt_obj = Differentiate(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()
            case "diff_x":
                logger.debug(
                    "apply_filters | Applying `Differentiate` (2D - x) filter..."
                )
                filt_obj = Differentiate(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply(twod_axis=0)
            case "diff_y":
                logger.debug(
                    "apply_filters | Applying `Differentiate` (2D - y) filter..."
                )
                filt_obj = Differentiate(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply(twod_axis=1)

            case "savgol":
                logger.debug("apply_filters | Applying `Smooth` filter...")
                filt_obj = Smooth(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "sma":
                logger.debug(
                    "apply_filters | Applying `Simple Moving Average` filter..."
                )
                filt_obj = SimpleMovingAverage(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "normalize":
                logger.debug("apply_filters | Applying `Normalize` filter...")
                filt_obj = Normalize(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "gamma_corr":
                logger.debug("apply_filters | Applying `Gamma Correction` filter...")
                filt_obj = GammaCorrection(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "log_corr":
                logger.debug(
                    "apply_filters | Applying `Logarithmic Correction` filter..."
                )
                filt_obj = LogCorrection(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "sig_corr":
                logger.debug("apply_filters | Applying `Sigmoid Correction` filter...")
                filt_obj = SigmoidCorrection(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "rescale_intensity":
                logger.debug("apply_filters | Applying `Rescale Intensity` filter...")
                filt_obj = RescaleIntensity(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "log_scale":
                logger.debug("apply_filters | Applying `Logarithmic Scaling` filter...")
                filt_obj = LogScale(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "rotate":
                logger.debug("apply_filters | Applying `Rotate HeatMap` filter...")
                filt_obj = RotateHeatMap(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case "polyfit":
                logger.debug("apply_filters | Applying `Polynomial Fitting` filter...")
                filt_obj = PolyFit(fig_tmp, fig_num_axes, opts)
                filt_fig = filt_obj.apply()

            case _:
                err = f"No definition for Filter {fil} was found."
                logger.error(err)
                raise ValueError(err)
        fig_tmp = filt_fig

    if filt_fig is None and not filters_order:
        # If no filters were applied, return the original figure
        logger.debug("No filters were applied.")
        return fig
    return filt_fig
