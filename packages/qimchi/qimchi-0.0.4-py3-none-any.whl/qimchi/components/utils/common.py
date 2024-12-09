import xarray as xr
from dash.exceptions import PreventUpdate


def parse_data(data: dict) -> xr.Dataset:
    """
    Utility function to parse data into xarray dataset

    Args:
        data (dict): Dictionary containing the data to be parsed

    Returns:
        xr.Dataset: Parsed xarray dataset

    """
    if data is None:
        raise PreventUpdate
    return xr.Dataset.from_dict(data)
