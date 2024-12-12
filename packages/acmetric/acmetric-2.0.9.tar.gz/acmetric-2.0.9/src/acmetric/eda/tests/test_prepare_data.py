"""Tests for the prepare_data module."""

import pandas as pd
import pytest

from acmetric.eda.utils.prepare_data import (
    convert_vertical_data_alignment_to_horizontal,
    determine_columns_to_include,
    get_data_subset,
    unstack_dataframe,
    validate_columns_exist,
    validate_missing_keys,
)
from acmetric.logger import Logger

logger = Logger()


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture providing sample data for testing."""
    return pd.DataFrame(
        {
            "entity": ["A", "A", "B", "B"],
            "value": [10, 15, 20, 25],
            "time": [1, 2, 1, 2],
        }
    )


@pytest.fixture
def sample_settings() -> dict:
    """Fixture providing sample settings for testing."""
    return {
        "data_structure": {
            "type": "vertical",
            "time_series": {
                "entity_column": "entity",
                "value_column": "value",
                "time_column": "time",
            },
        }
    }


@pytest.fixture
def required_keys() -> list[str]:
    """Fixture providing required keys for testing."""
    return ["entity_column", "value_column", "time_column"]


def test_unstack_data_with_vertical_data(
    sample_data: pd.DataFrame, sample_settings: dict, required_keys: list[str]
) -> None:
    """Test convert_vertical_data_alignment_to_horizontal function with vertical data."""
    result = convert_vertical_data_alignment_to_horizontal(
        sample_data, sample_settings, required_keys
    )
    expected = pd.DataFrame({"time": [1, 2], "A": [10, 15], "B": [20, 25]})
    pd.testing.assert_frame_equal(result, expected)


def test_unstack_data_with_horizontal_data(sample_data: pd.DataFrame) -> None:
    """Test convert_vertical_data_alignment_to_horizontal returns original data for horizontal type."""
    horizontal_settings = {"data_structure": {"type": "horizontal"}}
    result = convert_vertical_data_alignment_to_horizontal(
        sample_data, horizontal_settings, []
    )
    pd.testing.assert_frame_equal(result, sample_data)


def test_unstack_data_missing_time_series() -> None:
    """Test convert_vertical_data_alignment_to_horizontal raises KeyError when time_series is missing in settings."""
    settings = {"data_structure": {"type": "vertical"}}
    with pytest.raises(
        KeyError, match="The 'time_series' section is missing in the settings."
    ):
        convert_vertical_data_alignment_to_horizontal(
            pd.DataFrame(), settings, ["entity_column", "value_column", "time_column"]
        )


def test_unstack_data_missing_required_keys(sample_data: pd.DataFrame) -> None:
    """Test convert_vertical_data_alignment_to_horizontal raises KeyError when required keys are missing in settings."""
    settings = {
        "data_structure": {
            "type": "vertical",
            "time_series": {"entity_column": "entity"},
        }
    }
    required_keys = ["entity_column", "value_column", "time_column"]
    with pytest.raises(
        KeyError, match="Missing keys in the settings: value_column, time_column"
    ):
        convert_vertical_data_alignment_to_horizontal(
            sample_data, settings, required_keys
        )


def test_unstack_data_missing_columns(
    sample_data: pd.DataFrame, sample_settings: dict, required_keys: list[str]
) -> None:
    """Test convert_vertical_data_alignment_to_horizontal raises ValueError when required columns are missing in df."""
    incomplete_data = sample_data.drop(columns=["value"])
    with pytest.raises(ValueError, match="Missing columns in DataFrame: value"):
        convert_vertical_data_alignment_to_horizontal(
            incomplete_data, sample_settings, required_keys
        )


def test_unstack_dataframe(sample_data: pd.DataFrame) -> None:
    """Test unstack_dataframe works correctly."""
    result = unstack_dataframe(sample_data, "entity", "value", "time")
    expected = pd.DataFrame({"time": [1, 2], "A": [10, 15], "B": [20, 25]})
    pd.testing.assert_frame_equal(result, expected)


def test_validate_columns_exist() -> None:
    """Test validate_columns_exist raises ValueError if columns are missing."""
    data = pd.DataFrame({"col1": [1, 2]})
    with pytest.raises(ValueError, match="Missing columns in DataFrame: col2"):
        validate_columns_exist(data, "col1", "col2")


def test_valdiate_missing_keys() -> None:
    """Test validate_missing_keys raises KeyError if required keys are missing."""
    settings = {"key1": "value1"}
    required_keys = ["key1", "key2"]
    with pytest.raises(KeyError, match="Missing keys in the settings: key2"):
        validate_missing_keys(settings, required_keys)


def test_get_data_subset_including_all_columns(sample_data: pd.DataFrame) -> None:
    """Test get_data_subset includes all columns when settings dictate so."""
    settings = {
        "data_selection": {"include_all_columns": True, "max_number_of_rows": 2}
    }
    result = get_data_subset(sample_data, settings)
    pd.testing.assert_frame_equal(result, sample_data.head(2))


def test_get_data_subset_with_column_names(sample_data: pd.DataFrame) -> None:
    """Test get_data_subset works with specific column names in settings."""
    settings = {
        "data_selection": {"column_names": ["entity", "value"], "max_number_of_rows": 2}
    }
    result = get_data_subset(sample_data, settings)
    expected = sample_data[["entity", "value"]].head(2)
    pd.testing.assert_frame_equal(result, expected)


def test_determine_columns_to_include(sample_data: pd.DataFrame) -> None:
    """Test determine_columns_to_include works as expected."""
    settings = {"data_selection": {"column_names": ["entity", "value"]}}
    result = determine_columns_to_include(sample_data, settings)
    assert result == ["entity", "value"]
