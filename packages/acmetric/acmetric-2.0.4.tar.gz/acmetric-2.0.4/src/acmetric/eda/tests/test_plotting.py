"""Tests for time series plotting functions."""

from unittest import mock
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from acmetric.eda.time_series.plotting import (
    plot_acf,
    plot_differenced_line,
    plot_distribution,
    plot_generic,
    plot_line,
    plot_pacf,
    plot_qq,
    plot_stat_function,
    time_series_eda,
)


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture to provide sample time series data."""
    dates = pd.date_range("2022-01-01", periods=100)
    return pd.DataFrame(
        {
            "series1": np.random.randn(100),
            "series2": np.random.randn(100),
            "series3": np.random.randn(100),
        },
        index=dates,
    )


@pytest.fixture
def sample_settings() -> dict:
    """Fixture to provide sample settings for the EDA."""
    return {
        "plotting": {
            "type": "line",
            "max_lines_per_plot": 3,
            "separate_subplots": True,
            "max_number_of_subplots": 3,
            "diff_lag": 1,
            "lag": 10,
        },
        "plot_types": {
            "line": True,
            "differencing": True,
            "distribution": True,
            "acf": True,
            "pacf": True,
            "qq_plot": True,
        },
    }


@mock.patch("acmetric.eda.time_series.plotting.plt.show")
def test_time_series_eda(
    mock_show: MagicMock, sample_data: pd.DataFrame, sample_settings: dict
) -> None:
    """Test time_series_eda function with sample data and settings."""
    time_series_eda(sample_data, sample_settings)
    assert mock_show.called  # This is where plt.show() is expected to be called


def test_plot_line(sample_data: pd.DataFrame) -> None:
    """Test plot_line function without checking for plt.show()."""
    plot_line(sample_data, ["series1", "series2"], "line", False, 2)


def test_plot_differenced_line(sample_data: pd.DataFrame) -> None:
    """Test plot_differenced_line function without checking for plt.show()."""
    plot_differenced_line(sample_data, ["series1", "series2"], 1, "line", False, 2)


def test_plot_distribution(sample_data: pd.DataFrame) -> None:
    """Test plot_distribution function without checking for plt.show()."""
    plot_distribution(sample_data, ["series1", "series2"], False, 2)


@mock.patch("acmetric.eda.time_series.plotting.sm_plot_acf")
def test_plot_acf(mock_acf: MagicMock, sample_data: pd.DataFrame) -> None:
    """Test plot_acf function without checking for plt.show()."""
    plot_acf(sample_data, ["series1", "series2"], 10, False, 2)
    assert mock_acf.called


@mock.patch("acmetric.eda.time_series.plotting.sm_plot_pacf")
def test_plot_pacf(mock_pacf: MagicMock, sample_data: pd.DataFrame) -> None:
    """Test plot_pacf function without checking for plt.show()."""
    plot_pacf(sample_data, ["series1", "series2"], 10, False, 2)
    assert mock_pacf.called


@mock.patch("acmetric.eda.time_series.plotting.sm_qqplot")
def test_plot_qq(mock_qqplot: MagicMock, sample_data: pd.DataFrame) -> None:
    """Test plot_qq function without checking for plt.show()."""
    plot_qq(sample_data, ["series1", "series2"], False, 2)
    assert mock_qqplot.called


def test_plot_generic(sample_data: pd.DataFrame) -> None:
    """Test plot_generic function without checking for plt.show()."""
    plot_generic(sample_data, ["series1", "series2"], "line", False, 2, "Test Plot")


@mock.patch("statsmodels.graphics.tsaplots.plot_acf")
def test_plot_stat_function_acf(mock_acf: MagicMock, sample_data: pd.DataFrame) -> None:
    """Test plot_stat_function with ACF without checking for plt.show()."""
    plot_stat_function(
        mock_acf, sample_data, ["series1", "series2"], 10, False, 2, "ACF Test"
    )
    assert mock_acf.called


@mock.patch("statsmodels.graphics.gofplots.qqplot")
def test_plot_stat_function_qq(
    mock_qqplot: MagicMock, sample_data: pd.DataFrame
) -> None:
    """Test plot_stat_function with QQ plot without checking for plt.show()."""
    plot_stat_function(
        mock_qqplot,
        sample_data,
        ["series1", "series2"],
        None,
        False,
        2,
        "QQ Test",
        is_qq=True,
    )
    assert mock_qqplot.called
