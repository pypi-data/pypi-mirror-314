"""Tests for the PythonLogger class."""

import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

from acmetric.logger.loggers.python_logger import PythonLogger
from acmetric.logger.loggers.utils.create_formatting import create_logger_format
from acmetric.logger.loggers.utils.logger_config import LoggerConfig

IMPORT_STRING = "acmetric.logger.loggers.python_logger"


@pytest.fixture(scope="module")
def python_logger(mock_python_yaml_data: dict) -> PythonLogger:
    """Fixture for creating a PythonLogger instance."""
    config = LoggerConfig(mock_python_yaml_data)
    return PythonLogger("test", config)


@patch("logging.getLogger")
@pytest.mark.parametrize("use_log_filepath", [True, False])
def test_init_with_name_and_config(
    mock_getLogger: MagicMock, use_log_filepath: bool, mock_python_yaml_data: dict
) -> None:
    """Test the initialization of the PythonLogger class.

    Include name and config as input.
    """
    # Arrange
    mock_logger = MagicMock(spec=logging.Logger)
    mock_logger.handlers = []
    mock_getLogger.return_value = mock_logger
    config = LoggerConfig(mock_python_yaml_data)
    config.use_log_filepath = use_log_filepath
    config.log_filepath = "my_python_filepath.log"
    # Act
    PythonLogger(__name__, config)
    # Assert
    # Created with correct name and level
    mock_getLogger.assert_called_once_with(__name__)
    mock_logger.setLevel.assert_called_once_with(config.level.name)
    # Correct number of handlers added (extra one if we write to file)
    if use_log_filepath:
        mock_logger.addHandler.assert_called()
        assert mock_logger.addHandler.call_count == 2
    else:
        mock_logger.addHandler.assert_called()
        assert mock_logger.addHandler.call_count == 1


def test_init_without_name_raises_error(mock_python_yaml_data: dict) -> None:
    """Test the initialization of the PythonLogger class.

    Without name as input.
    """
    config = LoggerConfig(mock_python_yaml_data)
    with pytest.raises(TypeError):
        PythonLogger(config=config)  # type: ignore


def test_init_without_config_raises_error() -> None:
    """Test the initialization of the PythonLogger class.

    Without config as input.
    """
    with pytest.raises(TypeError):
        PythonLogger(name="test")  # type: ignore


@pytest.mark.parametrize("use_log_filepath", [False, True])
@patch(f"{IMPORT_STRING}.logging.FileHandler")
@patch(f"{IMPORT_STRING}.logging.StreamHandler")
@patch(f"{IMPORT_STRING}.logging.Formatter")
@patch(f"{IMPORT_STRING}.create_logger_format")
def test_add_handlers(
    mock_create_logger_format: MagicMock,
    mock_formatter: MagicMock,
    mock_stream_handler: MagicMock,
    mock_file_handler: MagicMock,
    use_log_filepath: MagicMock,
    mock_python_yaml_data: dict,
) -> None:
    """Test the add_handlers method of the PythonLogger class."""
    # Arrange
    config = LoggerConfig(mock_python_yaml_data)
    config.use_log_filepath = use_log_filepath
    logging_format = create_logger_format(config)

    # Mocks
    mock_create_logger_format.return_value = logging_format
    mock_formatter.return_value = logging_format

    with patch.object(logging.Logger, "addHandler", autospec=True) as mock_add_handler:
        # Act
        logger_instance = PythonLogger(__name__, config)

        # Assert the StreamHandler was created, configured, and added
        mock_stream_handler.assert_called_once_with(sys.stdout)
        mock_stream_handler.return_value.setFormatter.assert_called_once_with(
            mock_formatter.return_value
        )
        mock_add_handler.assert_any_call(
            logger_instance.logger, mock_stream_handler.return_value
        )

        if use_log_filepath:
            # Assert the FileHandler was created, configured, and added
            mock_file_handler.assert_called_once_with("logs/my_python_filepath.log")
            mock_file_handler.return_value.setFormatter.assert_called_once_with(
                mock_formatter.return_value
            )
            mock_add_handler.assert_any_call(
                logger_instance.logger, mock_file_handler.return_value
            )
        else:
            # Assert FileHandler was not called when use_log_filepath is False
            mock_file_handler.assert_not_called()


def test_add_handlers_raises_warning(mock_python_yaml_data: dict) -> None:
    """Test the _add_handlers method of the LoguruLogger class."""
    # Arrange
    config_dict = mock_python_yaml_data
    config_dict["log_filepath"] = None
    config = LoggerConfig(config_dict)

    # Act
    with pytest.warns(
        UserWarning,
        match="log_filepath not in config. Logging to file will be skipped.",
    ):
        PythonLogger(__name__, config)


def test_debug(python_logger: PythonLogger) -> None:
    """Test the debug method of the PythonLogger class."""
    with patch.object(python_logger.logger, "debug") as mock_debug:
        python_logger.debug("Debug message")
        mock_debug.assert_called_once_with("Debug message")


def test_info(python_logger: PythonLogger) -> None:
    """Test the info method of the PythonLogger class."""
    with patch.object(python_logger.logger, "info") as mock_info:
        python_logger.info("info message")
        mock_info.assert_called_once_with("info message")


def test_warning(python_logger: PythonLogger) -> None:
    """Test the warning method of the PythonLogger class."""
    with patch.object(python_logger.logger, "warning") as mock_warning:
        python_logger.warning("warning message")
        mock_warning.assert_called_once_with("warning message")


def test_error(python_logger: PythonLogger) -> None:
    """Test the error method of the PythonLogger class."""
    with patch.object(python_logger.logger, "error") as mock_error:
        python_logger.error("error message")
        mock_error.assert_called_once_with("error message")
