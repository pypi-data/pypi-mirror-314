"""Execute schema script."""

from pathlib import Path
from types import ModuleType

from acmetric.data.abs import Data
from acmetric.utils.manage_filesystem import extract_relative_path
from acmetric.utils.manage_modules import import_or_reload_module


def execute_validation(module: ModuleType, data: Data) -> Data:
    """
    Execute validation.

    This function executes validation using Pandera.

    Parameters
    ----------
    module : ModuleType
        Module.
    data : Data
        Dataframe.

    Returns
    -------
    Data
        Validated dataframe.
    """
    return module.schema.validate(data, lazy=False)


def construct_module_name(name: str, path: Path) -> str:
    """
    Construct module name.

    This function constructs module name from the name of the table and the path to the directory
    where the schema script is stored.

    Parameters
    ----------
    name : str
        Name of the table.
    path : Path
        Path to the directory where the schema script is stored.

    Returns
    -------
    str
        Module name.
    """
    root_module_path = str(extract_relative_path(path)).replace("/", ".")
    return f"{root_module_path}.{name}"


def validate_data_with_script_from_path(name: str, data: Data, path: Path) -> Data:
    """
    Validate data with script from path.

    This function validates data using Pandera script from the path.

    Parameters
    ----------
    name : str
        Name of the table.
    data : Data
        Dataframe.
    path : Path
        Path to the directory where the schema script is stored.

    Returns
    -------
    Data
        Validated dataframe.
    """
    module_name = construct_module_name(name, path)
    module = import_or_reload_module(module_name)
    return execute_validation(module, data)
