"""Log using Python logging."""

import logging
import sys
import warnings

from acmetric.logger.loggers.utils.create_formatting import create_logger_format
from acmetric.logger.loggers.utils.logger_config import LoggerConfig


class PythonLogger:
    """
    Log using Python logging.

    Attributes
    ----------
    logger: `logging.Logger`
        Logger object.

    Examples
    ----------
    ```
    >>> from acmetric.utils.logger.loggers.python_logger import PythonLogger
    >>> logger = PythonLogger(__name__)
    >>> logger.info("This is an info message")
    ```
    """

    def __init__(self, name: str, config: LoggerConfig) -> None:
        """Initialize the PythonLogger.

        Parameters
        ----------
        name: str
            Name of the logger.
        config: LoggerConfig
            The logger configuration.
        """
        self.logger = logging.getLogger(name)

        self.logger.setLevel(config.level.name)

        self._add_handlers(config)

    def _add_handlers(self, config: LoggerConfig) -> None:
        """Add handlers to the logger.

        Parameters
        ----------
        config: LoggerConfig
            The logger configuration.
        """
        use_log_file = config.use_log_filepath
        log_filepath = config.log_filepath or None
        logging_format = self._create_format(config)

        # Add default handler
        if not len(self.logger.handlers):
            self._add_stream_handler(logging_format)
            if use_log_file:
                if not log_filepath:
                    warnings.warn(
                        "log_filepath not in config. Logging to file will be skipped.",
                        stacklevel=2,
                    )
                else:
                    self._add_file_handler(logging_format, log_filepath)

    def _add_stream_handler(self, logging_format: logging.Formatter) -> None:
        """Add a stream handler to the logger.

        Args:
            logging_format (logging.Formatter): The logging format to use.
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging_format)

        self.logger.addHandler(stream_handler)

    def _add_file_handler(
        self, logging_format: logging.Formatter, log_filepath: str
    ) -> None:
        """Add a file handler to the logger.

        Args:
            logging_format (logging.Formatter): The logging format to use.
            log_filepath (str): The path to the log file.
        """
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setFormatter(logging_format)

        self.logger.addHandler(file_handler)

    def _create_format(self, config: LoggerConfig) -> logging.Formatter:
        """Create a logging Formatter suitable for Python logging.

        Args:
            config (LoggerConfig): The logger configuration.

        Returns:
            logging.Formatter: The logging formatter.
        """
        logging_format = create_logger_format(config)
        return logging.Formatter(logging_format, style="{")

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
