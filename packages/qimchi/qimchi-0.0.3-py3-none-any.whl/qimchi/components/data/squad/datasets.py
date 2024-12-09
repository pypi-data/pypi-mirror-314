from pathlib import Path
from typing import Any, List

import dash
import xarray as xr
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

# Local imports
from ..base import Data, Database
from qimchi.state import _state
from qimchi.logger import logger
from qimchi.components.utils import parse_data as parse


def _update_options_fn(
    condition_list: List[str | Path | Any],
    check_file: bool = False,
    default_return: List[str] | None = [],
) -> List[str] | str | None:
    """
    Helper function to update options based on the condition list.

    Args:
        condition_list (List[str | Path | Any]): List of parameters to compare with None.
            Ordering matters, as the path is constructed from the first item to the second last item.
            The last item is always assumed to be `dataset_type`
        check_file (bool, optional): Check if the path is a file, by default False (checks for directory)
        default_return (List | None, optional): Default return item if the condition is not satisfied, by default []

    Returns:
        List[str] | str | None: List of strings (options) or empty list or None

    """
    # NOTE: This only checks for truthy (i.e., "" is False, but Path("") is True). Should work here though.
    if all(condition_list):
        # Assuming either strings or Paths
        path = Path(*condition_list[:-1])

        if not path.is_dir():
            logger.debug(f"Path {path} is not a directory.")
            return default_return
        # Unfiltered options
        options: List[str] = [p.name for p in path.iterdir()]
        # Filter for only files or directories
        options = [
            opt
            for opt in options
            if (
                # TODOLATER: Some redundancy here
                (path / opt).is_dir() and (path / opt).suffix == ".zarr"
                if check_file
                else (path / opt).is_dir()
            )
        ]
        return options

    return default_return


def _update_data(path: Path, data_store: None | dict, origin: str) -> dict | None:
    """
    Conditionally update the data store with the Zarr file content.

    Args:
        path (Path): Path to the dataset
        data_store (None | dict): The current data store

    Returns:
        dict | None: The updated data store or None

    """
    if path.is_dir() and path.suffix == ".zarr":
        curr_mod_time = path.stat().st_mtime
        if path == _state.measurement_path:
            if curr_mod_time != _state.measurement_last_fmt:
                logger.warning(f"{origin}: DATA UPDATED ON DISK!! AT {path}.")
                _state.measurement_last_fmt = curr_mod_time
                _state.save_state()

                logger.warning(f"{origin}: LOADING DATA FROM UPDATED {path}")
                ds = xr.load_dataset(path, engine="zarr").to_dict()
                logger.warning(f"{origin}: DATA LOADED FROM UPDATED {path}")
                return ds
            # If the data has not been modified
            if data_store:
                # If the data is already loaded, do not reload
                return None
            # If the data has not been loaded even once, load it (e.g., for the first time on page load)
            ds = xr.load_dataset(path, engine="zarr").to_dict()
            logger.warning(f"{origin}: DATA LOADED FROM {path}")
            return ds
        else:
            # If the path has changed, update the state
            logger.warning(f"{origin}: DATA PATH MODIFIED!! AT {path}.")
            _state.measurement_path = path
            _state.measurement_last_fmt = curr_mod_time
            _state.save_state()

            logger.warning(f"{origin}: LOADING DATA FROM MODIFIED {path}")
            ds = xr.load_dataset(path, engine="zarr").to_dict()

            if origin == "XarrayData":
                # To update the wafer_id etc. in the state
                data = parse(ds)
                metadata = data.attrs
                device_type = metadata.get("Device Type", "")
                wafer_id = metadata.get("Wafer ID", "")
                sample_name = metadata.get("Sample Name", "")
                meas_id = metadata.get("Measurement ID", "")

                # Update the state
                _state.device_type = device_type
                _state.wafer_id = wafer_id
                _state.device_id = sample_name
                _state.measurement = meas_id
                _state.save_state()

            logger.warning(f"{origin}: DATA LOADED FROM MODIFIED {path}")
            return ds


class XarrayDataFolder(Database):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
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

    @staticmethod
    @callback(
        Output("wafer-id", "options"),
        State("wafer-id", "options"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("selector", "children"),
        Input("metadata-viewer", "children"),
        prevent_initial_call=True,
    )
    def update_wafer_id(
        wafer_options: List[str], dataset_path: str | Path, dataset_type: str, *_
    ) -> List[str]:
        return _update_options_fn(
            [dataset_path, dataset_type], default_return=wafer_options
        )

    @staticmethod
    @callback(
        Output("device-type", "options"),
        State("device-type", "options"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("selector", "children"),
        Input("metadata-viewer", "children"),
        prevent_initial_call=True,
    )
    def update_device_type(
        device_type_options: List[str],
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        return _update_options_fn([dataset_path, wafer_id, dataset_type])

    @staticmethod
    @callback(
        Output("device-id", "options"),
        State("device-id", "options"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("selector", "children"),
        Input("metadata-viewer", "children"),
        prevent_initial_call=True,
    )
    def update_device_id(
        device_id_options: List[str],
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        return _update_options_fn([dataset_path, wafer_id, device_type, dataset_type])

    @staticmethod
    @callback(
        Output("measurement-type", "options"),
        State("measurement-type", "options"),
        Input("device-id", "value"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("selector", "children"),
        Input("metadata-viewer", "children"),
        prevent_initial_call=True,
    )
    def update_measurement_type(
        measurement_type_options: List[str],
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        return _update_options_fn(
            [dataset_path, wafer_id, device_type, device_id, dataset_type],
        )

    @staticmethod
    @callback(
        Output("measurement", "options"),
        State("measurement", "options"),
        Input("measurement-type", "value"),
        Input("device-id", "value"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("selector", "children"),
        Input("metadata-viewer", "children"),
        prevent_initial_call=True,
    )
    def update_measurement(
        measurement_options: List[str],
        measurement_type: str,
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        return _update_options_fn(
            [
                dataset_path,
                wafer_id,
                device_type,
                device_id,
                measurement_type,
                dataset_type,
            ],
            check_file=True,  # Checks if the path is a measurement file
        )

    @staticmethod
    @callback(
        Output(
            "upload-data",
            "data",
            allow_duplicate=True,
        ),
        State("upload-data", "data"),
        Input(
            "measurement",
            "value",
        ),
        State("measurement-type", "value"),
        State("device-id", "value"),
        State("device-type", "value"),
        State("wafer-id", "value"),
        State("dataset-path", "value"),
        Input("selector", "children"),
        Input("upload-ticker", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_data(
        data_store: None | dict,
        measurement: str,
        measurement_type: str,
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        *_,
    ) -> dict:
        """
        Update the data store with the Zarr file content.

        Args:
            data_store (None | dict): The current data store
            measurement (str): Measurement name
            measurement_type (str): Measurement type
            device_id (str): Device ID
            device_type (str): Device type
            wafer_id (str): Wafer ID
            dataset_path (str | Path): Path to the dataset

        Returns:
            dict: The updated data store

        Raises:
            PreventUpdate: If the path is not a file or not a Zarr file

        """
        if measurement is None:
            raise PreventUpdate

        if all(
            [
                measurement,
                measurement_type,
                device_id,
                device_type,
                wafer_id,
                dataset_path,
            ]
        ):
            measurement_path = Path(
                dataset_path,
                wafer_id,
                device_type,
                device_id,
                measurement_type,
                measurement,
            )
            path = measurement_path
            out: dict | None = _update_data(path, data_store, "XarrayDataFolder")
            if out:
                return out
            else:
                raise PreventUpdate

    @staticmethod
    @callback(
        Output("measurement", "value"),
        Input("prev-mmnt-button", "n_clicks"),
        Input("next-mmnt-button", "n_clicks"),
        Input("measurement", "value"),
        State("measurement", "options"),
    )
    def update_selected_measurement(
        _prev_clicks: int, _next_clicks: int, curr_mmnt: str, mmnt_options: list
    ) -> int:
        """
        Updates selected measurement based on button clicks or dropdown selection.

        Args:
            _prev_clicks (int): Number of clicks on the previous button
            _next_clicks (int): Number of clicks on the next button
            curr_mmnt (str): Current selected measurement
            mmnt_options (list): List of measurement options

        Returns:
            str: New selected measurement

        Raises:
            PreventUpdate: If the options are not available

        """
        if mmnt_options is None:
            old_mmnt = _state.measurement
            # NOTE: Assuming this is None only on reload
            logger.debug(
                f"Options not available: Returning old measurement: {old_mmnt}"
            )
            return old_mmnt

        # Identify which button was pressed
        triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        curr_idx = mmnt_options.index(curr_mmnt)
        if triggered_id == "prev-mmnt-button":
            new_index = (curr_idx - 1) % len(mmnt_options)  # Cycle left
        elif triggered_id == "next-mmnt-button":
            new_index = (curr_idx + 1) % len(mmnt_options)  # Cycle right
        else:
            new_index = curr_idx  # No change

        logger.debug(f"New index: {new_index}")
        logger.debug(f"New option: {mmnt_options[new_index]}")

        return mmnt_options[new_index]

    def options(self):
        return html.Div(
            [
                html.Div("Sample Information:", className="column is-1"),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="wafer-id",
                            placeholder="Wafer ID",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="device-type",
                            placeholder="Device Type",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="device-id",
                            placeholder="Device ID",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="measurement-type",
                            placeholder="Measurement Type",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="measurement",
                            placeholder="Measurement",
                            searchable=True,
                            # NOTE: Persistence handled server-side
                        )
                    ],
                    className="column",
                ),
                html.Button(
                    html.I(className="fa-solid fa-arrow-left button"),
                    id="prev-mmnt-button",
                    n_clicks=0,
                ),
                html.Button(
                    html.I(className="fa-solid fa-arrow-right button"),
                    id="next-mmnt-button",
                    n_clicks=0,
                ),
            ],
            className="columns is-full is-multiline is-flex is-vcentered",
        )


class XarrayData(Data):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    @callback(
        Output(
            "upload-data",
            "data",
            allow_duplicate=True,
        ),
        State("upload-data", "data"),
        Input("dataset-path", "value"),
        Input("upload-ticker", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_data(data_store: None | dict, path: str, *_):
        """
        Update the data store with the Zarr file content.

        Args:
            path (str): Path to the Zarr file
            data_store (None | dict): The current data store

        Returns:
            dict: The updated data store

        Raises:
            PreventUpdate: If the path is not a file or not a Zarr file

        """
        if path is None:
            raise PreventUpdate

        path = Path(path)
        out: dict | None = _update_data(path, data_store, "XarrayData")
        if out:
            return out
        else:
            raise PreventUpdate
