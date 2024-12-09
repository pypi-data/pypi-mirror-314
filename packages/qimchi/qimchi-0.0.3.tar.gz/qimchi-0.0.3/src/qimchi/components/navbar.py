from dash import html


def navbar():
    """Navbar component

    Returns:
        dash.html.Nav: Navbar component
    """
    return html.Nav(
        [
            html.Div(
                html.A(
                    html.Img(
                        src="../assets/logos/SQUAD Logo.webp",
                        alt="logo",
                        id="logo",
                        style={"maxHeight": "90%", "maxWidth": "100%"},
                    ),
                    href="https://squad-lab.org",
                    className="navbar-item",
                ),
                className="navbar-brand",
            ),
            html.Div(
                html.A("QIMCHI", href="./", className="navbar-item"),
                className="navbar-end",
            ),
        ],
        className="navbar is-transparent",
        id="navbar",
        **{"data-theme": "light"},
    )
