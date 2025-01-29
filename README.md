# Dash AgGrid Scales

Plotly color scales for columns in `dash-ag-grid`

This package provides three main scales to highlight values in AgGrid columns. For consistency, the names use the same conventions use by the `plotly.colors` module:

- sequential
- qualitative
- bar

![](grid_with_color_scales.png)

## Installation

```bash
pip install dash-aggrid-scales
```

## Hello World

```python
import dash_aggrid_scales as das
from dash import Dash, html
from dash_ag_grid import AgGrid
import plotly.express as px
medals = px.data.medals_long().assign(negative=list(range(-5, 4)))

app = Dash()

app.layout = html.Div([
    AgGrid(
        rowData=medals.to_dict("records"),
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
])

if __name__ == "__main__"
    app.run(debug=True)

```