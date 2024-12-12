"""Tests for load_config.py"""

from unittest.mock import mock_open, patch

import pytest
import yaml

# Mock logger to avoid actual logging during tests
from acmetric.logger import Logger
from acmetric.utils.load_config import load_settings

logger = Logger()


def test_load_settings_success() -> None:
    """Test successful loading of settings."""
    mock_yaml_content = """
    key1: value1
    key2: value2
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        with patch("os.path.exists", return_value=True):
            settings = load_settings("dummy_path.yaml")
            assert settings == {"key1": "value1", "key2": "value2"}


def test_load_settings_file_not_found() -> None:
    """Test FileNotFoundError when file does not exist."""
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_settings("dummy_path.yaml")


def test_load_settings_yaml_error() -> None:
    """Test yaml.YAMLError when YAML is invalid."""
    mock_yaml_content = """
    key1: value1
    key2: value2
    invalid_yaml
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(yaml.YAMLError):
                load_settings("dummy_path.yaml")


def test_load_settings_unexpected_error() -> None:
    """Test unexpected error when opening file."""
    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = Exception("Unexpected error")
        with patch("os.path.exists", return_value=True):
            with pytest.raises(Exception, match="Unexpected error"):
                load_settings("dummy_path.yaml")
