from collections.abc import Sequence
from itertools import pairwise
from typing import Union

import pandas as pd
import plotly.express as px

__all__ = ["sequential", "bar", "qualitative", "diverging"]


ArrayLike = Union[pd.Series, Sequence]


_CSS_COLORS = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}


def _normalize_color(color: str) -> str:
    """
    Convert a color string to a format suitable for Plotly interpolation.

    Named CSS colors are converted to hex. Hex and rgb formats pass through.
    Raises ValueError for unrecognized color formats.

    Parameters
    ----------
    color : str
        A color string (CSS name, hex, or rgb format).

    Returns
    -------
    str
        The color in hex or rgb format.

    Raises
    ------
    ValueError
        If the color is not a recognized CSS name or valid hex/rgb format.
    """
    c = color.lower().strip()
    if c in _CSS_COLORS:
        return _CSS_COLORS[c]
    if c.startswith("#") or c.startswith("rgb"):
        return color
    raise ValueError(
        f"Color '{color}' is not recognized. "
        "Use a valid CSS color name, hex (e.g., '#ff0000'), or rgb (e.g., 'rgb(255,0,0)') format."
    )


def _make_custom_scale(colors: list, num_colors: int = 10) -> list:
    """
    Generate a list of interpolated colors from a list of color stops.

    Parameters
    ----------
    colors : list
        List of colors (CSS names, hex, or rgb format). Must contain at least 2 colors.
    num_colors : int, default 10
        Number of evenly-spaced colors to generate.

    Returns
    -------
    list of str
        List of rgb color strings, e.g., ['rgb(255,255,255)', 'rgb(0,0,255)', ...]

    Raises
    ------
    ValueError
        If fewer than 2 colors are provided or if any color is invalid.
    """
    if len(colors) < 2:
        raise ValueError("Must provide at least 2 colors for interpolation.")

    normalized = [_normalize_color(c) for c in colors]
    base_scale = [[i / (len(normalized) - 1), c] for i, c in enumerate(normalized)]

    return px.colors.sample_colorscale(base_scale, num_colors, colortype="rgb")


def _get_text_color(rgb_color: str) -> str:
    """
    Determine appropriate text color (white or inherit) based on background luminance.

    Uses WCAG relative luminance formula to ensure readable contrast.
    Returns 'white' for dark backgrounds (luminance < 0.179) and 'inherit' for light.

    Parameters
    ----------
    rgb_color : str
        Background color in 'rgb(r, g, b)' format.

    Returns
    -------
    str
        'white' for dark backgrounds, 'inherit' for light backgrounds.
    """
    rgb_tuple = px.colors.unlabel_rgb(rgb_color)
    r, g, b = rgb_tuple[0] / 255, rgb_tuple[1] / 255, rgb_tuple[2] / 255

    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # Calculate relative luminance (human eye is most sensitive to green)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # WCAG threshold: dark backgrounds need white text
    return "white" if luminance < 0.179 else "inherit"


def sequential(
    data: ArrayLike,
    colorscale: str | list[str] | tuple[str, ...] = "cividis",
    nbins: int = 10,
):
    """
    Generates style conditions for a heatmap-like styling based on numeric data.

    Parameters
    ----------
    data : array-like
        Input data for generating color bins. Can be a list, tuple,
        numpy array, or pandas Series.
    colorscale : str, list of str, or tuple of str, default 'cividis'
        Either a Plotly Express colorscale name (e.g., 'viridis', 'magma'),
        or a list/tuple of colors to interpolate (e.g., ['white', 'blue']).
        Colors can be CSS color names, hex codes, or 'rgb(r,g,b)' strings.
        If it ends with '_r', the scale will be reversed.
    nbins : int, default 10
        Number of bins to divide the data into.

    Returns
    -------
    list of dict
        A list of style condition dictionaries, each containing:
         - 'condition': the JS condition to compare cell values.
         - 'style': a dictionary with 'backgroundColor' and 'color'.
    """
    if isinstance(colorscale, (list, tuple)):
        colors = _make_custom_scale(colorscale, nbins)
    else:
        try:
            base_scale = px.colors.get_colorscale(colorscale)
        except ValueError:
            raise ValueError(f"Color scale '{colorscale}' is not recognized.")
        colors = px.colors.sample_colorscale(base_scale, nbins, colortype="rgb")

    series = pd.Series(data)
    categories = pd.cut(series, nbins, include_lowest=True).cat.categories.sort_values()

    styleConditions = []
    for i, cat in enumerate(categories):
        background_color = colors[i]
        text_color = _get_text_color(background_color)
        styleConditions.append(
            {
                "condition": f"params.value > {cat.left} && params.value <= {cat.right}",
                "style": {"backgroundColor": background_color, "color": text_color},
            }
        )

    return styleConditions


def diverging(
    data: ArrayLike,
    colorscale: str | list[str] | tuple[str, ...] = "RdBu",
    nbins: int = 11,
    midpoint=None,
):
    """
    Generates style conditions using a diverging color scale based on numeric data.

    Parameters
    ----------
    data : array-like
        Input data for generating color bins. Can be a list, tuple,
        numpy array, or pandas Series.
    colorscale : str, list of str, or tuple of str, default 'RdBu'
        Either a Plotly Express colorscale name (e.g., 'RdBu', 'PiYG'),
        or a list/tuple of colors to interpolate (e.g., ['red', 'white', 'blue']).
        Colors can be CSS color names, hex codes, or 'rgb(r,g,b)' strings.
        If it ends with '_r', the scale will be reversed.
    nbins : int, default 11
        Number of bins to divide the data into. Odd numbers work best
        for diverging scales to have a clear midpoint.
    midpoint : float, optional
        Value to center the colorscale on. If None, uses the data midpoint.

    Returns
    -------
    list of dict
        A list of style condition dictionaries, each containing:
         - 'condition': the JS condition to compare cell values.
         - 'style': a dictionary with 'backgroundColor' and 'color'.
    """
    if isinstance(colorscale, (list, tuple)):
        colors = _make_custom_scale(colorscale, nbins)
    else:
        try:
            base_scale = px.colors.get_colorscale(colorscale)
        except ValueError:
            raise ValueError(f"Color scale '{colorscale}' is not recognized.")
        colors = px.colors.sample_colorscale(base_scale, nbins, colortype="rgb")

    series = pd.Series(data)
    mid_value = series.min() + ((series.max() - series.min()) / 2)
    if midpoint is not None:
        if midpoint <= mid_value:
            newval = midpoint - (series.max() - midpoint)
        else:
            newval = midpoint + (midpoint - series.min())
        series = pd.concat([series, pd.Series([newval])])
    categories = pd.cut(series, nbins, include_lowest=True).cat.categories.sort_values()

    styleConditions = []
    for i, cat in enumerate(categories):
        background_color = colors[i]
        text_color = _get_text_color(background_color)
        styleConditions.append(
            {
                "condition": f"params.value > {cat.left} && params.value <= {cat.right}",
                "style": {"backgroundColor": background_color, "color": text_color},
            }
        )
    return styleConditions


def qualitative(
    data: ArrayLike,
    colorscale: str | list[str] | tuple[str, ...] = "Vivid",
):
    """
    Generates style conditions for categorical data.

    Parameters
    ----------
    data : array-like
        The categorical data. Can be a list, tuple, numpy array, or pandas Series.
    colorscale : str, list of str, or tuple of str, default 'Vivid'
        Either a Plotly Express qualitative colorscale name (e.g., 'Vivid', 'Pastel'),
        or a list/tuple of colors (e.g., ['red', 'green', 'blue']).
        Colors can be CSS color names, hex codes, or 'rgb(r,g,b)' strings.

    Returns
    -------
    list of dict
        A list of dictionaries, each with:
         - 'condition': the JS expression for matching a cell's value
         - 'style': a dictionary specifying 'backgroundColor' and 'color'
    """
    if isinstance(colorscale, (list, tuple)):
        colors = [_normalize_color(c) for c in colorscale]
    else:
        colors = getattr(px.colors.qualitative, colorscale, None)
        if colors is None:
            raise ValueError(
                f"Qualitative color scale '{colorscale}' is not recognized."
            )

    series = pd.Series(data)
    categories = series.astype("category").cat.categories
    styleConditions = []

    if isinstance(colorscale, (list, tuple)):
        if len(categories) > len(colors):
            raise ValueError(
                f"You have {len(categories)} categories but provided only {len(colors)} colors. "
                "When using a custom color list, you must provide at least as many colors as categories."
            )
    elif len(categories) > len(colors):
        raise ValueError(
            f"You have {len(categories)} categories but '{colorscale}' only has {len(colors)} colors. "
            "Please provide more colors or choose a different color scale."
        )

    for i, cat in enumerate(categories):
        color = colors[i]
        if color.startswith("#"):
            rgb_tuple = px.colors.hex_to_rgb(color)
            rgb_color = f"rgb({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]})"
        elif color.startswith("rgb"):
            rgb_color = color
        else:
            rgb_color = color

        text_color = (
            _get_text_color(rgb_color) if color.startswith(("#", "rgb")) else "inherit"
        )
        styleConditions.append(
            {
                "condition": f"params.value === '{cat}'"
                if isinstance(cat, str)
                else f"params.value === {cat}",
                "style": {"backgroundColor": color, "color": text_color},
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
