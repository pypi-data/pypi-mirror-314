from pathlib import Path
from datetime import datetime
from string import Template
from typing import Tuple

from dash import Input, Output, callback, html, dcc
from dash.exceptions import PreventUpdate

# Local imports
from qimchi.state import _state
from qimchi.logger import logger


# Default Frontmatter - Obsidian style
FRONTMATTER = Template(
    """---
Last Saved: ${timestamp}
Filename: ${filename}

---"""
)
DEFAULT_NOTES = "Type your notes here..."


def _get_notes() -> str:
    """
    Utility function to load or create notes

    Returns:
        str: Notes to be displayed in the notes viewer

    """
    base = Path(_state.measurement_path)
    if not _state.measurement_last_fmt:
        logger.debug("Notes | No measurement found")
        return DEFAULT_NOTES

    path = base.parent / base.stem / (base.stem + ".md")

    if path.exists():
        logger.debug(f"Notes | Loading from: {path}")
        with open(path, "r") as f:
            notes = f.read()

        # Remove frontmatter
        notes = notes.split("---\n")
        notes = "---\n".join(notes[2:])

        return notes

    else:
        logger.debug(f"Notes | Creating new at: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

        notes_to_write = (
            FRONTMATTER.substitute(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                filename=path.stem,
            )
            + "\n"
            + DEFAULT_NOTES
        )

        # Save to file
        logger.debug(f"Notes | NEW | Saving to: {path}")
        with open(path, "w") as f:
            f.write(notes_to_write)

        return DEFAULT_NOTES


def notes_viewer() -> html.Div:
    """
    Notes viewer

    Returns:
        dash.html.Div: Div element containing a textarea for notes and a collapsible markdown viewer

    """
    return html.Div(
        [
            dcc.Textarea(
                id="notes-area",
                value=_get_notes(),
                className="column m-2 p-3",
                style={
                    "minHeight": "175px",
                    "maxHeight": "278px",
                },
            ),
            html.Div(
                dcc.Markdown(
                    id="notes-preview",
                    className="content m-0 p-0",
                    mathjax=True,
                    # NOTE: Local
                    dangerously_allow_html=True,
                    style={
                        "minHeight": "175px",
                        "maxHeight": "270px",
                        "overflowY": "scroll",
                    },
                ),
                id="notes-preview-div",
                className="column m-2 p-3",
                style={
                    "minHeight": "175px",
                    "maxHeight": "278px",
                    "overflowY": "scroll",
                },
            ),
            html.Button(
                html.I(className="fa-solid fa-eye-slash"),
                id="hide-preview",
                className="button is-info is-pulled-right mr-3",
                style={
                    "maxHeight": "280px",
                },
            ),
        ],
        className="columns is-multiline box m-0 p-1 is-hidden",
        style={"maxHeight": "300px"},
        id="notes-viewer",
    )


@callback(
    Output("notes-preview-div", "style"),
    Output("hide-preview", "children"),
    Input("hide-preview", "n_clicks"),
)
def show_hide_preview(n_clicks: int) -> tuple:
    """
    Callback to show or hide the markdown preview

    Args:
        n_clicks (int): Number of times the button has been clicked

    Returns:
        tuple: Style to display the markdown preview and the button icon

    """
    if n_clicks is None or n_clicks % 2 == 0:
        return {"display": "block"}, html.I(className="fa-solid fa-eye-slash")
    else:
        return {"display": "none"}, html.I(className="fa-solid fa-eye")


@callback(
    Output("notes-preview", "children"),
    Input("notes-area", "value"),
)
def update_output(new_notes: str) -> str:
    """
    Callback to update the markdown preview

    Args:
        new_notes (str): Value of the notes textarea

    Returns:
        str: Markdown preview to be displayed

    """
    if new_notes is None:
        logger.debug("Notes | UPDATE | No notes to update")
        raise PreventUpdate
    # Save to file and update Last Saved
    base = Path(_state.measurement_path)
    if not _state.measurement_last_fmt:
        logger.debug("Notes | UPDATE | No measurement found")
        raise PreventUpdate

    path = base.parent / base.stem / (base.stem + ".md")

    if path.exists():
        logger.debug(f"Notes | UPDATE | Updating notes for: {path}")
        logger.debug(f"Notes | UPDATE | Updating notes with: {new_notes}")
        notes = (
            FRONTMATTER.substitute(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                filename=path.stem,
            )
            + "\n"
            + new_notes
        )

        # Save to file
        logger.debug(f"Notes | UPDATE | Saving to: {path}")
        with open(path, "w") as f:
            f.write(notes)

        # Update preview
        return rf"{new_notes}"

    else:
        logger.debug(f"Notes | UPDATE | No notes found at: {path}")
        return DEFAULT_NOTES


@callback(
    Output("notes-viewer", "className"),
    # TODOLATER: Figure out how to push plots to the notes
    Output("notes-area", "value"),  # , allow_duplicate=True),
    Input("upload-data", "data"),
    # TODOLATER:
    # BUG: True required for `allow_duplicate`, but it makes the notes non-persistent.
    # BUG: But it is needed to allow multiple callbacks with `notes-area` as output. So, ¯\_(ツ)_/¯
    # prevent_initial_call=True,
)
def update_notes(content) -> Tuple[str, str]:
    """
    Callback to update notes & preview

    Returns:
        Tuple[str, str]: Style to display the notes viewer and the notes to be displayed

    """
    notes = _get_notes()
    if content is None:
        return "columns is-multiline box m-0 p-1 is-hidden", notes
    logger.debug("Notes | Updating notes from upload-data")
    return "columns is-multiline box m-0 p-1", notes


# TODOLATER: Figure out how to push plots to the notes. See update_notes() above.
# @callback(
#     Output({"index": ALL, "type": "notes-store"}, "data", allow_duplicate=True),
#     Output("notes-area", "value", allow_duplicate=True),
#     Input({"index": ALL, "type": "notes-store"}, "data"),
#     prevent_initial_call=True,
# )
# def update_notes_from_store(notes_from_stores: list) -> Tuple[list, str]:
#     """
#     Callback to update notes from stores and to empty the stores after

#     Args:
#         notes_from_stores (list): List of notes from stores

#     Returns:
#         Tuple[list, str]: List of empty notes stores and the notes to be displayed

#     """
#     logger.debug(f"notes_from_stores : {notes_from_stores}")

#     # If notes found in stores, return the first one and empty all stores
#     empty_notes_stores = [None] * len(notes_from_stores)
#     for notes in notes_from_stores:
#         if notes:
#             logger.debug(f"Notes | Updating notes from store: {notes}")
#             return empty_notes_stores, notes

#     # If no notes found in stores, prevent update
#     logger.debug("Notes | No notes found in stores")
#     return empty_notes_stores, _get_notes()
