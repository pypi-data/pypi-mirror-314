"""Log using Loguru logging."""

import sys
import warnings

from loguru import logger

from acmetric.logger.loggers.utils.create_formatting import create_logger_format
from acmetric.logger.loggers.utils.logger_config import LoggerConfig


class LoguruLogger:
    """
    Log using Loguru logging.

    Configs for logging are kept in configuration/base/loguru_logging.yaml by default.

    Attributes
    ----------
    logger: `loguru._logger.Logger`
        Logger object.

    Examples
    ----------
    ```
    >>> from acmetric.logger.loggers.loguru_logger import LoguruLogger
    >>> logger = LoguruLogger()
    >>> logger.info("This is an info message")
    ```
    """

    def __init__(self, config: LoggerConfig) -> None:
        """Initialize the LoguruLogger.

        Parameters
        ----------
        config: LoggerConfig
            The logger configuration.
        """
        self._add_handlers(config)

        # Return with depth=1 to remove this module from the stack trace
        self.logger = logger.opt(depth=1)

    def _add_handlers(self, config: LoggerConfig) -> None:
        """Add handlers to the logger.

        Parameters
        ----------
        config: LoggerConfig
            The logger configuration.
        """
        level = config.level.name
        use_log_file = config.use_log_filepath
        log_filepath = config.log_filepath or None
        logging_format = create_logger_format(config)

        # Add default handler
        handlers = [dict(sink=sys.stdout, level=level, format=logging_format)]

        if use_log_file:
            if not log_filepath:
                warnings.warn(
                    "log_filepath not in config. Logging to file will be skipped.",
                    stacklevel=2,
                )
            else:
                handlers.append(
                    dict(sink=log_filepath, level=level, format=logging_format)
                )

        logger.configure(handlers=handlers)
        self.logger = logger

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
