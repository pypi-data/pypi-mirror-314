from abc import ABC, abstractmethod
from xarray import Dataset

from plotly.express import colors, imshow, line
from plotly.express.colors import named_colorscales
from plotly import graph_objects as go


# Local imports
from qimchi.logger import logger
from qimchi.state import _state


class QimchiFigure(ABC):
    def __init__(
        self,
        data: Dataset,
        independents: list,
        dependents: list,
        num_axes: int,
        colors=None,
        theme: dict = None,
    ) -> None:
        """
        Qimchi Figure Base Class

        Args:
            data (Dataset): Data to be plotted
            independents (list): Independent variables
            dependents (list): Dependent variables
            num_axes (int): Number of axes in the figure
            colors (list, optional): Colors for the plot. Defaults to None.
            theme (dict, optional): Theme dict for the plot. Defaults to None.

        Raises:
            ValueError: If the number of independent variables is greater than the number of axes.

        """
        self.data = data
        self.ind = independents
        self.deps = dependents
        self.colors = colors
        self.theme = theme
        self.num_axes = num_axes

        if len(self.ind) > self.num_axes:
            raise ValueError(
                f"Line plot can only have {self.num_axes} independent variable"
            )
        if type(self.deps) is list and len(self.deps) > 1:
            err = "Plots can only have one dependent variable."
            logger.error(err)
            raise ValueError(err)

    @abstractmethod
    def plot(self) -> go.Figure:
        """
        Abstract method to plot the figure.

        Returns:
            go.Figure: Plotly Figure object

        """


class Line(QimchiFigure):
    """
    Qimchi Line Plot Class

    """

    def __init__(
        self, data: Dataset, independents: list, dependents: list, theme: dict
    ) -> None:
        super().__init__(data, independents, dependents, theme=theme, num_axes=1)
        self.traces = {
            "mode": theme["line"]["mode"],
            "line": {
                "color": theme["line"]["color"],
                "width": theme["line"]["width"],
                "dash": theme["line"]["dash"],
                "shape": theme["line"]["shape"],
                "smoothing": theme["line"]["smoothing"],
            },
            "marker": {
                "symbol": theme["marker"]["symbol"],
                "size": theme["marker"]["size"],
                "color": theme["marker"]["color"],
                "opacity": theme["marker"]["opacity"],
            },
            "opacity": theme["line"]["opacity"],
        }

        logger.debug(
            f"Line || independents: {independents} | dependent: {dependents} | theme: {theme}"
        )
        # logger.debug(
        #     f"Line || self.data.coords : {self.data.coords}"  # | self.data.data : {self.data.data}"
        # )

    def plot(self) -> go.Figure:
        theme = self.theme
        layout = {
            "title": {
                "text": f"{_state.device_type} {_state.wafer_id} {_state.device_id} {_state.measurement}",
                "font": dict(
                    family="Roboto, sans-serif",
                    size=10,
                    color="rgba(0,0,0,0.6)",
                ),
                "x": 0.5,
                "y": 0.97,
            },
            "xaxis": {
                "title": self.ind[0],
                "ticks": "outside",
                "showline": True,
                "mirror": True,
                "automargin": True,
                "zeroline": False,
                "linewidth": 2,
                # Customizable
                "showgrid": theme["x"]["maj"]["showgrid"],
                "type": theme["x"]["maj"]["type"],
                "nticks": theme["x"]["maj"]["nticks"],
                "griddash": theme["x"]["maj"]["griddash"],
                "gridcolor": theme["x"]["maj"]["gridcolor"],
                "gridwidth": theme["x"]["maj"]["gridwidth"],
                "tickcolor": theme["x"]["maj"]["tickcolor"],
                "tickwidth": theme["x"]["maj"]["tickwidth"],
                "ticklen": theme["x"]["maj"]["ticklen"],
                "tickangle": theme["x"]["maj"]["tickangle"],
                "minor": {
                    "showgrid": theme["x"]["min"]["showgrid"],
                    "nticks": theme["x"]["min"]["nticks"],
                    "griddash": theme["x"]["min"]["griddash"],
                    "gridcolor": theme["x"]["min"]["gridcolor"],
                    "gridwidth": theme["x"]["min"]["gridwidth"],
                    "tickcolor": theme["x"]["min"]["tickcolor"],
                    "tickwidth": theme["x"]["min"]["tickwidth"],
                    "ticklen": theme["x"]["min"]["ticklen"],
                },
            },
            "yaxis": {
                "title": self.deps,
                "ticks": "outside",
                "showline": True,
                "mirror": True,
                "exponentformat": "e",
                "automargin": True,
                "zeroline": False,
                "linewidth": 2,
                # Customizable
                "showgrid": theme["y"]["maj"]["showgrid"],
                "type": theme["y"]["maj"]["type"],
                "nticks": theme["y"]["maj"]["nticks"],
                "griddash": theme["y"]["maj"]["griddash"],
                "gridcolor": theme["y"]["maj"]["gridcolor"],
                "gridwidth": theme["y"]["maj"]["gridwidth"],
                "tickcolor": theme["y"]["maj"]["tickcolor"],
                "tickwidth": theme["y"]["maj"]["tickwidth"],
                "ticklen": theme["y"]["maj"]["ticklen"],
                "tickangle": theme["y"]["maj"]["tickangle"],
                "minor": {
                    "showgrid": theme["y"]["min"]["showgrid"],
                    "nticks": theme["y"]["min"]["nticks"],
                    "griddash": theme["y"]["min"]["griddash"],
                    "gridcolor": theme["y"]["min"]["gridcolor"],
                    "gridwidth": theme["y"]["min"]["gridwidth"],
                    "tickcolor": theme["y"]["min"]["tickcolor"],
                    "tickwidth": theme["y"]["min"]["tickwidth"],
                    "ticklen": theme["y"]["min"]["ticklen"],
                },
            },
            "font": {
                "size": 15,
            },
            "margin": {"l": 50, "r": 10, "t": 40, "b": 50},
        }

        dat = self.data
        fig = line(
            dat.data,
            x=dat.coords[self.ind[0]],
            y=dat,
        )
        fig.update_layout(layout)
        fig.update_traces(self.traces)
        logger.debug("Line || PLOTTED")

        return fig


class HeatMap(QimchiFigure):
    """
    Qimchi HeatMap Plot Class

    """

    def __init__(
        self, data: Dataset, independents: list, dependents: list, theme: dict
    ) -> None:
        super().__init__(data, independents, dependents, theme=theme, num_axes=2)
        self.colors = named_colorscales()
        self.colorscale = theme["hmap"]["colorscale"]
        self.rangecolor = theme["hmap"]["rangecolor"]
        data_min = float(data.min().values)
        data_max = float(data.max().values)

        if self.rangecolor is not None:
            self.rangecolor[0] = max(float(self.rangecolor[0]), data_min)
            self.rangecolor[1] = min(float(self.rangecolor[1]), data_max)
        else:
            self.rangecolor = [data_min, data_max]
        self.theme["hmap"]["rangecolor"] = self.rangecolor

        logger.debug(
            f"HeatMap || independents: {independents} | dependent: {dependents} | theme: {theme}"
        )
        # logger.debug(
        #     f"HeatMap || self.data.coords : {self.data.coords}"  # | self.data.data : {self.data.data}"
        # )

    def plot(self) -> go.Figure:
        theme = self.theme
        layout = {
            "title": {
                "text": f"{_state.device_type} {_state.wafer_id} {_state.device_id} {_state.measurement}",
                "font": dict(
                    family="Roboto, sans-serif",
                    size=10,
                    color="rgba(0,0,0,0.6)",
                ),
                "x": 0.5,
                "y": 0.97,
            },
            "xaxis": {
                "title": self.ind[1],  # TODOLATER: theme["x"]["title"],
                "ticks": "outside",
                "showline": True,
                "mirror": True,
                "automargin": True,
                "zeroline": False,
                "linewidth": 2,
                # Customizable
                "nticks": theme["x"]["maj"]["nticks"],
                "tickcolor": theme["x"]["maj"]["tickcolor"],
                "tickwidth": theme["x"]["maj"]["tickwidth"],
                "ticklen": theme["x"]["maj"]["ticklen"],
                "tickangle": theme["x"]["maj"]["tickangle"],
                "minor": {
                    "nticks": theme["x"]["min"]["nticks"],
                    "tickcolor": theme["x"]["min"]["tickcolor"],
                    "tickwidth": theme["x"]["min"]["tickwidth"],
                    "ticklen": theme["x"]["min"]["ticklen"],
                },
            },
            "yaxis": {
                "title": self.ind[0],  # TODOLATER: theme["y"]["title"],
                "ticks": "outside",
                "showline": True,
                "mirror": True,
                "automargin": True,
                "zeroline": False,
                "linewidth": 2,
                # Customizable
                "nticks": theme["y"]["maj"]["nticks"],
                "tickcolor": theme["y"]["maj"]["tickcolor"],
                "tickwidth": theme["y"]["maj"]["tickwidth"],
                "ticklen": theme["y"]["maj"]["ticklen"],
                "tickangle": theme["y"]["maj"]["tickangle"],
                "minor": {
                    "nticks": theme["y"]["min"]["nticks"],
                    "tickcolor": theme["y"]["min"]["tickcolor"],
                    "tickwidth": theme["y"]["min"]["tickwidth"],
                    "ticklen": theme["y"]["min"]["ticklen"],
                },
            },
            "font": {
                "size": 15,
            },
            "coloraxis": {
                "colorbar_title": self.deps,  # TODOLATER: theme["colorbar_title"],
                "colorscale": colors.get_colorscale(self.colorscale),
                "cmin": self.rangecolor[0],
                "cmax": self.rangecolor[1],
                "colorbar": {
                    "exponentformat": "e",
                    "ticklen": 5,
                    "tickwidth": 2,
                    "outlinewidth": 2,
                },
            },
            "margin": {"l": 50, "r": 10, "t": 40, "b": 50},
        }

        if self.data.data.shape[0] != self.data.coords[self.ind[0]].shape[0]:
            self.data = self.data.T

        fig = imshow(
            self.data,
            x=self.data.coords[self.ind[1]],
            y=self.data.coords[self.ind[0]],
            origin="lower",  # NOTE: Moves origin to lower left
        )
        fig.update_layout(layout)
        logger.debug("HeatMap || PLOTTED")

        return fig
