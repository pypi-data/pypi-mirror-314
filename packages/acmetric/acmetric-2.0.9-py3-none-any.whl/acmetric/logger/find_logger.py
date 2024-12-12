"""Find the default logger for the project."""

import warnings
from importlib.util import find_spec
from typing import Optional

from acmetric.logger.loggers.abs import BaseLogger
from acmetric.logger.loggers.utils.logger_config import LoggerConfig


def find_logger(name: Optional[str], config: LoggerConfig) -> BaseLogger:
    """Find the default logger for the project.

    Parameters
    ----------
    name: Optional[str]
        Name of the logger. Required if using Python logger.

    level: Optional[LogLevel]
        If provided, overwrite the level in config with this level.
        Currently allows 'info', 'debug'.

    Returns
    ----------
    BaseLogger
        Logger object.
    """
    if find_spec("loguru") is not None:
        if name:
            warnings.warn("`name` is not required to use Loguru logger.", stacklevel=2)

        from acmetric.logger.loggers.loguru_logger import LoguruLogger

        return LoguruLogger(config).logger.opt(depth=1)
    else:
        if not name:
            raise ValueError("`name` must be provided to use Python logger.")

        from acmetric.logger.loggers.python_logger import PythonLogger

        return PythonLogger(name, config)
