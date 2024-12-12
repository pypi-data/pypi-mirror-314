"""Tests for the LoguruLogger class."""

from unittest.mock import MagicMock, patch

import pytest

from acmetric.logger.loggers.loguru_logger import LoguruLogger
from acmetric.logger.loggers.utils.create_formatting import create_logger_format
from acmetric.logger.loggers.utils.logger_config import LoggerConfig

IMPORT_STRING = "acmetric.logger.loggers.loguru_logger"


@pytest.fixture(scope="module")
def loguru_logger(mock_loguru_yaml_data: dict) -> LoguruLogger:
    """Fixture for creating a LoguruLogger instance."""
    config = LoggerConfig(mock_loguru_yaml_data)
    return LoguruLogger(config)


@patch(f"{IMPORT_STRING}.LoguruLogger._add_handlers")
def test_init(mock_add_handlers: MagicMock, mock_loguru_yaml_data: dict) -> None:
    """Test that the LoguruLogger class initializes as expected."""
    # Arrange
    config = LoggerConfig(mock_loguru_yaml_data)
    # Act
    LoguruLogger(config)
    # Assert
    mock_add_handlers.assert_called_once_with(config)


def test_init_without_config_raises() -> None:
    """Test that the LoguruLogger class raises an error when init without config."""
    with pytest.raises(TypeError):
        LoguruLogger()  # type: ignore[call-arg]


@patch(f"{IMPORT_STRING}.sys.stdout")
@patch(f"{IMPORT_STRING}.logger.configure")
def test_add_handlers(
    mock_configure: MagicMock, mock_stdout: MagicMock, mock_loguru_yaml_data: dict
) -> None:
    """Test the _add_handlers method of the LoguruLogger class."""
    # Arrange

    config = LoggerConfig(mock_loguru_yaml_data)
    logger_format = create_logger_format(config)

    # Act
    LoguruLogger(config)

    # Assert
    mock_configure.assert_called_once_with(
        handlers=[
            {"sink": mock_stdout, "level": config.level.name, "format": logger_format},
            {
                "sink": config.log_filepath,
                "level": config.level.name,
                "format": logger_format,
            },
        ]
    )


def test_add_handlers_raises_warning(mock_loguru_yaml_data: dict) -> None:
    """Test the _add_handlers method of the LoguruLogger class."""
    # Arrange
    config_dict = mock_loguru_yaml_data
    config_dict["log_filepath"] = None
    config = LoggerConfig(config_dict)

    # Act
    with pytest.warns(
        UserWarning,
        match="log_filepath not in config. Logging to file will be skipped.",
    ):
        LoguruLogger(config)


def test_debug(loguru_logger: LoguruLogger) -> None:
    """Test the debug method of the LoguruLogger class."""
    with patch.object(loguru_logger.logger, "debug") as mock_debug:
        loguru_logger.debug("Debug message")
        mock_debug.assert_called_once_with("Debug message")


def test_info(loguru_logger: LoguruLogger) -> None:
    """Test the info method of the LoguruLogger class."""
    with patch.object(loguru_logger.logger, "info") as mock_info:
        loguru_logger.info("info message")
        mock_info.assert_called_once_with("info message")


def test_warning(loguru_logger: LoguruLogger) -> None:
    """Test the warning method of the LoguruLogger class."""
    with patch.object(loguru_logger.logger, "warning") as mock_warning:
        loguru_logger.warning("warning message")
        mock_warning.assert_called_once_with("warning message")


def test_error(loguru_logger: LoguruLogger) -> None:
    """Test the error method of the LoguruLogger class."""
    with patch.object(loguru_logger.logger, "error") as mock_error:
        loguru_logger.error("error message")
        mock_error.assert_called_once_with("error message")
