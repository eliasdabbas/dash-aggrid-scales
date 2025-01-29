import operator
from itertools import pairwise

import pandas as pd
import plotly.express as px

__all__ = ["sequential", "bar", "qualitative"]


def sequential(
    series: pd.Series, colorscale: str = "cividis", flip_textcolor: bool = False
) -> list:
    """
    Generates style conditions for a heatmap-like styling based on the values in a Pandas Series.

    Parameters
    ----------
    series : pd.Series
        Input data for generating color bins.
    colorscale : str, default 'cividis'
        Name of a Plotly Express colorscale. If it ends with '_r',
        the scale will reverse the midpoint logic.
    flip_textcolor : bool
        Whether or not to start with a dark/light color for text (some scales start with light colors and white text would be unreadable)

    Returns
    -------
    list of dict
        A list of style condition dictionaries, each containing:
         - 'condition': the JS condition to compare cell values.
         - 'style': a dictionary with 'backgroundColor' and 'color'.
    """

    if not flip_textcolor:
        comparator = operator.gt if colorscale.endswith("_r") else operator.lt
    else:
        comparator = operator.lt if colorscale.endswith("_r") else operator.gt

    try:
        scale = px.colors.get_colorscale(colorscale)
    except ValueError:
        raise ValueError(f"Color scale '{colorscale}' is not recognized.")

    num_bins = len(scale)
    categories = pd.cut(
        series, num_bins, include_lowest=True
    ).cat.categories.sort_values()

    midpoint = num_bins / 2.0

    styleConditions = []
    for i, cat in enumerate(categories):
        background_color = scale[i][1]
        text_color = "white" if comparator(i, midpoint) else "inherit"
        styleConditions.append(
            {
                "condition": f"params.value > {cat.left} && params.value <= {cat.right}",
                "style": {"backgroundColor": background_color, "color": text_color},
            }
        )

    return styleConditions


def qualitative(series: pd.Series, colorscale: str = "Vivid"):
    """
    Generates style conditions for categorical data in a Pandas Series.

    Parameters
    ----------
    series : pd.Series
        The categorical data.
    colorscale : str, default "Vivid"
        A key referencing a known qualitative color scale in Plotly.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each with:
         - 'condition': the JS expression for matching a cell's value
         - 'style': a dictionary specifying 'backgroundColor'
    """
    scale = getattr(px.colors.qualitative, colorscale)
    categories = series.astype("category").cat.categories
    styleConditions = []

    if len(categories) > len(scale):
        raise ValueError(
            f"You have more categories than the colors in {colorscale}, please choose a different color scale."
        )
    for i, cat in enumerate(categories):
        styleConditions.append(
            {
                "condition": f"params.value === '{cat}'",
                "style": {"backgroundColor": scale[i]},
            }
        )
    return styleConditions


def bar(series: pd.Series, bar_color: str = "#efefef", font_color: str = "inherit"):
    """
    Generates style conditions that visualize a horizontal 'bar fill' effect
    based on the value in `series`. Bar widths are scaled as a percentage
    of the maximum value in the series. Negative values are clamped to 0% fill.

    Parameters
    ----------
    series : pd.Series
        Numeric data representing the values to visualize.
    bar_color : str, optional (default: '#efefef')
        The color to use for the filled portion of the bar.
    font_color : str, optional (default: 'inherit')
        The text color used when rendering the cell contents.

    Returns
    -------
    List[Dict[str, Dict[str, str]]]
        A list of style condition dictionaries. Each dictionary has:
          - 'condition': A JS expression (as a string) that checks if
            the cell's value is between two boundaries.
          - 'style': A dictionary with CSS properties such as
            'background' and 'color'.
    """
    if series.empty:
        return [
            {
                "condition": "true",  # Always match
                "style": {"background": "white", "color": font_color},
            }
        ]

    if not pd.api.types.is_numeric_dtype(series):
        raise ValueError("Series must be numeric to use style_bar.")
    if series.lt(0).any():
        min_val = series.min()
        max_val = series.max()
        range_val = max_val - min_val
        if range_val == 0:
            return [
                {
                    "condition": "true",
                    "style": {
                        "background": f"linear-gradient(90deg, {bar_color} 0%, {bar_color} 100%)",
                        "color": font_color,
                    },
                }
            ]
        zero_pos = (0 - min_val) / range_val

        distinct_vals = series.drop_duplicates().sort_values().tolist()
        distinct_vals.insert(0, distinct_vals[0] - 1)

        styleConditions = []

        for lower, upper in pairwise(distinct_vals):
            fraction = (upper - min_val) / range_val

            start = min(zero_pos, fraction)
            end = max(zero_pos, fraction)

            start = max(0.0, min(1.0, start))
            end = max(0.0, min(1.0, end))

            start_pct = f"{start * 100:.2f}%"
            end_pct = f"{end * 100:.2f}%"

            background = (
                "linear-gradient(90deg, "
                f"white 0%, "
                f"white {start_pct}, "
                f"{bar_color} {start_pct}, "
                f"{bar_color} {end_pct}, "
                f"white {end_pct}, "
                "white 100%)"
            )

            styleConditions.append(
                {
                    "condition": f"params.value > {lower} && params.value <= {upper}",
                    "style": {"background": background, "color": font_color},
                }
            )

        return styleConditions
    else:
        max_val = series.max()

        # Handle the edge case where all values are the same or max_val == 0
        # (i.e., 0% would always occur). We'll just show full fill in that case.
        if max_val == 0:
            return [
                {
                    "condition": "true",
                    "style": {
                        "background": f"linear-gradient(90deg, {bar_color} 0%, {bar_color} 100%)",
                        "color": font_color,
                    },
                }
            ]

        # Prepare distinct cutoff points
        distinct_vals = series.drop_duplicates().sort_values().tolist()
        # Insert a value just below the smallest distinct value to define intervals
        distinct_vals.insert(0, distinct_vals[0] - 1)

        styleConditions = []

        for lower, upper in pairwise(distinct_vals):
            # Fraction of max_val (clamp to [0,1])
            fraction = upper / max_val
            fraction = max(0.0, min(1.0, fraction))

            start_pct = "0%"
            end_pct = f"{fraction * 100:.2f}%"

            background = (
                "linear-gradient(90deg, "
                f"{bar_color} {start_pct}, "
                f"{bar_color} {end_pct}, "
                f"white {end_pct}, "
                "white 100%)"
            )

            styleConditions.append(
                {
                    # Match values strictly > lower and <= upper
                    "condition": f"params.value > {lower} && params.value <= {upper}",
                    "style": {"background": background, "color": font_color},
                }
            )

        return styleConditions


def style_column(series, typ, **kwargs):
    match typ:
        case typ if typ == "sequential":
            return sequential(series, **kwargs)
        case typ if typ == "qualitative":
            return sequential(series, **kwargs)
        case typ if typ == "bar":
            return bar(series, **kwargs)
        case _:
            return None
