"""Tests for getting logger configurations."""

from unittest.mock import MagicMock, patch

from acmetric.logger.loggers.utils.get_logger_config import (
    _select_logger,
    get_logger_config,
)
from acmetric.logger.loggers.utils.logger_config import LoggerConfig, LogLevel


@patch("acmetric.logger.loggers.utils.get_logger_config.find_spec")
def test_select_logger_with_loguru(mock_find_spec: MagicMock) -> None:
    """Test _select_logger when loguru is available."""
    # Arrange
    mock_find_spec.return_value = True

    # Act
    result = _select_logger()

    # Assert
    assert result == "loguru"
    mock_find_spec.assert_called_once_with("loguru")


@patch("acmetric.logger.loggers.utils.get_logger_config.find_spec")
def test_select_logger_without_loguru(mock_find_spec: MagicMock) -> None:
    """Test _select_logger when loguru is not available."""
    # Arrange
    mock_find_spec.return_value = None

    # Act
    result = _select_logger()

    # Assert
    assert result == "python"
    mock_find_spec.assert_called_once_with("loguru")


@patch("acmetric.logger.loggers.utils.get_logger_config.load_settings")
@patch("acmetric.logger.loggers.utils.get_logger_config._select_logger")
def test_get_logger_config_with_loguru(
    mock_select_logger: MagicMock,
    mock_load_settings: MagicMock,
    mock_default_config: dict,
) -> None:
    """Test get_logger_config when loguru is selected."""
    # Arrange
    mock_select_logger.return_value = "loguru"
    mock_load_settings.return_value = mock_default_config

    # Act
    result = get_logger_config()

    # Assert
    mock_load_settings.assert_called_once()
    mock_select_logger.assert_called_once()
    assert isinstance(result, LoggerConfig)
    assert result.level.name == LogLevel.DEBUG.name


@patch("acmetric.logger.loggers.utils.get_logger_config.load_settings")
@patch("acmetric.logger.loggers.utils.get_logger_config._select_logger")
def test_get_logger_config_with_py(
    mock_select_logger: MagicMock,
    mock_load_settings: MagicMock,
    mock_default_config: dict,
) -> None:
    """Test get_logger_config when python logging is selected."""
    # Arrange
    mock_select_logger.return_value = "python"
    mock_load_settings.return_value = mock_default_config

    # Act
    result = get_logger_config()

    # Assert
    mock_load_settings.assert_called_once()
    mock_select_logger.assert_called_once()
    assert isinstance(result, LoggerConfig)
    assert result.level.name == LogLevel.INFO.name
