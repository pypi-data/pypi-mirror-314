"""
This module contains utility functions for general EDA purposes.

The relevant functions for the module are the following:
    - load_default_settings
    - merge_dicts
"""

from copy import deepcopy
from typing import Any

from acmetric.logger import Logger
from acmetric.utils.load_config import load_settings

logger = Logger()


def load_default_settings(file_path: str) -> dict[str, Any]:
    """
    Load EDA default settings from the default configuration file.

    Returns:
        dict: Loaded settings from the default configuration file.

    Raises:
        ValueError: If the default config file does not have a .yaml extension.
        ValueError: If there is an error loading the default settings.
    """
    if not file_path.endswith(".yaml"):
        error_msg = f"Default config file name should have .yaml extension: {file_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    default_settings = load_settings(file_path)

    if not default_settings:
        error_msg = f"Error loading default settings from {file_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Settings loaded from {file_path}")
    return default_settings


def merge_dicts(default: dict, override: dict) -> dict:
    """
    Recursively (deeply) merge two dictionaries.

    Only keys existing in the default dictionary are allowed to be overwritten.

    Args:
        default (dict): The original dictionary.
        override (dict): The dictionary with keys to override.

    Returns:
        dict: The merged dictionary.

    Raises:
        TypeError: If either of the arguments is not a dictionary.
    """
    if not isinstance(default, dict):
        error_msg = f"Expected 'default' to be a dict, but got {type(default).__name__}"
        logger.error(error_msg)
        raise TypeError(error_msg)

    if not isinstance(override, dict):
        error_msg = (
            f"Expected 'override' to be a dict, but got {type(override).__name__}"
        )
        logger.error(error_msg)
        raise TypeError(error_msg)

    default = deepcopy(default)

    for key, value in override.items():
        if key in default:  # Only override existing keys
            if isinstance(value, dict) and isinstance(default[key], dict):
                default[key] = merge_dicts(default[key], value)
            else:
                default[key] = value

    return default
