import pandas as pd
import pytest

import dash_aggrid_scales as das
from dash_aggrid_scales.scales import (
    _get_text_color,
    _make_custom_scale,
    _normalize_color,
)


class TestHelperFunctions:
    """Test helper functions used internally by scale functions."""

    def test_normalize_color_css_names(self):
        """Test CSS color name normalization."""
        assert _normalize_color("red") == "#ff0000"
        assert _normalize_color("blue") == "#0000ff"
        assert _normalize_color("gold") == "#ffd700"

    def test_normalize_color_hex(self):
        """Test hex color pass-through."""
        assert _normalize_color("#ff0000") == "#ff0000"
        assert _normalize_color("#123456") == "#123456"

    def test_normalize_color_rgb(self):
        """Test rgb color pass-through."""
        assert _normalize_color("rgb(255,0,0)") == "rgb(255,0,0)"

    def test_normalize_color_invalid(self):
        """Test invalid color raises error."""
        with pytest.raises(ValueError, match="not recognized"):
            _normalize_color("notacolor")

    def test_make_custom_scale(self):
        """Test custom color scale generation."""
        colors = _make_custom_scale(["white", "black"], num_colors=3)
        assert len(colors) == 3
        assert all(c.startswith("rgb") for c in colors)

    def test_make_custom_scale_too_few_colors(self):
        """Test error when fewer than 2 colors provided."""
        with pytest.raises(ValueError, match="at least 2 colors"):
            _make_custom_scale(["red"], num_colors=5)

    def test_get_text_color_dark_background(self):
        """Test white text on dark backgrounds."""
        assert _get_text_color("rgb(0, 0, 0)") == "white"
        assert _get_text_color("rgb(50, 50, 50)") == "white"

    def test_get_text_color_light_background(self):
        """Test inherit text on light backgrounds."""
        assert _get_text_color("rgb(255, 255, 255)") == "inherit"
        assert _get_text_color("rgb(200, 200, 200)") == "inherit"


class TestSequential:
    """Test sequential scale function."""

    def test_sequential_named_colorscale(self):
        """Test sequential with named Plotly colorscale."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = das.sequential(data, colorscale="viridis", nbins=5)

        assert len(result) == 5
        assert all("condition" in item for item in result)
        assert all("style" in item for item in result)
        assert all("backgroundColor" in item["style"] for item in result)
        assert all("color" in item["style"] for item in result)

    def test_sequential_custom_color_list(self):
        """Test sequential with custom color list."""
        data = [10, 20, 30, 40, 50]
        result = das.sequential(data, colorscale=["white", "blue"], nbins=3)

        assert len(result) == 3
        assert all(
            item["style"]["backgroundColor"].startswith("rgb") for item in result
        )

    def test_sequential_different_input_types(self):
        """Test sequential with list, tuple, and Series."""
        data_list = [1, 2, 3, 4, 5]
        data_tuple = (1, 2, 3, 4, 5)
        data_series = pd.Series([1, 2, 3, 4, 5])

        result_list = das.sequential(data_list, nbins=3)
        result_tuple = das.sequential(data_tuple, nbins=3)
        result_series = das.sequential(data_series, nbins=3)

        assert len(result_list) == len(result_tuple) == len(result_series) == 3

    def test_sequential_condition_format(self):
        """Test that conditions have proper format."""
        data = [1, 5, 10]
        result = das.sequential(data, nbins=2)

        for item in result:
            assert "params.value >" in item["condition"]
            assert "&&" in item["condition"]
            assert "<=" in item["condition"]

    def test_sequential_invalid_colorscale(self):
        """Test error with invalid colorscale name."""
        data = [1, 2, 3]
        with pytest.raises(ValueError, match="not recognized"):
            das.sequential(data, colorscale="notacolorscale")

    def test_sequential_text_color_contrast(self):
        """Test that text color is set for contrast."""
        data = [1, 2, 3, 4, 5]
        result = das.sequential(data, nbins=3)

        for item in result:
            assert item["style"]["color"] in ["white", "inherit"]


class TestQualitative:
    """Test qualitative scale function."""

    def test_qualitative_named_colorscale(self):
        """Test qualitative with named Plotly colorscale."""
        data = ["A", "B", "C", "A", "B", "C"]
        result = das.qualitative(data, colorscale="Vivid")

        assert len(result) == 3  # 3 unique categories
        assert all("condition" in item for item in result)
        assert all("style" in item for item in result)

    def test_qualitative_custom_color_list(self):
        """Test qualitative with custom color list."""
        data = ["gold", "silver", "bronze"]
        result = das.qualitative(data, colorscale=["#FFD700", "#C0C0C0", "#cd7f32"])

        assert len(result) == 3
        assert all(item["style"]["backgroundColor"].startswith("#") for item in result)

    def test_qualitative_dict_valid_mapping(self):
        """Test qualitative with dict mapping all categories."""
        data = ["usa", "canada", "mexico", "usa", "canada"]
        color_map = {"usa": "green", "canada": "blue", "mexico": "yellow"}
        result = das.qualitative(data, colorscale=color_map)

        assert len(result) == 3

        conditions = {
            item["condition"]: item["style"]["backgroundColor"] for item in result
        }
        assert conditions["params.value === 'usa'"] == "#008000"
        assert conditions["params.value === 'canada'"] == "#0000ff"
        assert conditions["params.value === 'mexico'"] == "#ffff00"

    def test_qualitative_dict_missing_categories(self):
        """Test qualitative dict with missing categories raises error."""
        data = ["usa", "canada", "mexico"]
        color_map = {"usa": "green", "canada": "blue"}  # missing mexico

        with pytest.raises(ValueError, match="missing from the color mapping"):
            das.qualitative(data, colorscale=color_map)

    def test_qualitative_dict_extra_keys(self):
        """Test qualitative dict with extra keys works fine."""
        data = ["usa", "canada"]
        color_map = {
            "usa": "green",
            "canada": "blue",
            "mexico": "yellow",
            "brazil": "red",
        }
        result = das.qualitative(data, colorscale=color_map)

        assert len(result) == 2

    def test_qualitative_dict_case_sensitive(self):
        """Test qualitative dict is case-sensitive."""
        data = ["USA", "Canada"]
        color_map = {"usa": "green", "canada": "blue"}

        with pytest.raises(ValueError, match="missing from the color mapping"):
            das.qualitative(data, colorscale=color_map)

    def test_qualitative_numeric_categories(self):
        """Test qualitative with numeric categories."""
        data = [1, 2, 3, 1, 2, 3]
        result = das.qualitative(data, colorscale=["red", "green", "blue"])

        assert len(result) == 3
        assert any("params.value === 1" in item["condition"] for item in result)

    def test_qualitative_insufficient_colors_list(self):
        """Test error when color list has fewer colors than categories."""
        data = ["A", "B", "C", "D"]
        with pytest.raises(ValueError, match="4 categories but provided only 2 colors"):
            das.qualitative(data, colorscale=["red", "blue"])

    def test_qualitative_invalid_named_scale(self):
        """Test error with invalid named colorscale."""
        data = ["A", "B", "C"]
        with pytest.raises(ValueError, match="not recognized"):
            das.qualitative(data, colorscale="NotAScale")

    def test_qualitative_different_input_types(self):
        """Test qualitative with list, tuple, and Series."""
        data_list = ["A", "B", "C"]
        data_tuple = ("A", "B", "C")
        data_series = pd.Series(["A", "B", "C"])

        result_list = das.qualitative(data_list)
        result_tuple = das.qualitative(data_tuple)
        result_series = das.qualitative(data_series)

        assert len(result_list) == len(result_tuple) == len(result_series) == 3

    def test_qualitative_text_color_contrast(self):
        """Test that text color is appropriate for contrast."""
        data = ["A", "B", "C"]
        result = das.qualitative(data, colorscale=["black", "white", "red"])

        for item in result:
            assert item["style"]["color"] in ["white", "inherit"]


class TestDiverging:
    """Test diverging scale function."""

    def test_diverging_named_colorscale(self):
        """Test diverging with named Plotly colorscale."""
        data = [-10, -5, 0, 5, 10]
        result = das.diverging(data, colorscale="RdBu", nbins=5)

        assert len(result) == 5
        assert all("condition" in item for item in result)
        assert all("style" in item for item in result)

    def test_diverging_custom_color_list(self):
        """Test diverging with custom color list."""
        data = [-5, -2, 0, 2, 5]
        result = das.diverging(data, colorscale=["red", "white", "blue"], nbins=3)

        assert len(result) == 3
        assert all(
            item["style"]["backgroundColor"].startswith("rgb") for item in result
        )

    def test_diverging_default_midpoint(self):
        """Test diverging uses data midpoint by default."""
        data = [0, 10, 20, 30, 40]
        result = das.diverging(data, nbins=5)

        assert len(result) == 5

    def test_diverging_custom_midpoint(self):
        """Test diverging with custom midpoint."""
        data = [0, 5, 10, 15, 20]
        result = das.diverging(data, nbins=5, midpoint=10)

        assert len(result) == 5

    def test_diverging_odd_nbins(self):
        """Test diverging works best with odd nbins."""
        data = [-10, -5, 0, 5, 10]
        result = das.diverging(data, nbins=11)

        assert len(result) == 11

    def test_diverging_different_input_types(self):
        """Test diverging with list, tuple, and Series."""
        data_list = [-5, 0, 5]
        data_tuple = (-5, 0, 5)
        data_series = pd.Series([-5, 0, 5])

        result_list = das.diverging(data_list, nbins=3)
        result_tuple = das.diverging(data_tuple, nbins=3)
        result_series = das.diverging(data_series, nbins=3)

        assert len(result_list) == len(result_tuple) == len(result_series) == 3

    def test_diverging_condition_format(self):
        """Test that conditions have proper format."""
        data = [-5, 0, 5]
        result = das.diverging(data, nbins=3)

        for item in result:
            assert "params.value >" in item["condition"]
            assert "&&" in item["condition"]
            assert "<=" in item["condition"]

    def test_diverging_invalid_colorscale(self):
        """Test error with invalid colorscale name."""
        data = [-5, 0, 5]
        with pytest.raises(ValueError, match="not recognized"):
            das.diverging(data, colorscale="notacolorscale")

    def test_diverging_text_color_contrast(self):
        """Test that text color is set for contrast."""
        data = [-5, 0, 5]
        result = das.diverging(data, nbins=3)

        for item in result:
            assert item["style"]["color"] in ["white", "inherit"]


class TestBar:
    """Test bar scale function."""

    def test_bar_positive_values(self):
        """Test bar with positive values only."""
        data = pd.Series([10, 20, 30, 40, 50])
        result = das.bar(data)

        assert len(result) == 5
        assert all("condition" in item for item in result)
        assert all("style" in item for item in result)
        assert all("background" in item["style"] for item in result)
        assert all("linear-gradient" in item["style"]["background"] for item in result)

    def test_bar_negative_values(self):
        """Test bar with negative values only."""
        data = pd.Series([-50, -40, -30, -20, -10])
        result = das.bar(data)

        assert len(result) == 5
        assert all("linear-gradient" in item["style"]["background"] for item in result)

    def test_bar_mixed_values(self):
        """Test bar with both positive and negative values."""
        data = pd.Series([-20, -10, 0, 10, 20])
        result = das.bar(data)

        assert len(result) == 5
        # Should have gradients that handle both sides of zero

    def test_bar_all_zeros(self):
        """Test bar with all zero values."""
        data = pd.Series([0, 0, 0])
        result = das.bar(data)

        assert len(result) == 1
        assert result[0]["condition"] == "true"

    def test_bar_all_same_values(self):
        """Test bar with all same non-zero values."""
        data = pd.Series([5, 5, 5, 5])
        result = das.bar(data)

        assert len(result) == 1
        assert "100%" in result[0]["style"]["background"]

    def test_bar_empty_series(self):
        """Test bar with empty series."""
        data = pd.Series([], dtype=float)
        result = das.bar(data)

        assert len(result) == 1
        assert result[0]["condition"] == "true"
        assert result[0]["style"]["background"] == "white"

    def test_bar_custom_colors(self):
        """Test bar with custom bar and font colors."""
        data = pd.Series([10, 20, 30])
        result = das.bar(data, bar_color="#ff0000", font_color="#000000")

        assert all("#ff0000" in item["style"]["background"] for item in result)
        assert all(item["style"]["color"] == "#000000" for item in result)

    def test_bar_condition_format(self):
        """Test that conditions have proper format."""
        data = pd.Series([10, 20, 30])
        result = das.bar(data)

        for item in result:
            assert "params.value >" in item["condition"]
            assert "&&" in item["condition"]
            assert "<=" in item["condition"]

    def test_bar_non_numeric_error(self):
        """Test error when series is not numeric."""
        data = pd.Series(["a", "b", "c"])

        with pytest.raises(ValueError, match="must be numeric"):
            das.bar(data)

    def test_bar_gradient_percentages(self):
        """Test that gradients contain percentage values."""
        data = pd.Series([25, 50, 75, 100])
        result = das.bar(data)

        for item in result:
            # Should contain percentage values in gradient
            assert "%" in item["style"]["background"]

    def test_bar_max_value_full_fill(self):
        """Test that maximum value gets 100% fill."""
        data = pd.Series([10, 50, 100])
        result = das.bar(data)

        # Last result should be for max value (100)
        max_result = result[-1]
        assert (
            "100.00%" in max_result["style"]["background"]
            or "100%" in max_result["style"]["background"]
        )
