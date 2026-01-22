import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, dcc, html, page_container
from dash_ag_grid import AgGrid
from dash_bootstrap_templates import load_figure_template

import dash_aggrid_scales as das

load_figure_template("all")

primary = "#2C3E50"

dash.register_page(__name__, path="/")

medals = px.data.medals_long().assign(negative=list(range(-5, 4)))
iris = px.data.iris()
gapminder = px.data.gapminder()
stocks = px.data.stocks()
stock_changes = stock_changes = px.data.stocks().iloc[:, 1:].melt()["value"]

defaultColDef = {
    "filter": True,
    "filterParams": {
        "maxNumConditions": 5,
    },
}

dataTypeDefinitions = {
    "number": {
        "baseDataType": "number",
        "extendsDataType": "number",
        "columnTypes": "rightAligned",
        "appendColumnTypes": True,
    }
}


medals_grid = AgGrid(
    rowData=medals.to_dict("records"),
    defaultColDef=defaultColDef,
    columnSize="responsiveSizeToFit",
    style={"height": 450},
    columnDefs=[
        {
            "field": "nation",
            "headerName": "nation (qualitative)",
            "cellStyle": {"styleConditions": das.qualitative(medals["nation"])},
        },
        {
            "field": "medal",
            "headerName": "medal (qualitative)",
            "cellStyle": {"styleConditions": das.qualitative(medals["medal"], "Safe")},
        },
        {
            "field": "count",
            "headerName": "count (sequential)",
            "cellStyle": {"styleConditions": das.sequential(medals["count"])},
        },
        {
            "field": "count",
            "headerName": "count (bar)",
            "cellStyle": {"styleConditions": das.bar(medals["count"])},
        },
        {
            "field": "negative",
            "headerName": "random +ve & -ve values (bar)",
            "cellStyle": {"styleConditions": das.bar(medals["negative"], "teal")},
        },
    ],
)


iris_grid = AgGrid(
    rowData=iris.to_dict("records"),
    defaultColDef=defaultColDef,
    style={"height": 700},
    rowStyle={"fontFamily": "Menlo"},
    columnSize="responsiveSizeToFit",
    dashGridOptions={"rowHeight": 28, "dataTypeDefinitions": dataTypeDefinitions},
    columnDefs=[
        {
            "field": "sepal_length",
            "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
            "cellStyle": {"styleConditions": das.sequential(iris["sepal_length"])},
        },
        {
            "field": "sepal_width",
            "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
            "cellStyle": {
                "styleConditions": das.sequential(iris["sepal_width"], "magma")
            },
        },
        {
            "field": "petal_length",
        },
        {
            "field": "petal_width",
            "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
            "cellStyle": {"styleConditions": das.bar(iris["petal_width"], "skyblue")},
        },
        {
            "field": "species",
            "cellStyle": {
                "styleConditions": das.qualitative(iris["species"], "Plotly")
            },
        },
    ],
)

gapminder_grid = AgGrid(
    rowData=gapminder.to_dict("records"),
    style={"height": 700},
    rowStyle={"fontFamily": "Menlo"},
    columnSize="responsiveSizeToFit",
    dashGridOptions={"rowHeight": 28, "dataTypeDefinitions": dataTypeDefinitions},
    defaultColDef=defaultColDef,
    columnDefs=[
        {
            "field": "country",
        },
        {
            "field": "continent",
            "cellStyle": {"styleConditions": das.qualitative(gapminder["continent"])},
        },
        {
            "field": "year",
            "cellStyle": {
                "styleConditions": das.sequential(gapminder["year"], "Plotly3")
            },
        },
        {
            "field": "lifeExp",
            "valueFormatter": {"function": "d3.format('.1f')(params.value)"},
            "cellStyle": {
                "styleConditions": das.bar(gapminder["lifeExp"], "lightgray")
            },
        },
        {
            "field": "pop",
            "valueFormatter": {"function": "d3.format('>.3s')(params.value)"},
            "cellStyle": {
                "styleConditions": das.sequential(gapminder["pop"], "cividis")
            },
        },
        {
            "field": "gdpPercap",
            "valueFormatter": {"function": "d3.format('.2s')(params.value)"},
            "cellStyle": {
                "styleConditions": das.bar(
                    gapminder["gdpPercap"],
                    "tan",
                )
            },
        },
    ],
)

stocks_grid = AgGrid(
    rowData=stocks.to_dict("records"),
    defaultColDef=defaultColDef,
    columnSize="responsiveSizeToFit",
    rowStyle={"font-size": "0.75rem"},
    dashGridOptions={"rowHeight": 20},
    style={"height": 650},
    columnDefs=[
        {
            "field": "date",
        }
    ]
    + [
        {
            "field": col,
            "valueFormatter": {"function": "d3.format(',.2%')(params.value)"},
            "cellStyle": {
                "styleConditions": das.diverging(stock_changes, "RdBu", midpoint=1)
            },
        }
        for col in stocks.columns[1:]
    ],
)


code_tab = html.Div(
    [
        dcc.Markdown(
            """
### Installation

```bash
pip install dash-aggrid-scales
```

### Create a sequential scale

This create a set of rules for each of the (typically 9) colors of the chosen scale.
If the value is in the first 11% of the data assign the first color as its background color 
If the value is in the second 11% of the data assign the second color as its background color 
...


```python
import dash_aggrid_scales as das
import pandas as pd
s = pd.Series([1, 2, 3, 4, 5])
das.sequential(s)
```

```bash
[{'condition': 'params.value > 0.995 && params.value <= 1.4',
  'style': {'backgroundColor': '#00224e', 'color': 'white'}},
 {'condition': 'params.value > 1.4 && params.value <= 1.8',
  'style': {'backgroundColor': '#123570', 'color': 'white'}},
 {'condition': 'params.value > 1.8 && params.value <= 2.2',
  'style': {'backgroundColor': '#3b496c', 'color': 'white'}},
 {'condition': 'params.value > 2.2 && params.value <= 2.6',
  'style': {'backgroundColor': '#575d6d', 'color': 'white'}},
 {'condition': 'params.value > 2.6 && params.value <= 3.0',
  'style': {'backgroundColor': '#707173', 'color': 'white'}},
 {'condition': 'params.value > 3.0 && params.value <= 3.4',
  'style': {'backgroundColor': '#8a8678', 'color': 'inherit'}},
 {'condition': 'params.value > 3.4 && params.value <= 3.8',
  'style': {'backgroundColor': '#a59c74', 'color': 'inherit'}},
 {'condition': 'params.value > 3.8 && params.value <= 4.2',
  'style': {'backgroundColor': '#c3b369', 'color': 'inherit'}},
 {'condition': 'params.value > 4.2 && params.value <= 4.6',
  'style': {'backgroundColor': '#e1cc55', 'color': 'inherit'}},
 {'condition': 'params.value > 4.6 && params.value <= 5.0',
  'style': {'backgroundColor': '#fee838', 'color': 'inherit'}}]
```
"""
        )
    ]
)


nav = dbc.Nav(
    [
        html.Br(),
        dbc.NavItem(html.H4("Tutorials")),
        html.Ul([dbc.NavLink("Tutorial 1")]),
        dbc.NavItem(html.H4("How-to Guides")),
        dbc.NavItem(html.H4("Reference")),
        dbc.NavItem(html.H4("Explanations")),
    ],
    vertical=True,
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                # dbc.Col(nav, lg=2),
                dbc.Col(lg=1),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.Div(
                            [
                                html.H1(
                                    html.Code("Dash AgGrid Scales"),
                                    style={"textAlign": "center", "color": primary},
                                ),
                                dcc.Markdown(
                                    [
                                        """

A Python package that enables setting color scales for columns in a `dash-ag-grid` table.

All Plotly color scales are provided and can be used as:

- `sequential`: For providing a continuous color scales as a background gradient for cells in the desired column.
- `qualitative`: For categorical color scales to distinguish between unique (repeated) values in a column.
- `diverging`: Another variation of continuous color scales but used to show how much values diverge from a certain value. The `midpoint` value can be zero for example, to show positive/negative values, or could be an average or target value.
- `bar`: Provides bars to make columns like bar charts.

## Installation

```bash
pip install dash-aggrid-scales
```


## Examples

"""
                                    ]
                                ),
                            ],
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    [
                                        medals_grid,
                                        html.Br(),
                                        html.Br(),
                                        html.H2("Without scales:"),
                                        html.Br(),
                                        AgGrid(
                                            rowData=medals.to_dict("records"),
                                            style={"height": 450},
                                            columnDefs=[
                                                {"field": col} for col in medals
                                            ],
                                            columnSize="sizeToFit",
                                        ),
                                    ],
                                    label="Medals grid",
                                    label_style={
                                        "color": primary,
                                        "fontWeight": "bold",
                                    },
                                ),
                                dbc.Tab(
                                    [
                                        iris_grid,
                                        html.Br(),
                                        html.Br(),
                                        html.H2("Without scales:"),
                                        html.Br(),
                                        AgGrid(
                                            rowData=iris.to_dict("records"),
                                            style={"height": 700},
                                            columnDefs=[{"field": col} for col in iris],
                                            columnSize="sizeToFit",
                                        ),
                                    ],
                                    label="Iris grid",
                                    label_style={
                                        "color": primary,
                                        "fontWeight": "bold",
                                    },
                                ),
                                dbc.Tab(
                                    [
                                        gapminder_grid,
                                        html.Br(),
                                        html.Br(),
                                        html.H2("Without scales:"),
                                        html.Br(),
                                        AgGrid(
                                            rowData=gapminder.to_dict("records"),
                                            style={"height": 700},
                                            columnDefs=[
                                                {"field": col}
                                                for col in gapminder.columns[:6]
                                            ],
                                            columnSize="sizeToFit",
                                        ),
                                    ],
                                    label="Gapminder grid",
                                    label_style={
                                        "color": primary,
                                        "fontWeight": "bold",
                                    },
                                ),
                                dbc.Tab(
                                    stocks_grid,
                                    label="Stocks",
                                    label_style={
                                        "color": primary,
                                        "fontWeight": "bold",
                                    },
                                ),
                                # dbc.Tab([code_tab], label="Code"),
                            ]
                        ),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        dcc.Markdown("""## Usage

The `AgGrid` component accepts a `columnDefs` parameter to set specific definitions per column.

```python
from dash-ag-grid import AgGrid

AgGrid(
    rowData=df.to_dict("records"),
    columnDefs=[
        {
            "field": "column name",
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": "params.value > 10 && params.value <= 20",
                        "style": {"backgroundColor": "#00224e", "color": "white"},
                    },
                    {
                        "condition": "params.value > 20 && params.value <= 30",
                        "style": {"backgroundColor": "#123570", "color": "white"},
                    },
                    {
                        "condition": "params.value > 30 && params.value <= 40",
                        "style": {"backgroundColor": "#3b496c", "color": "white"},
                    },
                ]
            },
        },
    ],
)

```

The above code sets a bunch of style conditions. If a value falls between 10 and 20, give it this background color, and this font color, and so on for all mentioned intervals.

This package automates this process so you don't have to create all those conditions manually and worry about the exact color selections.

You simply provide the function corresponding to the scale type you want, and provide any of the optinal parameters like the scale name.

```python
import dash-aggrid-scales as das
das.sequential(df["column_a"])
```

This will produce the required list of conditions that you can feed into the `AgGrid` definition.
"""),
                    ],
                    lg=10,
                ),
            ]
        ),
    ],
    class_name="dbc dbc-ag-grid",
    fluid=True,
)
