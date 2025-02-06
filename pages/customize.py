import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html, register_page
from dash.exceptions import PreventUpdate
from dash_ag_grid import AgGrid

import dash_aggrid_scales as das

iris = px.data.iris()
register_page(__name__, path="/customize")

dataTypeDefinitions = {
    "number": {
        "baseDataType": "number",
        "extendsDataType": "number",
        "columnTypes": "rightAligned",
        "appendColumnTypes": True,
    },
}


layout = dbc.Container(
    [
        html.Br(),
        html.H1("Customize your tables!"),
        dbc.Row(
            [
                dbc.Col([], lg=6, md=5, sm=12),
                dbc.Col(
                    [
                        dbc.Label("Table height:"),
                        dcc.Slider(
                            id="table_height",
                            min=300,
                            max=1200,
                            step=50,
                            value=400,
                            dots=False,
                            included=False,
                            marks=None,
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Row heights:"),
                        dcc.Slider(
                            id="row_height",
                            min=17,
                            max=55,
                            step=1,
                            value=40,
                            dots=False,
                            included=False,
                            marks=None,
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Reset table",
                            id="reset_button",
                            color="dark",
                            outline=True,
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
            ],
        ),
        AgGrid(
            id="iris_grid",
            dashGridOptions={
                "dataTypeDefinitions": dataTypeDefinitions,
                "suppressMenuHide": True,
            },
            rowData=iris.to_dict("records"),
            rowStyle={"fontFamily": "Menlo", "backgroundColor": "white"},
            columnDefs=[
                {"field": col, "filter": True, "headerName": col.lower()}
                for col in iris
            ],
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label(html.B(("Column:"))),
                        dcc.Dropdown(id="col_dropdown", options=iris.columns),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    [
                        dbc.Label(html.B(("Colorscale type:"))),
                        dcc.Dropdown(
                            id="colorscale_type",
                            options=["sequential", "qualitative", "diverging", "bar"],
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    [
                        dbc.Label(html.B(("Colorscale name:"))),
                        dcc.Dropdown(id="colorscale_name"),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    [
                        dbc.Label(html.B(("Background color:"))),
                        daq.ColorPicker(
                            id="colorpicker_bg", size=180, value={"hex": "#efefef"}
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                    id="colorpicker_bg_div",
                ),
                dbc.Col(
                    [
                        dbc.Label(html.B(("Text color:"))),
                        daq.ColorPicker(
                            id="colorpicker_text", size=180, value={"hex": "#000000"}
                        ),
                    ],
                    lg=2,
                    md=6,
                    sm=12,
                    id="colorpicker_text_div",
                ),
            ]
        ),
        html.Br(),
        html.Div(id="colorscale_swatches"),
    ]
)


@callback(
    Output("iris_grid", "style"),
    Output("iris_grid", "dashGridOptions"),
    Input("table_height", "value"),
    Input("row_height", "value"),
)
def set_table_row_heights(table_height, row_height):
    return {"height": table_height}, {"rowHeight": row_height}


@callback(
    Output("colorscale_swatches", "children"),
    Input("colorscale_type", "value"),
)
def show_swatches(colorscale_type):
    try:
        fig = getattr(px.colors, colorscale_type).swatches()
        fig.layout.margin.t = 0
        fig.layout.title.text = ""
        return html.Div(
            [
                dbc.Label(html.B("Preview color scales:")),
                dcc.Graph(figure=fig, config={"displayModeBar": False}),
            ]
        )
    except Exception:
        return ""


@callback(
    Output("colorpicker_bg_div", "style"),
    Output("colorpicker_text_div", "style"),
    Input("colorscale_type", "value"),
)
def show_hide_color_pickers(colorscale_type):
    if colorscale_type == "bar":
        return {"visibility": "visible"}, {"visibility": "visible"}
    else:
        return {"display": "none"}, {"display": "none"}


@callback(Output("colorscale_name", "options"), Input("colorscale_type", "value"))
def set_colorscale_options(colorscale_type):
    if colorscale_type is None or colorscale_type == "bar":
        raise PreventUpdate
    return dir(getattr(px.colors, colorscale_type))


@callback(
    Output("iris_grid", "columnDefs", allow_duplicate=True),
    Input("col_dropdown", "value"),
    Input("colorscale_type", "value"),
    Input("colorscale_name", "value"),
    Input("colorpicker_bg", "value"),
    Input("colorpicker_text", "value"),
    Input("iris_grid", "columnDefs"),
    prevent_initial_call=True,
)
def make_styles(
    column,
    colorscale_type,
    colorscale_name,
    colorpicker_bg,
    colorpicker_text,
    columnDefs,
):
    if colorscale_type not in ["bar"] and colorscale_name:
        for columnDef in columnDefs:
            if columnDef["field"] == column:
                columnDef["cellStyle"] = {
                    "styleConditions": getattr(das, colorscale_type)(
                        iris[column], colorscale_name
                    )
                }
        return columnDefs
    if colorscale_type in ["bar"]:
        for columnDef in columnDefs:
            if columnDef["field"] == column:
                columnDef["cellStyle"] = {
                    "styleConditions": das.bar(
                        iris[column], colorpicker_bg["hex"], colorpicker_text["hex"]
                    )
                }
        return columnDefs
    else:
        raise PreventUpdate


@callback(
    Output("iris_grid", "columnDefs", allow_duplicate=True),
    Output("colorscale_type", "value"),
    Output("iris_grid", "style", allow_duplicate=True),
    Output("iris_grid", "dashGridOptions", allow_duplicate=True),
    Output("table_height", "value"),
    Output("row_height", "value"),
    Input("reset_button", "n_clicks"),
    State("iris_grid", "columnDefs"),
    prevent_initial_call=True,
)
def reset_scales(n_clicks, columnDefs):
    if not n_clicks:
        raise PreventUpdate
    for columnDef in columnDefs:
        columnDef["cellStyle"] = {}
    return (
        columnDefs,
        None,
        {"height": 400, "backgroundColor": "white"},
        {"rowHeight": 40},
        400,
        40,
    )
