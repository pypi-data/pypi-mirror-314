import json
from ast import literal_eval
from datetime import datetime

from dash import Input, Output, callback, html

# Local imports
from qimchi.components.utils import parse_data as parse


def metadata_viewer() -> html.P:
    """
    Metadata viewer

    Returns:
        dash.html.P: Paragraph element, displaying all the metadata relevant to the uploaded data

    """
    return html.P(
        "", className="column is-full has-background-light", id="metadata-viewer"
    )


def _render_tree(data):
    """
    Recursive function to render collapsible items
    """
    if isinstance(data, dict):
        return html.Ul(
            [
                html.Li(
                    # If the value is an empty list, empty string, empty dict, or None, render as "key: value" without a collapsible arrow
                    (
                        html.Span(
                            [
                                html.Strong(f"{key}", style={"color": "black"}),
                                f": {value}",
                            ]
                        )
                        if value in [None, [], "", {}]
                        else (
                            html.Span(
                                [
                                    html.Strong(f"{key}", style={"color": "black"}),
                                    f": {value}",
                                ]
                            )
                            if not isinstance(value, dict)
                            # Otherwise, make it collapsible, if it's a dictionary
                            else html.Details(
                                [
                                    html.Summary(
                                        html.Strong(key, style={"color": "black"}),
                                        style={"cursor": "pointer"},
                                    ),
                                    _render_tree(
                                        value
                                    ),  # NOTE: Recursively render nested dicts
                                ]
                            )
                        )
                    ),
                    style={
                        "listStyleType": "none",
                        "marginLeft": "20px",
                    },  # No bullets, indented
                )
                for key, value in data.items()
            ],
            style={"paddingLeft": "0px"},
        )
    else:
        # Render non-dict values directly as strings in a span
        return html.Span(str(data))


@callback(
    Output("metadata-viewer", "children"),
    Input("upload-data", "data"),
)
def update_metadata_viewer(contents: dict) -> list:
    """
    Callback to update metadata viewer

    Args:
        contents (dict): Dict representation of xarray.Dataset

    Returns:
        list: Metadata list to be displayed in the metadata viewer

    """
    if contents is None:
        return "No Data Uploaded"

    data = parse(contents)
    metadata = data.attrs
    dt = datetime.fromisoformat(metadata["Timestamp"])
    meta = []

    # Do not populate these keys in the metadata viewer
    forbidden_keys = [
        "Requirements",
        "Code Archive",
    ]
    for key in metadata:
        if key in forbidden_keys:
            continue

        meta.append(html.B(f"{key.capitalize()}: "))
        if key == "Timestamp":
            meta.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
            meta.append(html.Br())

        elif key == "Cryostat":
            data = metadata[key].capitalize()
            meta.append(data)
            meta.append(html.Br())

        elif key == "independent_parameter_instruments":
            data = metadata[key]
            data = literal_eval(
                data
            )  # NOTE: The dicts are stored as strings in the list
            for dct in data:
                # NOTE: Convert single quotes to double quotes and None to "None" to make the string JSON serializable
                dct = dct.replace("'", '"')
                dct = dct.replace("None", '"None"')

                # Load the now JSON-serializable string
                dct = json.loads(dct)
                meta.append(
                    html.Details(
                        [
                            html.Summary(
                                html.Strong(
                                    f"{dct['name'].upper()}", style={"color": "black"}
                                ),
                                style={"cursor": "pointer"},
                            ),
                            _render_tree(dct),
                        ]
                    ),
                )
        else:
            meta.append(metadata[key])
            meta.append(html.Br())

    return meta
