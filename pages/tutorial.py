import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, register_page
from dash_ag_grid import AgGrid
from dash_bootstrap_templates import load_figure_template

load_figure_template("all")
import dash_aggrid_scales as das

medals = px.data.medals_long()

df = pd.DataFrame({"num": list(range(1, 12))})
register_page(
    __name__, title="Python tutorial for creating color scales in data tables"
)

layout = dbc.Container(
    [
        html.Br(),
        html.Br(),
        dcc.Markdown(
            """
# Tutorial

We will go through the process of creating a simple `dash-ag-grid` table, and then explore
various scales and options.

## Contents

- [Creating a simple AgGrid](#simple-aggrid)
- [Sequential color scales](#sequential)
- [Bar charts](#bar-charts)
- [Qualitative color scales](#qualitative)
- [Diverging color scales](#diverging)

"""
        ),
        html.H2("Creating a simple AgGrid", id="simple-aggrid"),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[{"field": col} for col in medals],
        ),
        dcc.Markdown("""

```python
from dash_ag_grid import AgGrid
import plotly.express as px
medals = px.data.medals_long()

AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[{"field": col} for col in medals],
),


```

"""),
        html.H2("Sequential color scales", id="sequential"),
        dcc.Markdown("""
Let's now use a sequential color scale for the "count" column


"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                }
            ],
        ),
        dcc.Markdown("""
```python
import dash_aggrid_scales as das

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
We can explore other color scales and options for the same column, and we can do them
all in the same table so we can compare:


"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                },
                {
                    "field": "count",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale="viridis"
                        )
                    },
                },
                {
                    "field": "count",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale="Gray"
                        )
                    },
                },
                {
                    "field": "count",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale="Blues_r"
                        )
                    },
                },
                {
                    "field": "count",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale="Greens"
                        )
                    },
                },
            ],
        ),
        html.Br(),
        dcc.Markdown("""

```python
AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.sequential(medals["count"])},
        },
        {
            "field": "count",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale="viridis"
                )
            },
        },
        {
            "field": "count",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale="Gray"
                )
            },
        },
        {
            "field": "count",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale="Blues_r"
                )
            },
        },
        {
            "field": "count",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale="Greens"
                )
            },
        },
    ],
),

```

### Custom number of bins

You can control how many color bins are used with the `nbins` parameter. Here we compare
different values side by side:

"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "headerName": "nbins=2",
                    "cellStyle": {
                        "styleConditions": das.sequential(medals["count"], nbins=2)
                    },
                },
                {
                    "field": "count",
                    "headerName": "nbins=4",
                    "cellStyle": {
                        "styleConditions": das.sequential(medals["count"], nbins=4)
                    },
                },
                {
                    "field": "count",
                    "headerName": "nbins=6",
                    "cellStyle": {
                        "styleConditions": das.sequential(medals["count"], nbins=6)
                    },
                },
                {
                    "field": "count",
                    "headerName": "nbins=8",
                    "cellStyle": {
                        "styleConditions": das.sequential(medals["count"], nbins=8)
                    },
                },
            ],
        ),
        dcc.Markdown("""
```python
AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "count",
            "headerName": "nbins=2",
            "cellStyle": {
                "styleConditions": das.sequential(medals["count"], nbins=2)
            },
        },
        {
            "field": "count",
            "headerName": "nbins=4",
            "cellStyle": {
                "styleConditions": das.sequential(medals["count"], nbins=4)
            },
        },
        # ... and so on
    ],
)
```

### Custom color scales

Instead of using named Plotly color scales, you can provide your own list of colors.
Colors can be CSS color names, hex codes, or `rgb()` strings:

"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "headerName": "white → blue",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale=["white", "blue"]
                        )
                    },
                },
                {
                    "field": "count",
                    "headerName": "olive → yellow → brown",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"], colorscale=["olive", "yellow", "brown"]
                        )
                    },
                },
                {
                    "field": "count",
                    "headerName": "hex colors",
                    "cellStyle": {
                        "styleConditions": das.sequential(
                            medals["count"],
                            colorscale=["#fee8c8", "#fdbb84", "#e34a33"],
                        )
                    },
                },
            ],
        ),
        dcc.Markdown("""
```python
AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "count",
            "headerName": "white → blue",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale=["white", "blue"]
                )
            },
        },
        {
            "field": "count",
            "headerName": "olive → yellow → brown",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale=["olive", "yellow", "brown"]
                )
            },
        },
        {
            "field": "count",
            "headerName": "hex colors",
            "cellStyle": {
                "styleConditions": das.sequential(
                    medals["count"], colorscale=["#fee8c8", "#fdbb84", "#e34a33"]
                )
            },
        },
    ],
)
```

"""),
        html.H2("Bar charts", id="bar-charts"),
        dcc.Markdown("""
Another options is to use bars on a certain column to convert it to a bar chart. This follows the same logic as the `sequential`
function.


"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                },
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.bar(medals["count"])},
                },
                {
                    "field": "count",
                    "cellStyle": {
                        "styleConditions": das.bar(
                            medals["count"],
                            bar_color="steelblue",
                            font_color="black",
                        )
                    },
                },
            ],
        ),
        html.Br(),
        dcc.Markdown("""
```python
 AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.sequential(medals["count"])},
        },
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.bar(medals["count"])},
        },
        {
            "field": "count",
            "cellStyle": {
                "styleConditions": das.bar(
                    medals["count"],
                    bar_color="steelblue",
                    font_color="black",
                )
            },
        },
    ],
)

```

"""),
        html.H2("Qualitative (categorical) color scales", id="qualitative"),
        dcc.Markdown("""
With categorical data we can use the `qualitative` function to visually distinguish
between the various categories, which is valuable mainly if you have a few repeated
categories in the same column.

"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "nation",
                    "cellStyle": {"styleConditions": das.qualitative(medals["nation"])},
                },
                {
                    "field": "medal",
                    "cellStyle": {
                        "styleConditions": das.qualitative(
                            medals["medal"], colorscale="Set3"
                        )
                    },
                },
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.sequential(medals["count"])},
                },
                {
                    "field": "count",
                    "cellStyle": {"styleConditions": das.bar(medals["count"])},
                },
            ],
        ),
        html.Br(),
        dcc.Markdown("""
```python
AgGrid(
    rowData=medals.to_dict("records"),
    columnDefs=[
        {
            "field": "nation",
            "cellStyle": {"styleConditions": das.qualitative(medals["nation"])},
        },
        {
            "field": "medal",
            "cellStyle": {
                "styleConditions": das.qualitative(
                    medals["medal"], colorscale="Set3"
                )
            },
        },
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.sequential(medals["count"])},
        },
        {
            "field": "count",
            "cellStyle": {"styleConditions": das.bar(medals["count"])},
        },
    ],
)
```

### Custom color scales for categories

You can provide your own list of colors for categorical data. You must provide at least
as many colors as there are unique categories — extra colors will be ignored.

"""),
        AgGrid(
            style={"height": 430},
            rowData=medals.to_dict("records"),
            columnDefs=[
                {
                    "field": "medal",
                    "headerName": "Custom colors",
                    "cellStyle": {
                        "styleConditions": das.qualitative(
                            medals["medal"], colorscale=["gold", "silver", "#cd7f32"]
                        )
                    },
                },
                {
                    "field": "nation",
                    "headerName": "Custom colors",
                    "cellStyle": {
                        "styleConditions": das.qualitative(
                            medals["nation"],
                            colorscale=["#ff6b6b", "#4ecdc4", "#45b7d1"],
                        )
                    },
                },
            ],
        ),
        dcc.Markdown("""
```python
# 3 colors for 3 medal types (Gold, Silver, Bronze)
das.qualitative(medals["medal"], colorscale=["gold", "silver", "#cd7f32"])

# 3 colors for 3 nations
das.qualitative(
    medals["nation"],
    colorscale=["#ff6b6b", "#4ecdc4", "#45b7d1"],
)
```

"""),
        html.H2("Diverging color scales", id="diverging"),
        dcc.Markdown("""
Finally, we can use a diverging color scale to show how much value in a certain column
diverge from a certain value. By default, the middle value between the maximum and the
minimum is used as the midpoint, but you can set your own midpoint as well.

"""),
        AgGrid(
            style={"height": 515},
            rowData=df.to_dict("records"),
            columnDefs=[
                {
                    "field": "num",
                    "headerName": "default",
                    "cellStyle": {"styleConditions": das.diverging(df["num"])},
                },
                {
                    "field": "num",
                    "headerName": "midpoint=3",
                    "cellStyle": {
                        "styleConditions": das.diverging(df["num"], midpoint=3)
                    },
                },
                {
                    "field": "num",
                    "headerName": "midpoint=7.4",
                    "cellStyle": {
                        "styleConditions": das.diverging(df["num"], midpoint=7.4)
                    },
                },
                {
                    "field": "num",
                    "headerName": "colorscale='BrBG'",
                    "cellStyle": {
                        "styleConditions": das.diverging(df["num"], colorscale="BrBG")
                    },
                },
            ],
        ),
        dcc.Markdown("""
```python
AgGrid(
    style={"height": 515},
    rowData=df.to_dict("records"),
    columnDefs=[
        {
            "field": "num",
            "headerName": "default",
            "cellStyle": {"styleConditions": das.diverging(df["num"])},
        },
        {
            "field": "num",
            "headerName": "midpoint=3",
            "cellStyle": {
                "styleConditions": das.diverging(df["num"], midpoint=3)
            },
        },
        {
            "field": "num",
            "headerName": "midpoint=7.4",
            "cellStyle": {
                "styleConditions": das.diverging(df["num"], midpoint=7.4)
            },
        },
        {
            "field": "num",
            "headerName": "colorscale='BrBG'",
            "cellStyle": {
                "styleConditions": das.diverging(df["num"], colorscale="BrBG")
            },
        },
    ],
)
```

This is consistent with the midpoint color behavior in Plotly's diverging colorscales in
regular charts:
"""),
        dcc.Graph(
            figure=px.scatter(
                x=list(range(1, 12)),
                y=[1 for i in range(11)],
                size=[20 for i in range(11)],
                color=list(range(1, 12)),
                color_continuous_scale="RdBu",
                height=300,
                title="Default",
                template="cosmo",
                opacity=1,
            ),
            config={"displayModeBar": False},
        ),
        dcc.Graph(
            figure=px.scatter(
                x=list(range(1, 12)),
                y=[1 for i in range(11)],
                size=[20 for i in range(11)],
                color=list(range(1, 12)),
                color_continuous_scale="RdBu",
                color_continuous_midpoint=3,
                height=300,
                title="midpoint=3",
                template="cosmo",
                opacity=1,
            ),
            config={"displayModeBar": False},
        ),
        dcc.Graph(
            figure=px.scatter(
                x=list(range(1, 12)),
                y=[1 for i in range(11)],
                size=[20 for i in range(11)],
                color=list(range(1, 12)),
                color_continuous_scale="RdBu",
                color_continuous_midpoint=7.4,
                height=300,
                title="midpoint=7.4",
                template="cosmo",
                opacity=1,
            ),
            config={"displayModeBar": False},
        ),
    ],
)
