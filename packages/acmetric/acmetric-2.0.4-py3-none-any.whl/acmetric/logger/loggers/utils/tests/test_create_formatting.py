"""Tests for the create_logger_format function."""

import pytest

from acmetric.logger.loggers.utils.create_formatting import create_logger_format
from acmetric.logger.loggers.utils.logger_config import LoggerConfig


def test_create_logger_format_config(mock_yaml_data: dict) -> None:
    """Test the create_logger_format function."""
    config = LoggerConfig(mock_yaml_data)
    expected_format = "{asctime} | {levelname:8s} | {name} - {message}"
    result = create_logger_format(config)
    assert result == expected_format


def test_create_logger_format_no_config() -> None:
    """Test the create_logger_format function."""
    with pytest.raises(TypeError):
        create_logger_format("test")  # type: ignore
