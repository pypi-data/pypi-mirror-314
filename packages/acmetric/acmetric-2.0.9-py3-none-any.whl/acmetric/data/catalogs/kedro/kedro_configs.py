"""Kedro configuration utilities."""

import warnings
from pathlib import Path
from typing import Any

from kedro.config import (
    AbstractConfigLoader,
    MissingConfigException,
    TemplatedConfigLoader,
)
from kedro.io import DataCatalog


def create_templated_config_loader(config_path: str) -> TemplatedConfigLoader:
    """
    Return a Kedro templated configuration loader.

    Parameters
    ----------
    config_path: str
        Path to the configuration directory.

    Returns
    -------
    TemplatedConfigLoader
        Kedro configuration loader.
    """
    return TemplatedConfigLoader(config_path, globals_pattern="*catalog_globals.yml")


def get_catalog_config(
    config_loader: AbstractConfigLoader,
) -> dict[str, dict[str, Any]]:
    """
    Return the catalog configuration.

    Parameters
    ----------
    config_loader: AbstractConfigLoader
        Kedro configuration loader.

    Returns
    -------
    dict[str, dict[str, Any]]
        Catalog configuration.
    """
    return config_loader.get("catalog.yml") or {}


def _replace_sql_with_query(catalog_config: dict) -> dict[str, dict[str, Any]]:
    """
    Replace the `sql` key in the catalog configuration with the actual query stored in data/queries.

    Parameters
    ----------
    catalog_config: dict
        Catalog configuration.

    Returns
    -------
    dict[str, dict[str, Any]]
        Catalog configuration with the `sql` key replaced with the actual query.
    """
    for df_name, params in catalog_config.items():
        if "sql" in params and Path(params["sql"]).is_file():
            file_path = Path(params["sql"])
            catalog_config[df_name]["sql"] = file_path.read_text()

    return catalog_config


def get_credentials_config(
    config_loader: AbstractConfigLoader,
) -> dict[str, dict[str, Any]]:
    """
    Return the credentials configuration.

    If the project does not have a `credentials.yml` file, a warning will be issued
    and an empty dictionary will be returned.

    Parameters
    ----------
    config_loader: AbstractConfigLoader
        Kedro configuration loader.

    Returns
    -------
    dict[str, dict[str, Any]]
        Credentials configuration.
    """
    try:
        return config_loader.get("credentials.yml") or {}
    except MissingConfigException:
        warning_message = (
            "Your Kedro project does not have a `credentials.yml` file. "
            "Please refer to https://docs.kedro.org/en/stable/configuration/credentials.html "
            "for instructions on how to set up credentials."
        )
        warnings.warn(warning_message, stacklevel=2)
        return {}


def create_catalog(
    config_loader: AbstractConfigLoader,
) -> DataCatalog:
    """
    Create a data catalog from a Kedro configuration.

    Parameters
    ----------
    config_loader: AbstractConfigLoader, optional
        Kedro configuration loader. Defaults to `TemplatedConfigLoader`.

    Returns
    -------
    DataCatalog
        Kedro data catalog.
    """
    catalog_config = get_catalog_config(config_loader)
    catalog_config_updated = _replace_sql_with_query(catalog_config)
    credentials_config = get_credentials_config(config_loader)
    catalog = DataCatalog.from_config(
        catalog=catalog_config_updated,
        credentials=credentials_config,
    )
    return catalog
