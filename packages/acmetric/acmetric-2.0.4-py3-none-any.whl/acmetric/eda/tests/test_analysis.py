"""Tests for the TimeSeries class."""

from unittest.mock import patch

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from acmetric.eda.time_series.analysis import TimeSeries


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture for sample data."""
    return pd.DataFrame(
        {
            "time": pd.date_range(start="1/1/2020", periods=5, freq="D"),
            "value": [1, 2, 3, 4, 5],
        }
    )


@pytest.fixture
def sample_settings() -> dict:
    """Fixture for sample settings."""
    return {"entity_column": "entity", "value_column": "value", "time_column": "time"}


@pytest.fixture
def time_series_instance(
    sample_data: pd.DataFrame, sample_settings: dict
) -> TimeSeries:
    """Fixture for TimeSeries instance."""
    with patch(
        "acmetric.eda.utils.base_analysis.ExploratoryDataAnalysis.__init__",
        return_value=None,
    ):
        instance = TimeSeries(sample_data, sample_settings)
        instance.dataset = sample_data
        instance.settings = sample_settings
        return instance


def test_analyze(
    time_series_instance: TimeSeries, sample_data: pd.DataFrame, sample_settings: dict
) -> None:
    """Test the analyze method of TimeSeries."""
    with patch(
        "acmetric.eda.time_series.analysis.print_time_series_statistics"
    ) as mock_print_statistics:
        # Drop non-numeric columns as expected during actual processing
        sample_data_numeric = sample_data.drop(columns=["time"])

        time_series_instance.analyze()

        # Extract the arguments passed to the mock
        mock_args = mock_print_statistics.call_args[
            0
        ]  # This will be a tuple of arguments

        # Compare the DataFrame with assert_frame_equal
        assert_frame_equal(
            mock_args[0], sample_data_numeric
        )  # Compare the first argument (the DataFrame)

        # Ensure the settings argument is correctly passed
        assert mock_args[1] == sample_settings


def test_default_config_file_name() -> None:
    """Test the default config file name."""
    assert TimeSeries.DEFAULT_CONFIG_FILE_NAME == "ts_parameters.yaml"


def test_required_keys() -> None:
    """Test the required keys."""
    assert TimeSeries.REQUIRED_KEYS == ["entity_column", "value_column", "time_column"]
