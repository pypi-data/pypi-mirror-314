"""logging utilities"""

from typing import Optional, Union

from acmetric.logger.find_logger import find_logger
from acmetric.logger.loggers.abs import BaseLogger
from acmetric.logger.loggers.utils.get_logger_config import get_logger_config
from acmetric.logger.loggers.utils.logger_config import LoggerConfig, LogLevel


class Logger:
    """
    Log messages using a logger object.

    Parameters
    ----------
    name: Optional[str]
        Name of the logger. Required if using Python logger.
        Unused if using Loguru logger.

    Examples
    ----------
    >>> from acmetric.logger import Logger
    >>> logger = Logger()
    >>> logger.info("This is an info message")
    """

    _config: LoggerConfig = get_logger_config()

    def __init__(self, name: Optional[str] = None) -> None:
        """Initialize the logger.

        Parameters
        ----------
        name: Optional[str]
            Name of the logger. Required if using Python logger.
            Unused if using Loguru logger.
        """
        self.name = name
        self._logger: Optional[BaseLogger] = None

    @property
    def logger(self) -> BaseLogger:
        """Get the logger object.

        Returns
        ----------
        BaseLogger
            The logger object used for logging messages.
        """
        if self._logger is None:
            self._logger = find_logger(self.name, self._config)
        return self._logger

    @classmethod
    def set_level(cls, level: str) -> None:
        """Set the logging level for the logger.

        Parameters
        ----------
        level: str
            The logging level to use for all instances of the logger.
            Must be one of 'debug', 'info'.
        """
        cls._config.set_option("level", LogLevel(level))

    @classmethod
    def set_options(cls, **kwargs: Union[str, bool]) -> None:
        """Set options in the logger configuration by supplying kwargs.

        Available options:
            - format_time: str
            How to format time in log messages. See relevant logging library docs for details.

            - format_level: str
            How to format log level in log messages. See relevant logging library docs for details.

            - format_name: str
            How to format logger name in log messages. See relevant logging library docs for details.

            - format_message: str
            How to format log message in log messages. See relevant logging library docs for details.

            - use_log_filepath: bool
            Whether to log to a file.

            - log_filepath: str
            The path to the log file, if logging to a file.

        Parameters
        ----------
        name: str
            The name of the option to set.
        value: Union[str, bool]
            The value to set the option to.
        """
        for name, value in kwargs.items():
            cls._config.set_option(name, value)

    @classmethod
    def reset_options(cls) -> None:
        """Reset the logger configuration to the default values."""
        cls._config = get_logger_config()

    def debug(self, message: str) -> None:
        """Log a debug-level message.

        To use only in development or debugging for detailed information on code execution.

        Parameters
        ----------
        message: str
            The message to log.

        Examples
        ----------
        >>> logger.debug("Function X called with arguments Y and Z")
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info-level message.

        General, high-level information on status of operation. Should not be verbose.

        Parameters
        ----------
        message: str
            The message to log.

        Examples
        ----------
        >>> logger.info("Reading table X from catalog")
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning-level message.

        For potential future problems that are not errors. Use rarely.

        Parameters
        ----------
        message: str
            The message to log.

        Examples
        ----------
        >>> logger.warning("Config not found. Using default config.")
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error-level message.

        For logging exceptions and errors in code execution. Use together with exceptions.

        Parameters
        ----------
        message: str
            The exception to log.

        Examples
        ----------
        >>> logger.error("Failed to read table X from catalog")
        """
        self.logger.error(message)
