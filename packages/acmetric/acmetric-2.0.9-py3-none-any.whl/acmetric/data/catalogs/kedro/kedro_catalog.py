"""Kedro data catalog."""

from pathlib import Path
from typing import Any, Optional, Union

from kedro.config import AbstractConfigLoader

from acmetric.data.abs import Data
from acmetric.data.catalogs.kedro.kedro_configs import (
    create_catalog,
    create_templated_config_loader,
)


class KedroDataCatalog:
    """
    A Kedro data catalog that can be instantiated without any parameters.

    Use it to quickly get access to the data catalog in your project.
    Refer to the documentation for more information on how to configure the data catalog:
    https://docs.kedro.org/en/stable/data/data_catalog.html
    """

    def __init__(
        self,
        config_path: Union[str, Path],
        config_loader: Optional[AbstractConfigLoader] = None,
    ) -> None:
        """
        Create a new instance of the data catalog.

        Parameters
        ----------
        config_path: Union[str, Path]
            Path to the configuration directory.
        config_loader: Optional[AbstractConfigLoader]
            Configuration loader. Defaults to `None`. If not provided, a templated config loader will be used.
        """
        self.config_path = str(config_path)
        self.config_loader = config_loader
        if not self.config_loader:
            self.config_loader = create_templated_config_loader(self.config_path)
        self._catalog = create_catalog(self.config_loader)

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "KedroDataCatalog":
        """
        Create a new instance of the data catalog.

        Parameters
        ----------
        config_path: Union[str, Path]
            Path to the configuration directory.

        Returns
        -------
        KedroDataCatalog
            New instance of the data catalog.

        Examples
        --------
        >>> catalog = KedroDataCatalog.in_directory("path/to/config")
        """
        return cls(path)

    def load(self, name: str, **query_args: Any) -> Data:
        """
        Load data from the catalog.

        This method supports dynamic queries for SQL-like data sets.
        For example, if you have a SQL data set with a query like `SELECT * FROM table WHERE column='{value}'`,
        you can pass `value='some_value'` as a keyword argument to this method.

        Parameters
        ----------
        name: str
            Name of the data to be loaded.
        query_args: Any
            Arguments for dynamic queries. Only supported for SQL-like data sets.

        Returns
        -------
        Data
            Data set loaded from the catalog.

        Examples
        --------
        >>> catalog = KedroDataCatalog()
        >>> catalog.load("example_data", min_price=100)
        """
        if query_args:
            return self._load_with_dynamic_query(name, **query_args)
        return self._catalog.load(name)

    def save(self, name: str, data: Data) -> None:
        """
        Save data to the catalog.

        Parameters
        ----------
        name: str
            Name of the data to be saved.
        data: Data
            Data to be saved.
        """
        self._catalog.save(name, data)

    def _load_with_dynamic_query(self, name: str, **query_args: Any) -> Data:
        """
        Load data from the catalog with a dynamic query.

        Parameters
        ----------
        name: str
            Name of the data to be loaded.
        query_args: Any
            Query arguments.

        Returns
        -------
        Data
            Data set loaded from the catalog with a dynamic query.

        Raises
        ------
        ValueError
            If the data set does not support queries.
        """
        load_args = self._catalog._data_sets[name]._load_args
        if "query" not in load_args:
            raise ValueError(f"Data set `{name}` does not support queries.")

        raw_query = load_args["query"]
        load_args["query"] = raw_query.format(**query_args)
        data = self._catalog.load(name)
        load_args["query"] = raw_query

        return data
