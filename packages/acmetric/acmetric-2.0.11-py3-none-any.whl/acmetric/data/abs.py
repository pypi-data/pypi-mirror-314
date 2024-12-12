"""Abstract classes for data."""

from pathlib import Path
from typing import Protocol, Union


class Data(Protocol):
    """Abstract class for data. Any dataset can be passed as data."""

    columns: property
    dtypes: property


class DataCatalog(Protocol):
    """Abstract class for data catalog."""

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "DataCatalog":
        """Abstract method for creating a new instance of the data catalog in the directory."""
        ...

    def load(self, name: str) -> Data:
        """Abstract method for loading data from the catalog."""
        ...

    def save(self, name: str, data: Data) -> None:
        """Abstract method for saving data to the catalog."""
        ...


class DataValidator(Protocol):
    """Abstract class for data validator."""

    def validate(self, name: str, data: Data) -> Data:
        """Abstract method for validating data."""
        ...

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "DataValidator":
        """Abstract method for creating a new instance of the data validator in the directory."""
        ...
