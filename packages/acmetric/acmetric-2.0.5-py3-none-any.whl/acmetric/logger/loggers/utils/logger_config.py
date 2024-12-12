"""Data classes for logger config."""

from enum import Enum
from typing import Optional, Union, cast


class LogLevel(Enum):
    """Log levels."""

    DEBUG = "debug"
    INFO = "info"


class LoggerConfig:
    """Logger configuration.

    Attributes
    ----------
    level: LogLevel
        Log level
    """

    def __init__(self, raw: dict[str, Union[str, bool, LogLevel]]) -> None:
        """Initialize the logger configuration.

        Parameters
        ----------
        raw: dict[str, Any]
            Raw logger configuration as a dictionary.
            The dictionary must contain the following
            keys:
                - level: str
                - format_time: str
                - format_level: str
                - format_name: str
                - format_message: str
                - log_filepath: str
                - use_log_filepath: bool

        Examples
        ----------
        ```
        # Loguru Logging Config
        raw = {
            "level": "info",
            "format.time": "<green>{time: YYYY-MM-DD HH:mm:ss}</green>",
            "format.level": "<level>{level: <8}</level>",
            "format.name": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
            "format.message": "<level>{message}</level>",
            "log_filepath": False,
            "use_log_filepath": None,
        }

        # Python Logging Config
        raw = {
            "level": "info",
            "format.time": "{asctime}",
            "format.level": "{levelname:8s}",
            "format.name": "{name}",
            "format.message": "{message}",
            "log_filepath": False,
            "use_log_filepath": None,
        }

        """
        self.level: LogLevel = cast(LogLevel, LogLevel(raw["level"]))
        self.format_time: str = cast(str, raw["format_time"])
        self.format_level: str = cast(str, raw["format_level"])
        self.format_name: str = cast(str, raw["format_name"])
        self.format_message: str = cast(str, raw["format_message"])
        self.log_filepath: str = cast(str, raw["log_filepath"])
        self.use_log_filepath: bool = cast(bool, raw["use_log_filepath"])

    def __repr__(self) -> str:
        """Return the string representation of the logger configuration."""
        return f"LoggerConfig({self.__dict__})"

    def set_option(self, name: str, value: Union[str, bool, LogLevel]) -> None:
        """Set an option in the logger configuration.

        Parameters
        ----------
        name: str
            Option name.
        value: Union[str, bool, LogLevel]
            New value. Depending on parameter, allowed values are str, bool, or LogLevel.
        """
        attribute = getattr(self, name, None)
        self._validate_attribute(name, value, attribute)
        super().__setattr__(name, value)

    @staticmethod
    def _validate_attribute(
        name: str,
        value: Union[str, bool, LogLevel],
        attribute: Optional[Union[str, bool, LogLevel]] = None,
    ) -> None:
        """Validate the supplied name, value pairs.

        Parameters
        ----------
        name: str
            Option name.
        value: Union[str, bool, LogLevel]
            New value. Depending on parameter, allowed values are str, bool, or LogLevel.
        attribute: Optional[Union[str, bool, LogLevel]]
            Existing attribute value. Optional in case attribute does not exist in default config.
            In which case it will raise a TypeError.
        """
        if attribute and isinstance(value, type(attribute)):
            return
        elif attribute and not isinstance(value, type(attribute)):
            raise TypeError(
                f"The field {name} has a different type than the default settings: {type(attribute).__name__}."
            )
        else:
            raise TypeError(f"The field {name} is not a valid field.")
