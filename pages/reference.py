import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

register_page(__name__, title="API Reference - Dash AgGrid Scales")

layout = dbc.Container(
    [
        html.Br(),
        html.Br(),
        dcc.Markdown(
            """
# API Reference

This page documents all available functions in the `dash-aggrid-scales` package.

## Contents

- [sequential](#sequential)
- [diverging](#diverging)
- [qualitative](#qualitative)
- [bar](#bar)

---

"""
        ),
        html.H2("sequential", id="sequential"),
        dcc.Markdown(
            """
```python
das.sequential(
    data,
    colorscale="cividis",
    nbins=10,
)
```

Generates style conditions for a heatmap-like styling based on numeric data.

**Parameters**

**data** : array-like
>Input data for generating color bins. Can be a list, tuple, numpy array, or pandas Series.

**colorscale** : str, list, or tuple, default `"cividis"`
>Either a Plotly Express colorscale name (e.g., `"viridis"`, `"magma"`), or a list/tuple of colors to interpolate (e.g., `["white", "blue"]`). Colors can be CSS color names, hex codes, or `"rgb(r,g,b)"` strings. Append `"_r"` to reverse the scale.

**nbins** : int, default `10`
>Number of bins to divide the data into.

**Returns**

A list of style condition dictionaries for use with `cellStyle["styleConditions"]`.

---

"""
        ),
        html.H2("diverging", id="diverging"),
        dcc.Markdown(
            """
```python
das.diverging(
    data,
    colorscale="RdBu",
    nbins=11,
    midpoint=None,
)
```

Generates style conditions using a diverging color scale based on numeric data.

**Parameters**

**data** : array-like
>Input data for generating color bins. Can be a list, tuple, numpy array, or pandas Series.

**colorscale** : str, list, or tuple, default `"RdBu"`
>Either a Plotly Express colorscale name (e.g., `"RdBu"`, `"PiYG"`), or a list/tuple of colors to interpolate (e.g., `["red", "white", "blue"]`). Colors can be CSS color names, hex codes, or `"rgb(r,g,b)"` strings. Append `"_r"` to reverse the scale.

**nbins** : int, default `11`
>Number of bins to divide the data into. Odd numbers work best for diverging scales to have a clear midpoint.

**midpoint** : float or None, default `None`
>Value to center the colorscale on. If `None`, uses the data midpoint.

**Returns**

A list of style condition dictionaries for use with `cellStyle["styleConditions"]`.

---

"""
        ),
        html.H2("qualitative", id="qualitative"),
        dcc.Markdown(
            """
```python
das.qualitative(
    data,
    colorscale="Vivid",
)
```

Generates style conditions for categorical data.

**Parameters**

**data** : array-like
>The categorical data. Can be a list, tuple, numpy array, or pandas Series.

**colorscale** : str, list, or tuple, default `"Vivid"`
>Either a Plotly Express qualitative colorscale name (e.g., `"Vivid"`, `"Pastel"`), or a list/tuple of colors (e.g., `["red", "green", "blue"]`). Colors can be CSS color names, hex codes, or `"rgb(r,g,b)"` strings. You must provide at least as many colors as there are unique categories.

**Returns**

A list of style condition dictionaries for use with `cellStyle["styleConditions"]`.

---

"""
        ),
        html.H2("bar", id="bar"),
        dcc.Markdown(
            """
```python
das.bar(
    series,
    bar_color="#efefef",
    font_color="inherit",
)
```

Generates style conditions that visualize a horizontal bar fill effect based on numeric values.
Bar widths are scaled as a percentage of the maximum value in the series.

**Parameters**

**series** : pd.Series
>Numeric data representing the values to visualize.

**bar_color** : str, default `"#efefef"`
>The color to use for the filled portion of the bar.

**font_color** : str, default `"inherit"`
>The text color used when rendering the cell contents.

**Returns**

A list of style condition dictionaries for use with `cellStyle["styleConditions"]`.

"""
        ),
    ],
)
