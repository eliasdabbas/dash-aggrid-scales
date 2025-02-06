# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "dash",
#     "dash-ag-grid",
#     "dash-aggrid-scales",
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
    external_stylesheets=[dbc.themes.COSMO, dbc_css],
    use_pages=True,
)
server = app.server
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(
            dbc.NavLink(html.B("Customize"), href="/customize"),
        ),
        dbc.NavItem(
            dbc.NavLink(
                "GitHub", href="https://github.com/eliasdabbas/dash-aggrid-scales"
            ),
        ),
    ],
    brand=html.B("Dash AgGrid Scales"),
    brand_href="/",
    color="primary",
    fluid="lg",
)


app.layout = dbc.Container(
    [navbar, page_container] + [html.Br() for i in range(20)],
    class_name="dbc dbc-ag-grid",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
