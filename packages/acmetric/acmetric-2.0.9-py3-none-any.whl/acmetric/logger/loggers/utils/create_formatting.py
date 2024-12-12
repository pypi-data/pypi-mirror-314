"""Utility function to define logger format string."""

from .get_logger_config import LoggerConfig


def create_logger_format(config: LoggerConfig) -> str:
    """Create a logger format string from the configuration.

    Parameters
    ----------
    config: LoggerConfig
        The configuration for the logger.

    Returns
    -------
    str
        The logger format string.
    """
    if not isinstance(config, LoggerConfig):
        raise TypeError("config must be of type LoggerConfig")
    return f"{config.format_time} | {config.format_level} | {config.format_name} - {config.format_message}"
