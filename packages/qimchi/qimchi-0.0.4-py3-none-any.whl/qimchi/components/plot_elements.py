from dash import dcc, html

# Local imports
from qimchi.state import (
    # Line & marker options
    DEFAULT_LINE_MODE,
    DEFAULT_LINE_COLOR,
    DEFAULT_LINE_WIDTH,
    DEFAULT_LINE_OPACITY,
    DEFAULT_LINE_DASH,
    DEFAULT_LINE_SHAPE,
    DEFAULT_SPLINE_SMOOTHING,
    DEFAULT_MARKER_COLOR,
    DEFAULT_MARKER_SIZE,
    DEFAULT_MARKER_SYMBOL,
    DEFAULT_MARKER_OPACITY,
    LINE_COLOR_OPTS,
    LINE_DASH_OPTS,
    LINE_MODE_OPTS,
    LINE_SHAPE_OPTS,
    MARKER_COLOR_OPTS,
    MARKER_SYMBOL_OPTS,
)


def appearance_line_dropdown(fig_id: str) -> html.Div:
    return dcc.Dropdown(
        id={
            "index": fig_id,
            "key": "line",
            "setting": "mode",
        },
        options=LINE_MODE_OPTS,
        value=DEFAULT_LINE_MODE,
        placeholder="Line Mode",
        clearable=False,
        persistence=True,
        persistence_type="local",
    )


def appearance_line_options(fig_id: str) -> html.Div:
    return html.Div(
        id={
            "setfor": "line",
            "index": fig_id,
        },
        children=[
            html.Div(
                [
                    dcc.Dropdown(
                        id={
                            "index": fig_id,
                            "key": "line",
                            "setting": "color",
                        },
                        options=LINE_COLOR_OPTS,
                        value=DEFAULT_LINE_COLOR,
                        placeholder="Line Color",
                        clearable=False,
                        persistence=True,
                        persistence_type="local",
                        style={"width": "100%", "margin": "2px"},
                    ),
                    dcc.Dropdown(
                        id={
                            "index": fig_id,
                            "key": "line",
                            "setting": "dash",
                        },
                        options=LINE_DASH_OPTS,
                        value=DEFAULT_LINE_DASH,
                        placeholder="Line Dash",
                        clearable=False,
                        persistence=True,
                        persistence_type="local",
                        style={"width": "100%", "margin": "2px"},
                    ),
                    dcc.Dropdown(
                        id={
                            "index": fig_id,
                            "key": "line",
                            "setting": "shape",
                        },
                        options=LINE_SHAPE_OPTS,
                        value=DEFAULT_LINE_SHAPE,
                        placeholder="Line Shape",
                        clearable=False,
                        persistence=True,
                        persistence_type="local",
                        style={"width": "100%", "margin": "2px"},
                    ),
                ],
                className="column is-full is-flex px-0",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label(
                                "Line Width: ",
                                className="column is-one-quarter",
                                style={"fontWeight": "bold"},
                            ),
                            dcc.Slider(
                                min=0.0,
                                max=20.0,
                                step=0.5,
                                marks={0: "0", 20: "20"},
                                value=DEFAULT_LINE_WIDTH,
                                id={
                                    "index": fig_id,
                                    "key": "line",
                                    "setting": "width",
                                },
                                persistence=True,
                                persistence_type="local",
                                className="column is-three-quarters mx-0 my-2 p-3",
                            ),
                        ],
                        className="column is-flex is-one-third",
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Line Opacity: ",
                                className="column is-one-quarter",
                                style={"fontWeight": "bold"},
                            ),
                            dcc.Slider(
                                min=0.0,
                                max=1.0,
                                step=0.05,
                                marks={0: "0", 1: "1"},
                                value=DEFAULT_LINE_OPACITY,
                                id={
                                    "index": fig_id,
                                    "key": "line",
                                    "setting": "opacity",
                                },
                                persistence=True,
                                persistence_type="local",
                                className="column is-three-quarters mx-0 my-2 p-3",
                            ),
                        ],
                        className="column is-flex is-one-third",
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Spline Smoothing: ",
                                className="column is-one-quarter",
                                style={"fontWeight": "bold"},
                            ),
                            dcc.Slider(
                                min=0.0,
                                max=1.3,
                                step=0.05,
                                marks={0: "0", 1.3: "1.3"},
                                value=DEFAULT_SPLINE_SMOOTHING,
                                id={
                                    "index": fig_id,
                                    "key": "line",
                                    "setting": "smoothing",
                                },
                                persistence=True,
                                persistence_type="local",
                                className="column is-three-quarters mx-0 my-2 p-3",
                            ),
                        ],
                        className="column is-flex is-one-third",
                    ),
                ],
                className="column is-full is-flex p-0",
            ),
        ],
        # Always visible
        className="column is-full is-flex-wrap-wrap p-0",
    )


def appearance_marker_options(fig_id: str) -> html.Div:
    return html.Div(
        id={
            "setfor": "marker",
            "index": fig_id,
        },
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                id={
                                    "index": fig_id,
                                    "key": "marker",
                                    "setting": "color",
                                },
                                options=MARKER_COLOR_OPTS,
                                value=DEFAULT_MARKER_COLOR,
                                placeholder="Marker Color",
                                clearable=False,
                                persistence=True,
                                persistence_type="local",
                                # NOTE: className="column is-half" refuses to work here
                                style={"width": "100%", "margin": "2px"},
                            ),
                            dcc.Dropdown(
                                id={
                                    "index": fig_id,
                                    "key": "marker",
                                    "setting": "symbol",
                                },
                                options=MARKER_SYMBOL_OPTS,
                                value=DEFAULT_MARKER_SYMBOL,
                                placeholder="Marker Symbol",
                                clearable=False,
                                persistence=True,
                                persistence_type="local",
                                # NOTE: className="column is-half" refuses to work here
                                style={"width": "100%", "margin": "2px"},
                            ),
                        ],
                        className="column is-flex is-full px-0",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "Marker Size: ",
                                        className="column is-one-fifth",
                                        style={"fontWeight": "bold"},
                                    ),
                                    dcc.Slider(
                                        min=0.0,
                                        max=20.0,
                                        step=0.5,
                                        marks={0: "0", 20: "20"},
                                        value=DEFAULT_MARKER_SIZE,
                                        id={
                                            "index": fig_id,
                                            "key": "marker",
                                            "setting": "size",
                                        },
                                        persistence=True,
                                        persistence_type="local",
                                        className="column is-four-fifths mx-0 my-2 p-3",
                                    ),
                                ],
                                className="column is-flex is-half p-0",
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        "Marker Opacity: ",
                                        className="column is-one-fifth",
                                        style={"fontWeight": "bold"},
                                    ),
                                    dcc.Slider(
                                        min=0.0,
                                        max=1.0,
                                        step=0.05,
                                        marks={0: "0", 1: "1"},
                                        value=DEFAULT_MARKER_OPACITY,
                                        id={
                                            "index": fig_id,
                                            "key": "marker",
                                            "setting": "opacity",
                                        },
                                        persistence=True,
                                        persistence_type="local",
                                        className="column is-four-fifths mx-0 my-2 p-3",
                                    ),
                                ],
                                className="column is-flex is-half p-0",
                            ),
                        ],
                        className="column is-flex is-full",
                    ),
                ],
                className="column is-flex is-flex-wrap-wrap is-full p-0",
            )
        ],
        # Initially hidden
        className="column is-full is-flex-wrap-wrap p-0",
    )
