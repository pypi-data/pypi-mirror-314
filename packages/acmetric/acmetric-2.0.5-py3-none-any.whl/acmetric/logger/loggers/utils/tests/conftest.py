"""Shared fixtures for logger tests."""

import pytest


@pytest.fixture
def mock_yaml_data() -> dict:
    """Mock logger configuration data."""
    return {
        "level": "info",
        "format_time": "{asctime}",
        "format_level": "{levelname:8s}",
        "format_name": "{name}",
        "format_message": "{message}",
        "use_log_filepath": True,
        "log_filepath": "logs/my_python_filepath.log",
    }


@pytest.fixture
def mock_default_config() -> dict:
    """Mock default logger configuration data."""
    return {
        "loguru": {
            "level": "debug",
            "format_time": "<green>{time: YYYY-MM-DD HH:mm:ss}</green>",
            "format_level": "<level>{level: <8}</level>",
            "format_name": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
            "format_message": "<level>{message}</level>",
            "use_log_filepath": True,
            "log_filepath": "logs/my_loguru_filepath.log",
        },
        "python": {
            "level": "info",
            "format_time": "{asctime}",
            "format_level": "{levelname:8s}",
            "format_name": "{name}",
            "format_message": "{message}",
            "use_log_filepath": True,
            "log_filepath": "logs/my_python_filepath.log",
        },
    }
