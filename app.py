import dash_aggrid_scales as das
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from dash_ag_grid import AgGrid
from dash_bootstrap_templates import load_figure_template

load_figure_template("all")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(external_stylesheets=[dbc.themes.FLATLY, dbc_css])

medals = px.data.medals_long().assign(negative=list(range(-5, 4)))
iris = px.data.iris()
gapminder = px.data.gapminder()

defaultColDef = {
    "filter": True,
    "filterParams": {
        "maxNumConditions": 5,
    },
}


medals_grid = AgGrid(
    rowData=medals.to_dict("records"),
    defaultColDef=defaultColDef,
    columnSize="sizeToFit",
    style={"height": 500},
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
    columnSize="sizeToFit",
    dashGridOptions={"rowHeight": 28},
    columnDefs=[
        {
            "field": "sepal_length",
            "cellStyle": {
                "styleConditions": das.sequential(iris["sepal_length"], "Viridis")
            },
        },
        {
            "field": "sepal_width",
            "cellStyle": {
                "styleConditions": das.sequential(iris["sepal_width"], "magma")
            },
        },
        {
            "field": "petal_length",
        },
        {
            "field": "petal_width",
            "cellStyle": {"styleConditions": das.bar(iris["petal_width"], "steelblue")},
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
    dashGridOptions={"rowHeight": 28},
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
            "cellStyle": {"styleConditions": das.bar(gapminder["lifeExp"], "gray")},
        },
        {
            "field": "pop",
            "cellStyle": {
                "styleConditions": das.sequential(gapminder["pop"], "cividis")
            },
        },
        {
            "field": "gdpPercap",
            "cellStyle": {
                "styleConditions": das.bar(
                    gapminder["gdpPercap"],
                    "tan",
                )
            },
        },
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

app.layout = dbc.Container(
    [
        html.Br(),
        html.Br(),
        html.Div(html.H1("Dash AgGrid Scales"), style={"textAlign": "center"}),
        html.Br(),
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        medals_grid,
                    ],
                    label="Medals grid",
                ),
                dbc.Tab(
                    [
                        iris_grid,
                    ],
                    label="Iris grid",
                ),
                dbc.Tab([gapminder_grid], label="Gapminder grid"),
                dbc.Tab([code_tab], label="Code"),
            ]
        ),
    ],
    class_name="dbc dbc-ag-grid",
)

if __name__ == "__main__":
    app.run(debug=True)
