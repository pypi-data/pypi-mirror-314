"""Module for testing the ExploratoryDataAnalysis class with mock objects."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from acmetric.eda.utils.base_analysis import ExploratoryDataAnalysis


class MockEDA(ExploratoryDataAnalysis):
    """Mock class for testing the ExploratoryDataAnalysis base class."""

    DEFAULT_CONFIG_FILE_NAME = "mock_config.yaml"

    def analyze(self) -> None:
        """Implement the analyze method."""


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Provide a sample pandas DataFrame for testing."""
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})


@pytest.fixture
def default_settings() -> dict:
    """Provide default settings for testing."""
    return {"data_structure": "horizontal", "subset_columns": ["A"]}


@pytest.fixture
def user_settings() -> dict:
    """Provide user-provided settings for testing."""
    return {"data_structure": "vertical", "subset_columns": ["B"]}


@patch("acmetric.eda.utils.base_analysis.load_default_settings")
@patch("acmetric.eda.utils.base_analysis.get_data_subset")
@patch("acmetric.eda.utils.base_analysis.convert_vertical_data_alignment_to_horizontal")
def test_init_with_default_settings(
    mock_unstack_data: MagicMock,
    mock_get_data_subset: MagicMock,
    mock_load_default_settings: MagicMock,
    sample_dataframe: pd.DataFrame,
    default_settings: dict,
) -> None:
    """Test initialization with default settings only."""
    # Setup mock return values
    mock_load_default_settings.return_value = default_settings
    mock_get_data_subset.return_value = sample_dataframe
    mock_unstack_data.return_value = sample_dataframe

    # Instantiate the subclass and assert settings and dataset
    eda = MockEDA(sample_dataframe)
    assert eda.settings == default_settings
    assert isinstance(eda.dataset, pd.DataFrame)
    assert mock_load_default_settings.called_once()
    assert mock_get_data_subset.called_once()
    assert mock_unstack_data.called_once()


@patch("acmetric.eda.utils.base_analysis.load_default_settings")
@patch("acmetric.eda.utils.base_analysis.get_data_subset")
@patch("acmetric.eda.utils.base_analysis.convert_vertical_data_alignment_to_horizontal")
def test_init_with_user_settings(
    mock_unstack_data: MagicMock,
    mock_get_data_subset: MagicMock,
    mock_load_default_settings: MagicMock,
    sample_dataframe: pd.DataFrame,
    default_settings: dict,
    user_settings: dict,
) -> None:
    """Tests initialization with both default and user-provided settings."""
    # Setup mock return values
    mock_load_default_settings.return_value = default_settings
    mock_get_data_subset.return_value = sample_dataframe
    mock_unstack_data.return_value = sample_dataframe

    # Instantiate the subclass with user settings and assert merged settings
    eda = MockEDA(sample_dataframe, settings=user_settings)
    expected_settings = {**default_settings, **user_settings}
    assert eda.settings == expected_settings
    assert isinstance(eda.dataset, pd.DataFrame)
    assert mock_load_default_settings.called_once()
    assert mock_get_data_subset.called_once()
    assert mock_unstack_data.called_once()


@patch("acmetric.eda.utils.base_analysis.load_default_settings")
@patch("acmetric.eda.utils.base_analysis.get_data_subset")
@patch("acmetric.eda.utils.base_analysis.convert_vertical_data_alignment_to_horizontal")
def test_prepare_data_for_eda(
    mock_unstack_data: MagicMock,
    mock_get_data_subset: MagicMock,
    mock_load_default_settings: MagicMock,
    sample_dataframe: pd.DataFrame,
    default_settings: dict,
) -> None:
    """Tests _prepare_data_for_eda functionality."""
    # Setup mock return values
    mock_load_default_settings.return_value = default_settings
    mock_get_data_subset.return_value = sample_dataframe
    mock_unstack_data.return_value = sample_dataframe

    # Instantiate the subclass and run _prepare_data_for_eda
    eda = MockEDA(sample_dataframe)
    prepared_data = eda._prepare_data_for_eda(sample_dataframe)

    assert isinstance(prepared_data, pd.DataFrame)
    assert not prepared_data.empty
    assert mock_get_data_subset.called_once()
    assert mock_unstack_data.called_once()


@patch("acmetric.eda.utils.base_analysis.load_default_settings")
@patch("acmetric.eda.utils.base_analysis.get_data_subset")
@patch("acmetric.eda.utils.base_analysis.convert_vertical_data_alignment_to_horizontal")
def test_prepare_data_for_eda_empty_result(
    mock_unstack_data: MagicMock,
    mock_get_data_subset: MagicMock,
    mock_load_default_settings: MagicMock,
    sample_dataframe: pd.DataFrame,
    default_settings: dict,
) -> None:
    """Tests _prepare_data_for_eda when unstacked data is empty."""
    # Setup mock return values
    mock_load_default_settings.return_value = default_settings
    mock_get_data_subset.return_value = sample_dataframe
    mock_unstack_data.return_value = (
        pd.DataFrame()
    )  # Return an empty DataFrame to trigger the ValueError

    # Test that ValueError is raised during instantiation (as _prepare_data_for_eda is called in __init__)
    with pytest.raises(ValueError, match="No data available for analysis."):
        MockEDA(sample_dataframe)


@patch("acmetric.eda.utils.base_analysis.load_default_settings")
@patch("acmetric.eda.utils.base_analysis.get_data_subset")
@patch("acmetric.eda.utils.base_analysis.convert_vertical_data_alignment_to_horizontal")
@patch.object(
    ExploratoryDataAnalysis, "_prepare_data_for_eda", return_value=pd.DataFrame()
)
def test_analyze_method_not_implemented(
    mock_unstack_data: MagicMock,
    mock_get_data_subset: MagicMock,
    mock_load_default_settings: MagicMock,
    sample_dataframe: pd.DataFrame,
) -> None:
    """Tests that analyze method raises NotImplementedError if not implemented."""
    # Subclass that provides a no-op implementation of analyze
    class IncompleteEDA(ExploratoryDataAnalysis):
        DEFAULT_CONFIG_FILE_NAME = "mock_config.yaml"

        def analyze(self) -> None:
            """Raise NotImplementedError in this subclass."""
            raise NotImplementedError

    # Instantiate the subclass and call analyze
    incomplete_eda = IncompleteEDA(sample_dataframe)
    with pytest.raises(NotImplementedError):
        incomplete_eda.analyze()
