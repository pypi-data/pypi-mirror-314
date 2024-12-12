"""Get the logger configurations for the project."""

import os
from importlib.util import find_spec

from acmetric.logger.loggers.utils.logger_config import LoggerConfig
from acmetric.utils.load_config import get_config_directory, load_settings


def _select_logger() -> str:
    """Identify whether to use Python or Loguru logging."""
    if find_spec("loguru") is not None:
        return "loguru"
    return "python"


def get_logger_config() -> LoggerConfig:
    """Get the default logger configurations from logger.yaml for the given logger library.

    Returns
    ----------
    LoggerConfig
        The logger configuration.
    """
    config_path: str = get_config_directory()
    config_filepath: str = os.path.join(config_path, "logger.yaml")

    all_configs = load_settings(config_filepath)
    raw_config = all_configs[_select_logger()]
    return LoggerConfig(raw_config)
