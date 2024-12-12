"""Tests for find_logger function."""

from unittest.mock import MagicMock, patch

import pytest

from acmetric.logger.find_logger import find_logger
from acmetric.logger.loggers.loguru_logger import LoguruLogger
from acmetric.logger.loggers.python_logger import PythonLogger

IMPORT_PATH = "acmetric.logger.find_logger"
LOGURU_LOGGER_PATH = "acmetric.logger.loggers.loguru_logger.LoguruLogger"
PYTHON_LOGGER_PATH = "acmetric.logger.loggers.python_logger.PythonLogger"


def test_find_logger_loguru_present() -> None:
    """Test find_logger when Loguru is installed."""
    config = MagicMock()
    with patch(f"{IMPORT_PATH}.find_spec", return_value=MagicMock()):
        with patch(LOGURU_LOGGER_PATH) as mock_loguru_logger:
            mock_loguru_logger.return_value.logger.opt.return_value = MagicMock(
                spec=LoguruLogger
            )
            with pytest.warns(
                UserWarning, match="`name` is not required to use Loguru logger."
            ):
                logger = find_logger("some name", config)

            assert isinstance(logger, LoguruLogger)
            assert logger.__class__.__name__ == "LoguruLogger"


def test_find_logger_no_loguru_no_name() -> None:
    """Test find_logger when Loguru is not installed and no name is provided."""
    config = MagicMock()
    with patch(f"{IMPORT_PATH}.find_spec", return_value=None):
        with pytest.raises(
            ValueError, match="`name` must be provided to use Python logger."
        ):
            find_logger(None, config)


def test_find_logger_no_loguru_with_name() -> None:
    """Test find_logger when Loguru is not installed and a name is provided."""
    config = MagicMock()
    with patch(f"{IMPORT_PATH}.find_spec", return_value=None):
        with patch(PYTHON_LOGGER_PATH) as mock_python_logger:
            mock_python_logger.return_value = MagicMock(spec=PythonLogger)

            logger = find_logger("some_name", config)

            assert isinstance(logger, PythonLogger)
            assert logger.__class__.__name__ == "PythonLogger"


def test_find_logger_no_config() -> None:
    """Test find_logger when no config is provided."""
    with patch(f"{IMPORT_PATH}.find_spec", return_value=MagicMock()):
        with patch(LOGURU_LOGGER_PATH) as mock_loguru_logger:
            mock_loguru_logger.return_value.logger.opt.return_value = MagicMock(
                spec=LoguruLogger
            )
            with pytest.raises(TypeError):
                find_logger(None)  # type: ignore[call-arg]
