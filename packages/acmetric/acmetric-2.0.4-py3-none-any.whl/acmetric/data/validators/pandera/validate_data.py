"""Validate data."""

from pathlib import Path

from acmetric.data.abs import Data
from acmetric.data.validators.pandera.compile_schema_script import (
    compile_type_specific_schema_script,
)
from acmetric.data.validators.pandera.execute_schema_script import (
    validate_data_with_script_from_path,
)
from acmetric.data.validators.pandera.file_manager import FileManager


def create_schema_script_if_not_exists(
    name: str, data: Data, config_path: Path
) -> None:
    """
    Create schema script.

    This function creates schema script executable by Pandera.

    Parameters
    ----------
    name : str
        Name of the table.
    data : Data
        Dataframe.
    config_path : Path
        Path to configuration directory where schema scripts are stored.

    Returns
    -------
    str
        Schema script.
    """
    file_manager = FileManager(name, config_path)

    if not file_manager.check_if_file_exists():
        file_manager.create_directory_and_empty_file()
        schema_script = compile_type_specific_schema_script(data)
        file_manager.write_file(schema_script)


def validate_data(name: str, data: Data, config_path: Path) -> Data:
    """
    Validate data.

    This function validates data using Pandera.

    Parameters
    ----------
    name : str
        Name of the table.
    data : Data
        Dataframe.
    config_path : Path
        Path to configuration directory where schema scripts are stored.

    Returns
    -------
    Data
        Validated dataframe.
    """
    create_schema_script_if_not_exists(name, data, config_path)
    return validate_data_with_script_from_path(name, data, config_path)
