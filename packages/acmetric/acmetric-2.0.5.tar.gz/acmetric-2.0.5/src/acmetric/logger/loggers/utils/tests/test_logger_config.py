"""Test Logger config classes."""

import pytest

from acmetric.logger.loggers.utils.logger_config import LoggerConfig, LogLevel


def test_log_level_enum() -> None:
    """Test the LogLevel enum."""
    # Test that the enum contains the correct values
    assert LogLevel.DEBUG.value == "debug"
    assert LogLevel.INFO.value == "info"

    # Test creating an enum instance
    assert LogLevel("debug") == LogLevel.DEBUG
    assert LogLevel("info") == LogLevel.INFO

    # Test that invalid enum values raise an error
    with pytest.raises(ValueError):
        LogLevel("invalid_level")


def test_logger_config(mock_yaml_data: dict) -> None:
    """Test the LoggerConfig class."""
    # Arrange
    raw_config = mock_yaml_data
    # Act
    config = LoggerConfig(raw_config)
    # Assert
    assert config.level == LogLevel.INFO
    assert config.format_time == "{asctime}"
    assert config.format_level == "{levelname:8s}"
    assert config.format_name == "{name}"
    assert config.format_message == "{message}"
    assert config.log_filepath == "logs/my_python_filepath.log"
    assert config.use_log_filepath is True


def test_logger_config_invalid_log_level(mock_yaml_data: dict) -> None:
    """Test that an invalid log level raises an error."""
    raw_config = mock_yaml_data
    raw_config["level"] = "invalid_level"

    with pytest.raises(ValueError):
        LoggerConfig(raw_config)


def test_set_option(mock_yaml_data: dict) -> None:
    """Test set_option method."""
    config = LoggerConfig(mock_yaml_data)
    config.set_option("level", LogLevel.DEBUG)
    assert config.level == LogLevel.DEBUG

    config.set_option("format_time", "{time}")
    assert config.format_time == "{time}"

    config.set_option("use_log_filepath", False)
    assert config.use_log_filepath is False


def test_validate_attribute_valid(mock_yaml_data: dict) -> None:
    """Test _validate_attribute with valid inputs."""
    config = LoggerConfig(mock_yaml_data)
    # Valid attribute change
    config._validate_attribute("level", LogLevel.DEBUG, config.level)
    config._validate_attribute("format_time", "{time}", config.format_time)
    config._validate_attribute("use_log_filepath", False, config.use_log_filepath)


def test_validate_attribute_invalid_type(mock_yaml_data: dict) -> None:
    """Test _validate_attribute with invalid type."""
    config = LoggerConfig(mock_yaml_data)

    with pytest.raises(TypeError):
        config._validate_attribute("level", "invalid_level", config.level)

    with pytest.raises(TypeError):
        config._validate_attribute("format_time", 123, config.format_time)  # type: ignore

    with pytest.raises(TypeError):
        config._validate_attribute("use_log_filepath", "yes", config.use_log_filepath)


def test_validate_attribute_invalid_field(mock_yaml_data: dict) -> None:
    """Test _validate_attribute with invalid field."""
    config = LoggerConfig(mock_yaml_data)

    with pytest.raises(TypeError):
        config._validate_attribute("invalid_field", "value", None)


def test_logger_config_repr(mock_yaml_data: dict) -> None:
    """Test the __repr__ method of LoggerConfig."""
    config = LoggerConfig(mock_yaml_data)
    expected_repr = (
        f"LoggerConfig({{'level': {repr(config.level)}, 'format_time': '{config.format_time}', "
        f"'format_level': '{config.format_level}', 'format_name': '{config.format_name}', "
        f"'format_message': '{config.format_message}', 'log_filepath': '{config.log_filepath}', "
        f"'use_log_filepath': {config.use_log_filepath}}})"
    )
    assert repr(config) == expected_repr
