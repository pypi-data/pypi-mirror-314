"""Test logger.py."""

from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from acmetric.logger import Logger
from acmetric.logger.loggers.utils.logger_config import LogLevel

IMPORT_PATH = "acmetric.logger.logger"


@pytest.mark.parametrize("name", [None, "some_name"])
def test_init(name: Optional[str]) -> None:
    """Test init."""
    # Act
    logger = Logger(name)
    # Assert
    assert logger.name == name
    assert logger._logger is None


@patch(f"{IMPORT_PATH}.find_logger")
def test_logger_property(
    mock_find_logger: MagicMock,
) -> None:
    """Test logger property of Logger."""
    # Arrange
    Logger._config = MagicMock()
    mock_find_logger.return_value = MagicMock()
    Logger.set_level("debug")
    logger = Logger()

    # Act
    result = logger.logger

    # Assert
    mock_find_logger.assert_called_once_with(None, Logger._config)
    assert result == mock_find_logger.return_value


@patch(f"{IMPORT_PATH}.Logger.logger", new_callable=MagicMock)
def test_debug(mock_logger: MagicMock) -> None:
    """Test debug."""
    message = "This is a debug message."

    logger = Logger()
    logger.debug(message)
    mock_logger.debug.assert_called_once_with(message)


@patch(f"{IMPORT_PATH}.Logger.logger", new_callable=MagicMock)
def test_info(mock_logger: MagicMock) -> None:
    """Test info."""
    message = "This is an info message."

    logger = Logger()
    logger.info(message)
    mock_logger.info.assert_called_once_with(message)


@patch(f"{IMPORT_PATH}.Logger.logger", new_callable=MagicMock)
def test_warning(mock_logger: MagicMock) -> None:
    """Test warning."""
    message = "This is a warning message."

    logger = Logger()
    logger.warning(message)
    mock_logger.warning.assert_called_once_with(message)


@patch(f"{IMPORT_PATH}.Logger.logger", new_callable=MagicMock)
def test_error(mock_logger: MagicMock) -> None:
    """Test error."""
    message = "This is an error message."

    logger = Logger()
    logger.error(message)
    mock_logger.error.assert_called_once_with(message)


@patch(f"{IMPORT_PATH}.Logger._config", new_callable=MagicMock)
def test_set_level(mock_config: MagicMock) -> None:
    """Test set_level."""
    level = "info"

    Logger.set_level(level)
    mock_config.set_option.assert_called_once_with("level", LogLevel(level))


@patch(f"{IMPORT_PATH}.Logger._config", new_callable=MagicMock)
def test_set_options(mock_config: MagicMock) -> None:
    """Test set_option."""
    options = {"format_time": "%Y-%m-%d %H:%M:%S", "format_message": "TEST"}

    Logger.set_options(**options)
    for option_name, option_value in options.items():
        mock_config.set_option.assert_any_call(option_name, option_value)


@patch(f"{IMPORT_PATH}.get_logger_config")
def test_reset_options(mock_get_logger_config: MagicMock) -> None:
    """Test reset_options."""
    mock_get_logger_config.return_value = MagicMock()

    Logger.reset_options()
    assert Logger._config == mock_get_logger_config.return_value
