"""This module contains functions for loading of settings and configurations."""

import os
from pathlib import Path
from typing import Any

import yaml


def get_config_directory() -> str:
    """
    Find the path of the acmetric config directory.

    If not specified in ACMETRIC_CONFIG_DIR environment variable, the default path is used.

    Returns:
        str: Value of the environment variable that specifies the acmetric config directory.
    """
    return str(Path(__file__).parents[1] / "configuration/base")


def load_settings(file_path: str) -> dict[str, Any]:
    """
    Load settings from a YAML configuration file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Loaded settings from the YAML file.
    """
    settings: dict[str, Any] = {}

    if os.path.exists(file_path):
        try:
            with open(file_path) as file:
                settings = yaml.safe_load(file) or {}
        except (FileNotFoundError, yaml.YAMLError):
            raise
    else:
        raise FileNotFoundError(f"Config file {file_path} not found.")

    return settings
