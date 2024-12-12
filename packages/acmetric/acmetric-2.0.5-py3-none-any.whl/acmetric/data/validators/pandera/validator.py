"""Pandera validator."""

from pathlib import Path
from typing import Union

from acmetric.data.abs import Data
from acmetric.data.validators.pandera.validate_data import validate_data


class PanderaValidator:
    """
    Pandera validator.

    This class validates data using Pandera.
    If the schema object does not exist, it creates a file for it and compiles a script.
    If the schema object exists, it validates the data using the schema object.

    Parameters
    ----------
    config_path : Path
        Path to configuration directory where schema scripts are stored.
    """

    def __init__(self, config_path: Union[str, Path]) -> None:
        """
        Create a new instance of the Pandera validator.

        Parameters
        ----------
        config_path : Union[str, Path]
            Path to configuration directory where schema scripts are stored.
        """
        self.config_path = Path(config_path) / "pandera_schemas"

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "PanderaValidator":
        """
        Create a new instance of the Pandera validator.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the configuration directory.

        Returns
        -------
        PanderaValidator
            New instance of the Pandera validator.
        """
        return cls(path)

    def validate(self, name: str, data: Data) -> Data:
        """
        Validate data.

        This method validates data using Pandera.
        If the schema object does not exist, it creates a file for it and compiles a script.
        If the schema object exists, it validates the data using the schema object.

        Parameters
        ----------
        name : str
            Name of the schema object.
        data : Data
            Dataframe.

        Returns
        -------
        Data
            Validated dataframe.
        """
        return validate_data(name, data, self.config_path)
