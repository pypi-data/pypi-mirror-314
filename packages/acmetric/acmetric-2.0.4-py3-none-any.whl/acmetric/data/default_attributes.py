"""
Functions to return default data catalog and data validator.

The default data catalog is `KedroDataCatalog` from `kedro` package.
The default data validator is `GXValidator` from `great_expectations` package.
If `great_expectations` package is not installed, the default data validator is
`PanderaValidator` from `pandera` package. If neither `great_expectations` nor
`pandera` packages are installed, raises `ImportError`.
"""

import warnings
from importlib.util import find_spec
from pathlib import Path
from typing import Union

from acmetric.data.abs import DataCatalog, DataValidator


def default_catalog(config_path: Union[str, Path]) -> DataCatalog:
    """
    Return default data catalog initialized in the directory.

    Looks-up `kedro` package and returns `KedroDataCatalog` if it is installed.

    Parameters
    ----------
    config_path : Union[str, Path]
        Path to the configuration directory.

    Returns
    -------
    DataCatalog
        Default data catalog.

    Raises
    ------
    `ImportError`
        If `kedro` package is not installed.
    """
    is_kedro_installed = find_spec("kedro") is not None
    if not is_kedro_installed:
        raise ImportError(
            "Default data catalog is KedroDataCatalog. "
            "You must install kedro to use KedroDataCatalog. "
            "Run `poetry install --with kedro` to do so. "
            "Alternatively, you can implement your own data catalog."
        )

    from acmetric.data.catalogs.kedro import KedroDataCatalog

    return KedroDataCatalog(config_path)


def default_validator(config_path: Union[str, Path]) -> DataValidator:
    """
    Return default data validator initialized in the directory.

    Looks-up `great_expectations` package and returns `GXValidator` if it is installed.
    If `great_expectations` package is not installed, looks-up `pandera` package and
    returns `PanderaValidator` if it is installed. If neither `great_expectations` nor
    `pandera` packages are installed, raises `ImportError`.

    Parameters
    ----------
    config_path : Union[str, Path]
        Path to the configuration directory.

    Returns
    -------
    DataValidator
        Default data validator.

    Raises
    ------
    `ImportError`
        If neither `great_expectations` nor `pandera` packages are installed.
    """
    is_great_expectations_installed = find_spec("great_expectations") is not None
    is_pandera_installed = find_spec("pandera") is not None

    if is_great_expectations_installed:
        from acmetric.data.validators.gx import GXValidator

        return GXValidator.in_directory(config_path)
    elif is_pandera_installed:
        warnings.warn(
            "Default data validator is GXValidator. "
            "Great Expectations is not installed. "
            "Using PanderaValidator instead.",
            stacklevel=2,
        )
        from acmetric.data.validators.pandera import PanderaValidator

        return PanderaValidator.in_directory(config_path)
    else:
        raise ImportError(
            "Default data validators are GXValidator and PanderaValidator. "
            "You must install either great_expectations or pandera to use them. "
            "Neither package is installed. "
            "Run `poetry install --with great_expectations` or "
            "`poetry install --with pandera` to do so. "
            "Alternatively, you can implement your own data validator. "
            "If you don't want to validate data, use NoValidator class (not recommended)."
        )
