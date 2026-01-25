import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, register_page
from dash_ag_grid import AgGrid

import dash_aggrid_scales as das

medals = px.data.medals_long()

register_page(__name__)


layout = dbc.Container(
    [
        html.Br(),
        dcc.Markdown("""

# How does the `dash-aggrid-scales` package work

"""),
        html.H2("The AgGrid object", className="mt-4"),
        dcc.Markdown("""

The minimal AgGrid object requires two basic parameters:

- `rowData`: You set this with a list of dictionaries. If you are using a DataFrame, you would convert it with `to_dict("records")`

- `columnDefs`: This can be minimally set by providing a list of dictionaries for each column: `[{"field": col_1}, {"field": col_2}, {"field": col_3}, ...]`

## The `columnDefs` attribute

This is where you define all settings for each of the columns like datatypes, header name, and many other options.

The interesting one in our case is how to set cell styles.

## The `cellStyle` attribute

For each column you can set CSS styles for each column like background color, opacity, font size, etc.

Most importantly is that we can set the style programmatically, using a set of conditions.

## The `styleConditions` key

Here is where we set conditions for background colors depending on which interval in the data range the respective cell falls.

## Example

Let's say you have a set of numbers between one and one-hundred, and we choose a color scale that has ten colors. The conditions would simply be:

```
if 1 < value <= 10: then bgcolor would take the first color in the colorscale
if 11 < value <= 20: then bgcolor would take the second color in the colorscale
if 21 < value <= 30: then bgcolor would take the third color in the colorscale
```
and so on...

## The code

Assuming we have a DataFrame `medals`, and we want to set a sequential (continuous) color scale for the column `count`:

```python
from dash_ag_grid import AgGrid
import dash_aggrid_scales as das

import plotly.express as px
medals = px.data.medals_long()

AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.sequential(medals["count"])},
        }
    ],
)
```

The result of running this code would be a list of dictionaries

```python
import dash_aggrid_scales as das
das.sequential(medals['count'])

[{'condition': 'params.value > 7.983 && params.value <= 9.6',
  'style': {'backgroundColor': '#00224e', 'color': 'white'}},
 {'condition': 'params.value > 9.6 && params.value <= 11.2',
  'style': {'backgroundColor': '#123570', 'color': 'white'}},
 {'condition': 'params.value > 11.2 && params.value <= 12.8',
  'style': {'backgroundColor': '#3b496c', 'color': 'white'}},
 {'condition': 'params.value > 12.8 && params.value <= 14.4',
  'style': {'backgroundColor': '#575d6d', 'color': 'white'}},
 {'condition': 'params.value > 14.4 && params.value <= 16.0',
  'style': {'backgroundColor': '#707173', 'color': 'white'}},
 {'condition': 'params.value > 16.0 && params.value <= 17.6',
  'style': {'backgroundColor': '#8a8678', 'color': 'inherit'}},
 {'condition': 'params.value > 17.6 && params.value <= 19.2',
  'style': {'backgroundColor': '#a59c74', 'color': 'inherit'}},
 {'condition': 'params.value > 19.2 && params.value <= 20.8',
  'style': {'backgroundColor': '#c3b369', 'color': 'inherit'}},
 {'condition': 'params.value > 20.8 && params.value <= 22.4',
  'style': {'backgroundColor': '#e1cc55', 'color': 'inherit'}},
 {'condition': 'params.value > 22.4 && params.value <= 24.0',
  'style': {'backgroundColor': '#fee838', 'color': 'inherit'}}]
```

```python
import plotly.express as px
from dash import Dash, html
from dash_ag_grid import AgGrid

import dash_aggrid_scales as das

medals = px.data.medals_long()
app = Dash()

app.layout = html.Div(
    [
        AgGrid(
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                }
            ],
        )
    ]
)

app.run()
```"""),
        AgGrid(
            rowData=medals.to_dict("records"),
            style={"height": 450},
            columnDefs=[
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                }
            ],
        ),
        # dcc.Markdown(),
    ]
)
