"""Abstract class for logger."""

from typing import Protocol


class BaseLogger(Protocol):
    """Abstract class for logger."""

    def debug(self, message: str) -> None:
        """Log a debug-level message."""
        ...

    def info(self, message: str) -> None:
        """Log an info-level message."""
        ...

    def warning(self, message: str) -> None:
        """Log a warning-level message."""
        ...

    def error(self, message: str) -> None:
        """Log an error-level message."""
        ...
