import json
from pathlib import Path
from datetime import datetime
from typing import Any, Tuple

import plotly.io as pio
from plotly import graph_objects as go
from dash import ALL, MATCH, Input, Output, State, callback, html, dcc
from dash import callback_context as ctx
from xarray import Dataset

# Local imports
from qimchi.components.appearance import apply_appearance_by_key, apply_appearance_axes
from qimchi.components.plot_elements import (
    appearance_line_options,
    appearance_marker_options,
)
from qimchi.components.utils import parse_data as parse
from qimchi.components.plots import Plot

from qimchi.state import _state
from qimchi.logger import logger


pio.templates.default = "none"


def plot_selector() -> html.Div:
    """
    Generator for the plot selector, defining the dropdowns for the dependent and independent variables.

    Returns:
        dash.html.Div: Dash div component containing the dropdowns for the dependent and independent variables.

    """
    return html.Div(
        [
            html.Div(
                [
                    html.P("Dependents"),
                    dcc.Dropdown(
                        className="dropdown",
                        id="dependent-dropdown",
                        persistence=True,
                        persistence_type="local",
                    ),
                ],
                className="column is-one-third",
            ),
            html.Div(
                [
                    html.P("Independents"),
                    dcc.Dropdown(
                        className="dropdown",
                        id="independent-dropdown",
                        multi=True,
                        persistence=True,
                        persistence_type="local",
                    ),
                ],
                className="column is-one-third",
            ),
            html.Div(
                html.Button("Add Plot", className="button is-3", id="add-plot"),
                className="column mt-auto",
            ),
            html.Div(
                html.Button(
                    "Clear All Plots",
                    className="button is-danger",
                    id="clear-all-plots",
                ),
                className="column mt-auto",
            ),
        ],
        className="columns is-full",
        id="plot-selector",
    )


def plots_container() -> html.Div:
    """
    Plots container

    Returns:
        dash.html.Div: Empty div to hold the plots, to be filled with callbacks

    """
    return html.Div(
        [
            html.Div([], className="columns is-multiline is-full", id="plots"),
        ]
    )


@callback(
    Input("measurement", "value"),
    Input("measurement-type", "value"),
    Input("device-id", "value"),
    Input("device-type", "value"),
    Input("wafer-id", "value"),
)
def update_state_wafer_id(
    measurement: str,
    measurement_type: str,
    device_id: str,
    device_type: str,
    wafer_id: str,
) -> None:
    """
    Update the state with the wafer id, device type, device id, measurement type, and measurement.

    """
    _state.wafer_id = wafer_id if wafer_id else _state.wafer_id
    _state.device_type = device_type if device_type else _state.device_type
    _state.device_id = device_id if device_id else _state.device_id
    _state.measurement_type = (
        measurement_type if measurement_type else _state.measurement_type
    )
    _state.measurement = measurement if measurement else _state.measurement
    _state.save_state()


def _update_plots_list(new_plots: list[html.Div], plots_list_tmp: list) -> list:
    """
    Utility function to update the plots list with new plots in Div.
    Args:
        new_plots (list): List of new plots in Div
        plots_list_tmp (list): List of existing plots in Div

    Returns:
        list: Updated list of plots in Div

    """
    plots_list_tmp.extend(
        [
            html.Div(
                new_plot,
                className="column is-half",
            )
            for new_plot in new_plots
        ]
    )

    return plots_list_tmp


def _add_default_plots(data: Dataset) -> list:
    """
    Utility function to add default plots based on the uploaded data.

    Args:
        data (dict): Dict representation of xarray.Dataset

    Returns:
        list: List of default plots

    """
    deps = list(data.data_vars.keys())  # [0] # TODOLATER: remove
    indeps = list(
        data[deps[0]].coords
    )  # TODOLATER: remove - # CONCERN: complication if deps becomes a list

    fig_divs = []
    # Line Plot
    try:
        fig_divs = [
            Plot(
                data=data,
                deps=deps,
                indeps=[indeps[0]],
                fig_id=None,
                # NOTE: These must be new objects; don't use defaults
                slider={},
                filters_order=[],
                filters_opts={},
            ).plot()
        ]
    except Exception as err:
        logger.error(f"Error in adding default LINE plot.\nError: {err}", exc_info=True)

    # If the data is multidimensional, add a HeatMap
    if len(indeps) > 1:
        try:
            fig_divs.extend(
                [
                    Plot(
                        data=data,
                        deps=deps,
                        indeps=indeps[:2],
                        fig_id=None,
                        # NOTE: These must be new objects; don't use defaults
                        slider={},
                        filters_order=[],
                        filters_opts={},
                    ).plot()
                ]
            )
        except Exception as err:
            logger.error(
                f"Error in adding default HEATMAP plot.\nError: {err}", exc_info=True
            )

    return _update_plots_list(fig_divs, [])


# TODOLATER: Pass relayout from the store
@callback(
    Output("plots", "children"),
    State("dependent-dropdown", "value"),
    State("independent-dropdown", "value"),
    State("plots", "children"),
    Input("upload-data", "data"),
    Input("add-plot", "n_clicks"),
    Input("clear-all-plots", "n_clicks"),
    Input({"type": "button-plot-delete", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def update_plot_list(
    dependents: str,  # TODOLATER: type, when deps is a list
    independents: list,
    plots_list: list,
    contents: dict,
    *_,
) -> Tuple[list]:
    """
    Callback to add a plot to the plots container, or to update existing plots in the container.
    Updates the container under certain conditions:
        1. If the data is uploaded for the first time, it generates default plots based on the data.
        2. If the user adds a new plot, it generates a new plot based on the selected dependent and independent variables.
        3. If the user clears all plots, it removes all the plots from the container.
        4. If the user deletes a specific plot, it removes the plot from the container.
        5. If the user uploads new data, it updates the plots based on the new data. Filters, ranges, and appearance settings are retained.

    Args:
        dependents (str): Selected dependent variables. # TODOLATER: type, when deps is a list
        independents (list): Selected independent variables.
        plots_list (list): List of plots in the plots container.
        contents (dict): Dict representation of xarray.Dataset

    Returns:
        tuple: Updated plots list.

    """
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    data = parse(contents)
    plots_list = plots_list or []

    if "index" in input_id:
        # TODOLATER: any better way to do this? Include in match?
        # To delete a specific plot when the delete button is clicked
        delete_chart = json.loads(input_id)["index"]
        plots_list = [
            chart
            for chart in plots_list
            if f"'index': '{delete_chart}'" not in str(chart)
        ]

        _state.plot_states.pop(delete_chart, None)
        _state.save_state()
        # logger.debug(f"Deleted plot {delete_chart}.")

    match input_id:
        case "clear-all-plots":
            _state.plot_states = {}
            _state.save_state()
            plots_list = []
            # logger.debug("Cleared all plots.")

        case "upload-data":
            # logger.warning("New data uploaded. UPDATING PLOTS...")
            # NOTE: Plot() adds fig info to `_state` internally
            if _state.plot_states != {}:
                # If there are plots already present, try plotting with new data
                try:
                    fig_divs = [
                        Plot(
                            data=data,
                            deps=fig_info["deps"],
                            indeps=fig_info["indeps"],
                            fig_id=fig_id,
                            slider=fig_info["slider"],
                            theme=fig_info["theme"],
                            filters_order=fig_info["filters_order"],
                            filters_opts=fig_info["filters_opts"],
                            plots_menu=fig_info["plots_menu"],
                        ).plot()
                        for fig_id, fig_info in _state.plot_states.items()
                    ]
                    plots_list = []  # NOTE: This makes _state the source of truth
                    plots_list = _update_plots_list(fig_divs, plots_list)
                    # logger.debug("Updated plots based on EXISTING data.")
                # If KeyError is raised, e.g., "ch# does not exist", clear all plots and start fresh with default plots
                except (KeyError, ValueError) as err:
                    # logger.error(f"Error: {err}")
                    _state.plot_states = {}
                    _state.save_state()
                    # logger.warning(
                    #     "Existing data mismatch. Cleared all plots. Adding default plots."
                    # )
                    plots_list = _add_default_plots(data)

            else:
                # If there are no plots present, add default plots
                plots_list = _add_default_plots(data)
                # logger.debug("No EXISTING data found. Created new plots.")

        case "add-plot":
            if all([dependents, independents]):
                fig_div = Plot(
                    data=data,
                    deps=[
                        dependents
                    ],  # TODOLATER: remove [] when deps is a proper list
                    indeps=independents,
                    fig_id=None,
                    # NOTE: These must be new objects; don't use defaults
                    slider={},
                    filters_order=[],
                    filters_opts={},
                ).plot()

                plots_list = _update_plots_list([fig_div], plots_list)
                # logger.debug("Added new plot.")
            # TODOLATER: add toast for error

    return plots_list


@callback(
    Output({"type": "plots-menu-dropdown", "index": MATCH}, "style"),
    Output({"type": "content-ranges", "index": MATCH}, "style"),
    Output({"type": "content-appearance", "index": MATCH}, "style"),
    Output({"type": "content-filters", "index": MATCH}, "style"),
    Output({"type": "button-plot-ranges", "index": MATCH}, "className"),
    Output({"type": "button-plot-appearance", "index": MATCH}, "className"),
    Output({"type": "button-plot-filters", "index": MATCH}, "className"),
    State({"type": "button-plot-ranges", "index": MATCH}, "className"),
    State({"type": "button-plot-appearance", "index": MATCH}, "className"),
    State({"type": "button-plot-filters", "index": MATCH}, "className"),
    Input({"type": "button-plot-ranges", "index": MATCH}, "n_clicks"),
    Input({"type": "button-plot-appearance", "index": MATCH}, "n_clicks"),
    Input({"type": "button-plot-filters", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle_dropdown(
    r_state: str,
    a_state: str,
    s_state: str,
    r_n_clicks: int,
    a_n_clicks: int,
    s_n_clicks: int,
) -> tuple:
    """
    Callback to toggle the dropdowns for the plot options.
    Toggles the dropdowns for the plot options when the corresponding button is clicked.
    Changes the color to `warning` when the button is active, and changes it back, when the button is clicked again.

    Args:
        r_state (str): State of the ranges dropdown from the class name.
        a_state (str): State of the appearance dropdown from the class name.
        s_state (str): State of the filters dropdown from the class name.

    Returns:
        tuple: Tuple of display styles and class names for the dropdowns and buttons.

    """
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    button = json.loads(input_id)["type"]
    fig_id = json.loads(input_id)["index"]
    fig_plot_menu = _state.plot_states[fig_id]["plots_menu"]

    ret_styles = None

    def reset_plot_buttons():
        fig_plot_menu.update(
            {
                "ranges_n_clicks": 0,
                "ranges_cname": "button mb-2",
                "appearance_n_clicks": 0,
                "appearance_cname": "button mb-2",
                "filters_n_clicks": 0,
                "filters_cname": "button mb-2",
                "plots_menu_dropdown_disp": "none",
                "content_ranges_disp": "none",
                "content_appearance_disp": "none",
                "content_filters_disp": "none",
            }
        )
        _state.plot_states[fig_id]["plots_menu"] = fig_plot_menu
        _state.save_state()
        # logger.debug(f"Reset plot buttons. || fig_plot_menu (AFTER): {fig_plot_menu}")

        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            "button mb-2",
            "button mb-2",
            "button mb-2",
        )

    match button:
        case "button-plot-ranges":
            # logger.debug(
            #     f"Ranges button clicked. || Fig ID: {fig_id} || r_state: {r_state}"
            # )
            # Toggle off
            if r_state == "button is-warning mb-2":
                return reset_plot_buttons()

            # Toggle on
            fig_plot_menu.update(
                {
                    "ranges_n_clicks": r_n_clicks,
                    "ranges_cname": "button is-warning mb-2",
                    "appearance_n_clicks": 0,
                    "appearance_cname": "button mb-2",
                    "filters_n_clicks": 0,
                    "filters_cname": "button mb-2",
                    "plots_menu_dropdown_disp": "unset",
                    "content_ranges_disp": "unset",
                    "content_appearance_disp": "none",
                    "content_filters_disp": "none",
                }
            )
            ret_styles = (
                {"display": "unset"},
                {"display": "unset"},
                {"display": "none"},
                {"display": "none"},
                "button is-warning mb-2",
                "button mb-2",
                "button mb-2",
            )

        case "button-plot-appearance":
            # logger.debug(
            #     f"Appearance button clicked. || Fig ID: {fig_id} || a_state: {a_state}"
            # )
            # Toggle off
            if a_state == "button is-warning mb-2":
                return reset_plot_buttons()

            # Toggle on
            fig_plot_menu.update(
                {
                    "ranges_n_clicks": 0,
                    "ranges_cname": "button mb-2",
                    "appearance_n_clicks": a_n_clicks,
                    "appearance_cname": "button is-warning mb-2",
                    "filters_n_clicks": 0,
                    "filters_cname": "button mb-2",
                    "plots_menu_dropdown_disp": "unset",
                    "content_ranges_disp": "none",
                    "content_appearance_disp": "unset",
                    "content_filters_disp": "none",
                }
            )
            ret_styles = (
                {"display": "unset"},
                {"display": "none"},
                {"display": "unset"},
                {"display": "none"},
                "button mb-2",
                "button is-warning mb-2",
                "button mb-2",
            )

        case "button-plot-filters":
            # logger.debug(
            #     f"Filters button clicked. || Fig ID: {fig_id} || s_state: {s_state}"
            # )
            # Toggle off
            if s_state == "button is-warning mb-2":
                return reset_plot_buttons()

            # Toggle on
            fig_plot_menu.update(
                {
                    "ranges_n_clicks": 0,
                    "ranges_cname": "button mb-2",
                    "appearance_n_clicks": 0,
                    "appearance_cname": "button mb-2",
                    "filters_n_clicks": s_n_clicks,
                    "filters_cname": "button is-warning mb-2",
                    "plots_menu_dropdown_disp": "unset",
                    "content_ranges_disp": "none",
                    "content_appearance_disp": "none",
                    "content_filters_disp": "unset",
                }
            )
            ret_styles = (
                {"display": "unset"},
                {"display": "none"},
                {"display": "none"},
                {"display": "unset"},
                "button mb-2",
                "button mb-2",
                "button is-warning mb-2",
            )
        case _:
            reset_plot_buttons()

    _state.plot_states[fig_id]["plots_menu"] = fig_plot_menu
    _state.save_state()
    # logger.debug(f"Plot Menu (AFTER): {fig_plot_menu}")

    return ret_styles


@callback(
    Output({"index": MATCH, "type": "line-options"}, "children"),
    Input({"index": MATCH, "key": "line", "setting": "mode"}, "value"),
    prevent_initial_call=True,
)
def update_settings(line_mode: list[str]) -> tuple:
    """
    Callback to update the settings based on the line mode dropdown.

    Args:
        line_mode (list): Selected line mode.

    Returns:
        tuple: Updated class names for the settings.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    fig_id = input_id["index"]
    logger.debug(f"Line mode: {line_mode}")
    fig_plot_menu = _state.plot_states[fig_id]["plots_menu"]
    logger.debug(f"Line mode | fig_plot_menu (BEFORE): {fig_plot_menu}")

    ret_con = None
    match line_mode:
        case "markers":
            # Show markers only
            fig_plot_menu["appearance_line_options_disp"] = False
            fig_plot_menu["appearance_marker_options_disp"] = True
            ret_con = (appearance_marker_options(fig_id),)
        case "lines":
            # Show lines only
            fig_plot_menu["appearance_line_options_disp"] = True
            fig_plot_menu["appearance_marker_options_disp"] = False
            ret_con = (appearance_line_options(fig_id),)
        case "lines+markers":
            # Show both
            fig_plot_menu["appearance_line_options_disp"] = True
            fig_plot_menu["appearance_marker_options_disp"] = True
            ret_con = (
                appearance_line_options(fig_id),
                appearance_marker_options(fig_id),
            )
    logger.debug(f"Line mode | fig_plot_menu (AFTER): {fig_plot_menu}")
    _state.plot_states[fig_id]["plots_menu"] = fig_plot_menu
    _state.save_state()

    return ret_con


@callback(
    Output({"index": MATCH, "type": "relayout-data"}, "data"),
    Input({"index": MATCH, "type": "figure"}, "relayoutData"),
)
def store_relayout_data(relayout_data: dict) -> dict:
    """
    Callback to store the relayout data in dcc.Store to be used while exporting the plot.

    Args:
        relayout_data (dict): Relayout data from the plot.

    Returns:
        dict: Relayout data.

    """
    if relayout_data:
        return relayout_data
    return {}


# TODOLATER: BUG: See notes.py::update_notes()
# @callback(
#     Output({"index": MATCH, "type": "notes-store"}, "data", allow_duplicate=True),
#     State({"index": MATCH, "type": "relayout-data"}, "data"),
#     State({"index": MATCH, "type": "figure"}, "figure"),
#     Input({"index": MATCH, "type": "button-plot-send-to-md"}, "n_clicks"),
#     prevent_initial_call=True,
# )
# def send_img_to_notes(
#     relayout_data: dict,
#     orig_fig: go.Figure,
#     n_clicks: int,
# ) -> str:
#     """
#     # TODO: Docs

#     """
#     # TODO: Remove some debug logs
#     logger.debug(f"Attempting image addition...")

#     logger.debug(f"relayout_data : {type(relayout_data)}")
#     logger.debug(f"orig_fig : {type(orig_fig)}")
#     logger.debug(f"n_clicks : {type(n_clicks)}")
#     logger.debug(f"n_clicks val : {n_clicks}")

#     input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
#     fig_id = input_id["index"]
#     logger.debug(f"{fig_id}: Attempting image addition...")
#     meas_path = Path(_state.measurement_path)

#     # Get current notes from disk
#     notes = _get_notes()

#     # Save to file
#     # Output directory # NOTE: Different from the one in `export_images`
#     exports_dir = meas_path.parent / meas_path.stem / "exports/notes"
#     exports_dir.mkdir(exist_ok=True)

#     # Filename
#     # NOTE: The first 8 characters of the measurement ID
#     meas_id_short = meas_path.stem[:8]
#     fig_cls = _state.plot_states[fig_id]["plot_type"]
#     filename = (
#         exports_dir
#         / f"{meas_id_short}__{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}__{fig_cls}.png"
#     )

#     if n_clicks > 0:
#         logger.debug(f"{fig_id}: Exporting images...")
#         logger.debug(f"{fig_id}: Export path: {exports_dir}")

#         try:
#             # Reload the original figure as a valid Plotly figure
#             fig = go.Figure(orig_fig)
#             # Apply the relayout changes (zoom, pan, grid/tick settings etc.)
#             if relayout_data:
#                 logger.debug(f"{fig_id}: Relayout data: {relayout_data}")
#                 fig.plotly_relayout(relayout_data)
#                 logger.debug(f"{fig_id}: Applied relayout data.")

#             # Ensure transparent background
#             fig.update_layout(
#                 paper_bgcolor="rgba(0,0,0,0)",
#                 plot_bgcolor="rgba(0,0,0,0)",
#             )

#             # TODO: @s.anupam Customize the look of the exported figures

#             # Save
#             pio.write_image(fig, f"{filename}")

#             logger.debug(
#                 f"{fig_id}: Image added to markdown. Exported to {exports_dir} as {filename}"
#             )

#             # Append centered image (using <center> tag)
#             notes += f"""
# <center>

# <img src="./exports/notes/{filename.name}" alt="{filename.name}" width="400"/>

# </center>

# """

#         except Exception as err:
#             logger.error(
#                 f"{fig_id}: Error adding to markdown.\nError: {err}", exc_info=True
#             )

#         return notes


@callback(
    # NOTE: Styled using Bulma, not Bootstrap
    Output({"index": MATCH, "type": "export-toast"}, "className"),
    Output({"index": MATCH, "type": "export-toast"}, "children"),
    Output({"index": MATCH, "type": "export-toast"}, "is_open"),
    Input({"index": MATCH, "type": "button-plot-export"}, "n_clicks"),
    State({"index": MATCH, "type": "relayout-data"}, "data"),
    State({"index": MATCH, "type": "figure"}, "figure"),
    prevent_initial_call=True,
)
def export_images(
    n_clicks: int,
    relayout_data: dict,
    orig_fig: go.Figure,
) -> Tuple[str, str, bool]:
    """
    Callback to export the figure in .svg, .png. .pdf formats in light and dark mode with relayout.
    Shows a toast notification with the export status.

    Args:
        n_clicks (int): Number of clicks on the export button.
        relayout_data (dict): Relayout data from the plot.
        orig_fig (go.Figure): Original figure.

    Returns:
        Tuple[str, str, bool]: Toast color, message, and is_open status.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    fig_id = input_id["index"]
    logger.debug(f"{fig_id}: Attempting image export...")
    meas_path = Path(_state.measurement_path)

    # Output directory
    exports_dir = meas_path.parent / meas_path.stem / "exports"
    exports_dir.mkdir(exist_ok=True, parents=True)

    # Filenames
    # NOTE: The first 8 characters of the measurement ID
    meas_id_short = meas_path.stem[:8]
    fig_cls = _state.plot_states[fig_id]["plot_type"]
    base_filename = (
        exports_dir
        / f"{meas_id_short}__{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}__{fig_cls}"
    )
    formats = ["png", "svg"]  # , "pdf"]

    if n_clicks > 0:
        logger.debug(f"{fig_id}: Exporting images...")
        logger.debug(f"{fig_id}: Export path: {exports_dir}")

        try:
            # Reload the original figure as a valid Plotly figure
            fig = go.Figure(orig_fig)
            # Apply the relayout changes (zoom, pan, grid/tick settings etc.)
            if relayout_data:
                logger.debug(f"{fig_id}: Relayout data: {relayout_data}")
                fig.plotly_relayout(relayout_data)
                logger.debug(f"{fig_id}: Applied relayout data.")

            # Ensure transparent background
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            # TODO: @s.anupam Customize the look of the exported figures

            # NOTE: To avoid https://github.com/plotly/plotly.py/issues/3469
            # 1. Write an arbitrary .pdf plot to file first.
            # 2. Sleep for 0.2 seconds.
            # 3. Save the actual plot in each format.
            # logger.debug(f"{fig_id}: Saving arbitrary plot...")
            # arb_fig = go.Figure(data=go.Scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16]))
            # pio.write_image(arb_fig, f"{base_filename}_arbitrary.pdf")
            # sleep(2)

            # Save in each format
            for fmt in formats:
                pio.write_image(fig, f"{base_filename}.{fmt}")

            # Same in dark mode
            fig.update_layout(template="plotly_dark")
            for fmt in formats:
                pio.write_image(fig, f"{base_filename}_dark.{fmt}")

            # Delete the arbitrary .pdf plot
            # Path(f"{base_filename}_arbitrary.pdf").unlink()
            # logger.debug(f"{fig_id}: Deleted arbitrary .pdf plot.")

            logger.debug(
                f"{fig_id}: Images exported to {exports_dir} as {', '.join(formats)}"
            )

            return ("notification p-4 is-success", "Export successful", True)

        except Exception as err:
            logger.error(
                f"{fig_id}: Error exporting images.\nError: {err}", exc_info=True
            )

            return ("notification p-4 is-danger", "Export failed", True)

    return ("", "", False)


@callback(
    Output({"type": "figure", "index": MATCH}, "figure", allow_duplicate=True),
    State({"type": "figure", "index": MATCH}, "figure"),
    Input({"index": MATCH, "key": ALL, "setting": ALL}, "value"),
    prevent_initial_call=True,
)
def update_plot_by_type(
    figure: dict,
    _: list,
) -> go.Figure:
    """
    Callback to update the plot appearance settings by plot type.

    Args:
        figure (dict): Dict representation of a go.Figure object.
        _: List of values from the dropdowns. Unused.

    Returns:
        go.Figure: Updated figure.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    app_val = ctx.triggered[0]["value"]
    fig_id = input_id["index"]
    fig = _state.plot_states[fig_id]

    app_setting = input_id["setting"]
    key = input_id["key"]

    # Update _state
    fig["theme"][key][app_setting] = app_val
    _state.save_state()
    # logger.debug(f"Updated _state for plot {fig_id} with new appearance settings.")

    return apply_appearance_by_key(
        input_id, figure, app_val=app_val, key=key, app_setting=app_setting
    )


@callback(
    Output({"type": "figure", "index": MATCH}, "figure", allow_duplicate=True),
    State({"type": "figure", "index": MATCH}, "figure"),
    Input({"index": MATCH, "axis": ALL, "ticks": ALL, "setting": ALL}, "value"),
    prevent_initial_call=True,
)
def update_plot_axes(
    figure: dict,
    _: list,
) -> go.Figure:
    """
    Callback to update the plot appearance settings for the axes.

    Args:
        figure (dict): Dict representation of a go.Figure object.
        _: List of values from the dropdowns. Unused.

    Returns:
        go.Figure: Updated figure.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    app_val = ctx.triggered[0]["value"]
    fig_id = input_id["index"]
    fig = _state.plot_states[fig_id]

    app_setting = input_id["setting"]
    axis = input_id["axis"]
    ticks = input_id["ticks"]

    # Update _state
    fig["theme"][axis][ticks][app_setting] = app_val
    _state.save_state()
    # logger.debug(
    #     f"Updated _state for the axes of plot {fig_id} with new appearance settings."
    # )
    # logger.debug(f"theme: {fig['theme']}")

    return apply_appearance_axes(
        input_id,
        figure,
        app_val=app_val,
        axis=axis,
        ticks=ticks,
        app_setting=app_setting,
    )


@callback(
    Output({"type": "figure", "index": MATCH}, "figure", allow_duplicate=True),
    State("upload-data", "data"),
    Input({"type": ALL, "index": MATCH, "menu": "ranges", "extra": ALL}, "value"),
    prevent_initial_call=True,
)
def update_plot_range(
    contents: Dataset,
    range_val: float,
) -> go.Figure:
    """
    Updates the plot based on the range slider values and filter button clicks.

    Args:
        contents (dict): Dict representation of xarray.Dataset loaded from the uploaded file.
        range_val (float): Value of the range slider.

    Returns:
        go.Figure: Updated figure.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    fig_id = input_id["index"]
    fig = _state.plot_states[fig_id]
    data = parse(contents)

    slider_id = json.loads(input_id["extra"])["dim"]
    slider = fig["slider"]
    slider[slider_id]["value"] = range_val[list(slider.keys()).index(slider_id)]
    _state.save_state()

    # NOTE: Filters are applied in the Plot class
    fig_div = Plot(
        data=data,
        deps=fig["deps"],
        indeps=fig["indeps"],
        fig_id=fig_id,
        slider=slider,
        theme=fig["theme"],
        filters_order=fig["filters_order"],
        filters_opts=fig["filters_opts"],
        plots_menu=fig["plots_menu"],
    ).plot(return_div=False)

    logger.debug(f"Updated plot {fig_id} with new ranges.")
    return fig_div


@callback(
    Output({"index": MATCH, "type": "figure"}, "figure", allow_duplicate=True),
    State("upload-data", "data"),
    Input({"index": MATCH, "type": ALL, "menu": "filter-opts"}, "value"),
    prevent_initial_call=True,
)
def update_filter_opts(
    contents: Dataset,
    _: Any,
) -> go.Figure:
    """
    Updates the filter opts and the plot.

    Args:
        contents (dict): Dict representation of xarray.Dataset loaded from the uploaded file.

    Returns:
        go.Figure: Updated figure.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    app_val = ctx.triggered[0]["value"]
    fig_id = input_id["index"]
    fil_type = input_id["type"]
    data = parse(contents)

    # Update "filters_opts" dict in _state
    fil, fil_opt = fil_type.split("-")
    fig = _state.plot_states[fig_id]
    fil_opts = fig["filters_opts"]

    # Check if corresponding filter_opts exists
    if fil not in fil_opts:
        fil_opts.update({fil: {}})
    fil_opts[fil][fil_opt] = app_val
    _state.save_state()

    logger.debug(
        f"update_filter_opts | {input_id=}, {fig_id=}, {fil_type=} {fil=} {fil_opt=} {app_val=}"
    )

    # Redo the plot with the new filter options applied,...
    # NOTE: ...depending on whether the filter is toggled on.
    # NOTE: Filters are applied in the Plot class
    fig_div = Plot(
        data=data,
        deps=fig["deps"],
        indeps=fig["indeps"],
        fig_id=fig_id,
        slider=fig["slider"],
        theme=fig["theme"],
        filters_order=fig["filters_order"],
        filters_opts=fil_opts,
        plots_menu=fig["plots_menu"],
    ).plot(return_div=False)

    logger.debug(
        f"update_filter_opts | Updated plot {fig_id} with new filters_opts: {fil_opts}."
    )
    return fig_div


@callback(
    Output({"index": MATCH, "type": "figure"}, "figure", allow_duplicate=True),
    State("upload-data", "data"),
    Input({"index": MATCH, "type": ALL, "menu": "filter-apply"}, "value"),
    prevent_initial_call=True,
)
def update_filter_apply(
    contents: Dataset,
    _: Any,
) -> go.Figure:
    """
    Updates the plot based on the applied filters.

    Args:
        contents (dict): Dict representation of xarray.Dataset loaded from the uploaded file.

    Returns:
        go.Figure: Updated figure.

    """
    input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    app_val = ctx.triggered[0]["value"]
    fig_id = input_id["index"]
    fil_type = input_id["type"]
    data = parse(contents)

    # Update "filters_order" list in _state
    fil = fil_type.split("-")[
        1
    ]  # NOTE: Get the filter name (same as in filters.py::apply_filters() cases)
    fig = _state.plot_states[fig_id]
    fil_order = fig["filters_order"]
    if fil in fil_order:
        fil_order.remove(fil)
    else:
        fil_order.extend([fil])

    # Ensures that the filters are unique & preserve order
    fil_order = [*dict.fromkeys(fil_order)]

    # Check if corresponding filter_opts exists
    if fil not in fig["filters_opts"]:
        fig["filters_opts"].update({fil: {}})

    # Save the updated state
    _state.save_state()

    logger.debug(
        f"update_filter_apply | {input_id=}, {fig_id=}, {fil_type=} {fil=} {app_val=} {fil_order=}"
    )

    # Redo the plot with the new filters applied
    # NOTE: Filters are applied in the Plot class
    fig_div = Plot(
        data=data,
        deps=fig["deps"],
        indeps=fig["indeps"],
        fig_id=fig_id,
        slider=fig["slider"],
        theme=fig["theme"],
        filters_order=fil_order,
        filters_opts=fig["filters_opts"],
        plots_menu=fig["plots_menu"],
    ).plot(return_div=False)

    logger.debug(
        f"update_filter_apply | Updated plot {fig_id} with new filters_order: {fil_order}."
    )
    return fig_div
