"""Base class for data contexts."""

from typing import Protocol

from great_expectations.data_context import AbstractDataContext


class BaseDataContext(Protocol):
    """Base class for data contexts."""

    def create(self) -> AbstractDataContext:
        """Create a data context."""
        ...
