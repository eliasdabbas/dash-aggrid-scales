# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "dash",
#     "dash-ag-grid",
#     "dash-aggrid-scales>=0.3.0",
#     "dash-bootstrap-components",
#     "dash-bootstrap-templates",
#     "dash-daq",
#     "gunicorn",
# ]
# ///

import dash_bootstrap_components as dbc
from dash import Dash, html, page_container

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    external_stylesheets=[dbc.themes.COSMO, dbc_css, dbc.icons.BOOTSTRAP],
    title="Python package for colors scales in data tables - Dash AgGrid Scales",
    use_pages=True,
)
server = app.server
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(
            dbc.NavLink(
                "Tutorial",
                style={"fontSize": "19pt"},
                href="/tutorial",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Reference",
                style={"fontSize": "19pt"},
                href="/reference",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(dbc.Button("Customize", color="warning"), href="/customize"),
        ),
        dbc.NavItem(
            dbc.NavLink(
                html.I(className="bi bi-github", style={"fontSize": "23pt"}),
                href="https://github.com/eliasdabbas/dash-aggrid-scales",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                html.Img(src="assets/plotly_community_logo.png", width=43),
                href="https://community.plotly.com/u/eliasdabbas/summary",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                html.I(className="bi bi-linkedin", style={"fontSize": "23pt"}),
                href="https://www.linkedin.com/in/eliasdabbas/",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                html.I(className="bi bi-twitter", style={"fontSize": "23pt"}),
                href="https://x.com/eliasdabbas",
            )
        ),
    ],
    brand=html.B("Dash AgGrid Scales"),
    brand_href="/",
    color="light",
    dark=False,
    fluid="lg",
)


app.layout = dbc.Container(
    [navbar, page_container] + [html.Br() for i in range(20)],
    class_name="dbc dbc-ag-grid",
    fluid=True,
    style={"fontSize": "1.23rem"},
)

if __name__ == "__main__":
    app.run(debug=True)
