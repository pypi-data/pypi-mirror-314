from pathlib import Path

from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

# Local imports
import qimchi.components.data as data
from qimchi.components.data import (
    __all__ as DATASET_TYPES,
)  # NOTE: __all__ is a list of all the public names in the module
from qimchi.components.utils import parse_data as parse
from qimchi.state import _state, DATA_REFRESH_INTERVAL
from qimchi.logger import logger


def data_selector() -> html.Div:
    """
    Generator for the data selector component.

    Returns:
        dash.html.Div: The data selector component

    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Interval(
                        id="upload-ticker",
                        interval=DATA_REFRESH_INTERVAL,
                        n_intervals=0,
                    ),
                    html.Div(
                        dcc.Input(
                            className="input",
                            type="text",
                            placeholder="Dataset Path",
                            id="dataset-path",
                            persistence=True,
                            persistence_type="local",
                        ),
                        className="column is-5 mb-0 pb-0",
                    ),
                    html.Div(
                        dcc.Dropdown(
                            options=DATASET_TYPES,
                            placeholder="Dataset type",
                            id="dataset-type",
                            persistence=True,
                            persistence_type="local",
                        ),
                        className="column is-2 mb-0 pb-0",
                    ),
                    html.Div(
                        html.Button(
                            "Submit", id="submit", className="button is-warning"
                        ),
                        className="column is-2 mb-0 pb-0",
                    ),
                    html.Div(
                        className="column is-12 m-1 pt-0 mt-0",
                        id="data-options",
                    ),
                    dcc.Store("upload-data"),
                ],
                className="columns is-full is-multiline ml-1 mr-1 is-flex is-vcentered",
                id="selector",
            ),
        ]
    )


@callback(
    Output("data-options", "children"),
    State("data-options", "children"),
    Input("dataset-type", "value"),
    Input("dataset-path", "value"),
    Input("submit", "n_clicks"),
    prevent_initial_call=True,
)
def update_options(
    contents: None | html.Div, dataset_type: str, dataset_path: str, _
) -> html.Div:
    """
    Updates the options for the data selector.

    Args:
        contents (None | html.Div): The current contents of the data selector
        dataset_type (str): The type of the dataset
        dataset_path (str): The path to the dataset

    Returns:
        dash.html.Div: The updated data selector component

    """
    if dataset_type is not None and dataset_path is not None:
        try:
            dataset_path = Path(dataset_path)
            logger.debug(f"Dataset Type: {dataset_type}")
            logger.debug(f"Dataset Path: {dataset_path}")

            # Import `dataset_type` class from data module and instantiate it
            data_cls = getattr(data, dataset_type)(path=dataset_path)
            logger.debug(f"Dataset Class: {data_cls}")

            # Update the state
            _state.dataset_path = dataset_path
            _state.dataset_type = dataset_type
            _state.save_state()

            return data_cls.selector()
        except AttributeError:
            # CONCERN: API: XarrayData is being handled differently from XarrayDataFolder
            logger.error("AttributeError from update_options()")
            return contents
    return contents


@callback(
    Output("submit", "n_clicks"),
    State("submit", "n_clicks"),
    State("data-options", "children"),
    Input("upload-ticker", "n_intervals"),
)
def refresh(n_clicks: int, data_options: list, _) -> int:
    """
    Refreshes the submit button, auto-submitting the data path and options.

    Args:
        n_clicks (int): The current number of clicks
        data_options (list): The data options

    Returns:
        int: The number of clicks

    """
    if data_options is None:
        return n_clicks
    else:
        raise PreventUpdate


@callback(
    Output("dependent-dropdown", "options"),
    Input("upload-data", "data"),
)
def update_dependents(contents: dict | None) -> list:
    """
    Updates the dependent dropdown options.

    Args:
        contents (dict | None): Dict representation of xarray.Dataset or None

    Returns:
        list: The dependent dropdown options generated from the data

    Raises:
        PreventUpdate: If `contents` is None

    """
    if contents is None:
        raise PreventUpdate
    data = parse(contents)
    return list(data.data_vars.keys())


@callback(
    Output("independent-dropdown", "options"),
    Input("upload-data", "data"),
    Input("dependent-dropdown", "value"),
)
def update_independents(contents: dict | None, dependents: list):
    """
    Updates the independent dropdown options.

    Args:
        contents (dict): Dict representation of xarray.Dataset or None
        dependents (list): List of dependent variables

    Returns:
        list: The independent dropdown options generated from the data

    Raises:
        PreventUpdate: If `contents` or `dependents` is None

    """
    if contents is None or dependents is None:
        raise PreventUpdate
    data = parse(contents)
    return list(data[dependents].coords)
