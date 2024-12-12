"""
Unit tests for the load_config module in acmetric.

This module contains tests for the load_default_settings and merge_dicts functions.
"""

from unittest.mock import MagicMock, patch

import pytest

from acmetric.eda.utils.load_config import load_default_settings, merge_dicts


@patch(
    "acmetric.eda.utils.load_config.load_settings",
    return_value={"key1": "value1", "key2": "value2"},
)
def test_load_default_settings_valid(mock_load_settings: MagicMock) -> None:
    """Test loading default settings with a valid YAML file."""
    default_settings_file_path = "config.yaml"
    expected_settings = {"key1": "value1", "key2": "value2"}
    settings = load_default_settings(default_settings_file_path)
    assert settings == expected_settings


def test_load_default_settings_invalid_extension() -> None:
    """Test loading default settings with an invalid file extension."""
    default_settings_file_path = "config.txt"
    with pytest.raises(
        ValueError, match="Default config file name should have .yaml extension"
    ):
        load_default_settings(default_settings_file_path)


@patch("acmetric.eda.utils.load_config.load_settings", return_value=None)
def test_load_default_settings_error_loading(mock_load_settings: MagicMock) -> None:
    """Test error handling when loading default settings fails."""
    default_settings_file_path = "config.yaml"
    with pytest.raises(ValueError, match="Error loading default settings from"):
        load_default_settings(default_settings_file_path)


def test_merge_dicts_valid() -> None:
    """Test merging two dictionaries with valid inputs."""
    default = {"key1": "value1", "key2": {"subkey1": "subvalue1"}}
    override = {"key2": {"subkey1": "new_subvalue1"}}
    expected = {"key1": "value1", "key2": {"subkey1": "new_subvalue1"}}
    result = merge_dicts(default, override)
    assert result == expected


def test_merge_dicts_invalid_default_type() -> None:
    """Test merging dictionaries with an invalid default type."""
    default = ["not", "a", "dict"]
    override = {"key1": "value1"}
    with pytest.raises(TypeError, match="Expected 'default' to be a dict"):
        merge_dicts(default, override)  # type: ignore


def test_merge_dicts_invalid_override_type() -> None:
    """Test merging dictionaries with an invalid override type."""
    default = {"key1": "value1"}
    override = ["not", "a", "dict"]
    with pytest.raises(TypeError, match="Expected 'override' to be a dict"):
        merge_dicts(default, override)  # type: ignore


def test_merge_dicts_nested() -> None:
    """Test merging nested dictionaries."""
    default = {
        "key1": "value1",
        "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"},
    }
    override = {"key2": {"subkey1": "new_subvalue1"}}
    expected = {
        "key1": "value1",
        "key2": {"subkey1": "new_subvalue1", "subkey2": "subvalue2"},
    }
    result = merge_dicts(default, override)
    assert result == expected


def test_merge_dicts_no_new_keys() -> None:
    """Test merging dictionaries without adding new keys."""
    default = {"key1": "value1"}
    override = {"key2": "value2"}
    expected = {"key1": "value1"}  # key2 should not be added
    result = merge_dicts(default, override)
    assert result == expected
