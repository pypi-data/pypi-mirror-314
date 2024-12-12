"""Tests for the time series statistics module."""

from contextlib import redirect_stdout
from io import StringIO

import pandas as pd
import pytest

from acmetric.eda.time_series.statistics import (
    collect_jarque_bera_test,
    collect_ljung_box_test,
    collect_stationarity_test,
    collect_summary_statistics,
    print_time_series_statistics,
)


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Return a sample DataFrame for testing."""
    return pd.DataFrame({"series_1": [1, 2, 3, 4, 5], "series_2": [2, 3, 4, 5, 6]})


def test_collect_summary_statistics(sample_data: pd.DataFrame) -> None:
    """Test summary statistics collection."""
    summary_stats = collect_summary_statistics(sample_data)
    assert summary_stats is not None
    assert "mean" in summary_stats.index


def test_collect_jarque_bera_test(sample_data: pd.DataFrame) -> None:
    """Test Jarque-Bera test collection."""
    jb_test = collect_jarque_bera_test(sample_data)
    assert jb_test is not None
    # Access the DataFrame index by checking for the statistic names (e.g., JB Statistic, P-value)
    assert "P-value" in jb_test.index
    assert "JB Statistic" in jb_test.index
    # Check the columns to verify the series names
    assert "series_1" in jb_test.columns
    assert "series_2" in jb_test.columns


def test_collect_stationarity_test(sample_data: pd.DataFrame) -> None:
    """Test Augmented Dickey-Fuller (ADF) test collection."""
    adf_test = collect_stationarity_test(sample_data)
    assert adf_test is not None
    # Access the DataFrame index by checking for the statistic names (e.g., ADF Statistic, P-value)
    assert "P-value" in adf_test.index
    assert "ADF Statistic" in adf_test.index
    # Check the columns to verify the series names
    assert "series_1" in adf_test.columns
    assert "series_2" in adf_test.columns


def test_collect_ljung_box_test(sample_data: pd.DataFrame) -> None:
    """Test Ljung-Box test collection."""
    ljung_box_test = collect_ljung_box_test(sample_data, max_lag=3)
    assert ljung_box_test is not None
    assert ljung_box_test["series_1"].iloc[0] >= 0  # Check if p-value is non-negative


def test_print_time_series_statistics_all_tests(sample_data: pd.DataFrame) -> None:
    """Test print_time_series_statistics with all tests enabled."""
    settings = {
        "statistics": {
            "summary_statistics": True,
            "normality_test": True,
            "stationarity_test": True,
            "autocorrelation_test": True,
            "max_lag": 3,
        }
    }

    f = StringIO()
    with redirect_stdout(f):
        print_time_series_statistics(sample_data, settings)
    output = f.getvalue()

    # Check for summary statistics output
    assert "Summary Statistics" in output

    # Check for normality test output
    assert "Jarque-Bera Normality Test" in output
    assert "P-value" in output

    # Check for stationarity test output
    assert "Augmented Dickey-Fuller (ADF)" in output
    assert "ADF Statistic" in output

    # Check for Ljung-Box test output - check for p-value values instead of specific field names
    assert "Ljung-Box Test" in output
    assert "0.236724" in output  # Example p-value that is part of the Ljung-Box result


def test_print_time_series_statistics_some_tests(sample_data: pd.DataFrame) -> None:
    """Test print_time_series_statistics with only some tests enabled."""
    settings = {
        "statistics": {
            "summary_statistics": True,
            "normality_test": False,
            "stationarity_test": True,
            "autocorrelation_test": False,
        }
    }

    f = StringIO()
    with redirect_stdout(f):
        print_time_series_statistics(sample_data, settings)
    output = f.getvalue()

    # Check for summary statistics output
    assert "Summary Statistics" in output

    # Check for normality test absence
    assert "Jarque-Bera Normality Test" not in output

    # Check for stationarity test output
    assert "Augmented Dickey-Fuller (ADF)" in output

    # Check for Ljung-Box test absence
    assert "Ljung-Box Test" not in output


def test_print_time_series_statistics_no_tests(sample_data: pd.DataFrame) -> None:
    """Test print_time_series_statistics with no tests enabled."""
    settings = {
        "statistics": {
            "summary_statistics": False,
            "normality_test": False,
            "stationarity_test": False,
            "autocorrelation_test": False,
        }
    }

    f = StringIO()
    with redirect_stdout(f):
        print_time_series_statistics(sample_data, settings)
    output = f.getvalue()

    # Ensure no output is printed
    assert output == ""


def test_print_time_series_statistics_invalid_lag(sample_data: pd.DataFrame) -> None:
    """Test print_time_series_statistics with an invalid (negative) max_lag."""
    settings = {
        "statistics": {
            "summary_statistics": True,
            "normality_test": True,
            "stationarity_test": True,
            "autocorrelation_test": True,
            "max_lag": -1,  # Invalid lag
        }
    }

    with pytest.raises(ValueError, match="max_lag must be a positive integer"):
        print_time_series_statistics(sample_data, settings)
