from plotly import colors
from dash.exceptions import PreventUpdate

# Local imports
from qimchi.logger import logger


def apply_appearance_axes(
    input_id: dict,
    figure: dict,
    app_val: str,
    axis: str,
    ticks: str,
    app_setting: str,
) -> dict:
    """
    Applies appearance settings to the axes of `figure`.

    Args:
        input_id (dict): Input ID containing appearance information to modify.
        figure (dict): Dict representation of a go.Figure object.
        app_val (str): Appearance value to apply.
        axis (str): Axis to apply the appearance settings to. Either "x" or "y".
        ticks (str): Ticks to apply the appearance settings to. Either "maj" or "min".
        app_setting (str): Appearance type to apply.

    Returns:
        dict: dict representation of the modified figure.

    """
    logger.debug(
        f"Applying appearance settings to the axes of the figure: {input_id}, {app_val}..."
    )
    fig_layout = figure["layout"]

    match axis:
        case "x":
            fig_ax = fig_layout["xaxis"]
        case "y":
            fig_ax = fig_layout["yaxis"]
        case _:
            raise PreventUpdate

    match ticks:
        case "maj":
            fig_ticks = fig_ax
        case "min":
            fig_ticks = fig_ax["minor"]
        case _:
            raise PreventUpdate

    fig_ticks[app_setting] = app_val

    return figure


def apply_appearance_by_key(
    input_id: dict,
    figure: dict,
    app_val: str,
    key: str,
    app_setting: str,
) -> dict:
    """
    Changes the appearance of the figure based on the provided key.

    Args:
        input_id (dict): Input ID containing appearance information to modify.
        figure (dict): Dict representation of a go.Figure object.
        app_val (str): Appearance value to apply.
        key (str): Key to apply the appearance settings to. One of "hmap", "line", or "marker".
        app_setting (str): Appearance type to apply.

    Returns:
        dict: dict representation of the modified figure

    """
    logger.debug(f"Applying appearance settings to figure: {input_id}, {app_val}...")
    logger.debug(f"Setting key: {key}")

    fig = figure["data"][0]
    match key:
        case "hmap":
            fig_caxis = figure["layout"]["coloraxis"]
            match app_setting:
                case "colorscale":
                    fig_caxis["colorscale"] = colors.get_colorscale(app_val)
                case "rangecolor":
                    fig_caxis["cmin"] = app_val[0]
                    fig_caxis["cmax"] = app_val[1]
                case _:
                    raise PreventUpdate

        case "line":
            fig_line = fig["line"]
            match app_setting:
                case "mode":
                    fig["mode"] = app_val
                case "opacity":
                    fig["opacity"] = app_val
                case _:
                    fig_line[app_setting] = app_val

        case "marker":
            fig_marker = fig["marker"]
            fig_marker[app_setting] = app_val

    return figure
