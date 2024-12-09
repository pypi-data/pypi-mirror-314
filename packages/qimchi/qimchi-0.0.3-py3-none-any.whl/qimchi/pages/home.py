import dash
from dash import html

from qimchi.components.notes import notes_viewer
from qimchi.components.metadata import metadata_viewer
from qimchi.components.navbar import navbar
from qimchi.components.plot_callbacks import plot_selector, plots_container
from qimchi.components.selector import data_selector

dash.register_page(__name__, path="/")
content = html.Div([plot_selector(), plots_container()], className="content p-5")


layout = html.Div(
    [
        navbar(),
        data_selector(),
        html.Div(
            [
                metadata_viewer(),
                notes_viewer(),
            ]
        ),
        content,
    ],
    **{"data-theme": "light"},
)
