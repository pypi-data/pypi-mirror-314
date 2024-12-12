"""Default acmetric data catalog."""

from pathlib import Path
from typing import Any, Optional, Type, Union

from acmetric.data.abs import Data, DataCatalog, DataValidator
from acmetric.data.default_attributes import default_catalog, default_validator


class ValidatedDataCatalog:
    """
    A data catalog that validates data after loading and before saving it.

    Parameters
    ----------
    catalog: `DataCatalog`
        Data catalog. Defaults to `KedroDataCatalog`.
        Data catalog must have `load` and `save` methods.
        `load` method must have `name` parameter.
        `save` method must have `name` and `data` parameters.
    validator: `DataValidator`
        Data validator. Defaults to `GXValidator`.
        Data validator must have `validate` method.
        `validate` method must have `name` and `data` parameters.
        `validate` method must return validated data.
        If you don't want to validate data, use `NoValidator` class.

    Attributes
    ----------
    catalog: `DataCatalog`
        Data catalog.
    validator: `DataValidator`
        Data validator.

    Attributes are immutable and can only be set during instantiation.

    Methods
    -------
    `in_directory`
        Create a new instance of the data catalog with default catalog and validator or custom classes.
    `load`
        Load data from the catalog and validate it.
    `save`
        Save data to the catalog after validating it.

    Raises
    ------
    `ValidationError`
        If the data is invalid.

    Examples
    --------
    >>> acmetric.data.catalog import ValidatedDataCatalog
    >>> catalog = ValidatedDataCatalog.in_directory("path/to/config")
    >>> df = catalog.load("example_data")
    >>> catalog.save("example_data", df)
    """

    __slots__ = ("catalog", "validator")

    def __init__(self, catalog: DataCatalog, validator: DataValidator) -> None:
        """
        Create a new instance of the data catalog.

        Parameters
        ----------
        catalog: DataCatalog
            Data catalog.
        validator: DataValidator
            Data validator.
        """
        self.catalog = catalog
        self.validator = validator

    @classmethod
    def in_directory(
        cls,
        path: Union[str, Path],
        catalog_class: Optional[Type[DataCatalog]] = None,
        validator_class: Optional[Type[DataValidator]] = None,
    ) -> "ValidatedDataCatalog":
        """
        Create a new instance of the data catalog with default catalog and validator or custom classes.

        Parameters
        ----------
        path: Union[str, Path]
            Path to the configuration directory.
        catalog_class: Optional[Type[DataCatalog]]
            Data catalog class. Defaults to `KedroDataCatalog`.
        validator_class: Optional[Type[DataValidator]]
            Data validator class. Defaults to `GXValidator`.

        Returns
        -------
        ValidatedDataCatalog
            New instance of the data catalog.

        Examples
        --------
        >>> acmetric.data.catalog import ValidatedDataCatalog
        >>> catalog = ValidatedDataCatalog.in_directory("path/to/config")
        >>> catalog = ValidatedDataCatalog.in_directory("path/to/config", catalog_class=CustomCatalog)
        >>> catalog = ValidatedDataCatalog.in_directory("path/to/config", validator_class=CustomValidator)
        """
        catalog = (
            catalog_class.in_directory(path) if catalog_class else default_catalog(path)
        )
        validator = (
            validator_class.in_directory(path)
            if validator_class
            else default_validator(path)
        )
        return cls(catalog, validator)

    def load(self, name: str, **kwargs: Any) -> Data:
        """
        Load data from the catalog and validate it.

        Parameters
        ----------
        name: str
            Name of the data to be loaded.
        kwargs: Any
            Additional keyword arguments to be passed to the catalog.

        Returns
        -------
        Data
            Validated data.

        Raises
        ------
        ValidationError
            If the data is invalid.
        """
        return self.validator.validate(name, self.catalog.load(name, **kwargs))

    def save(self, name: str, data: Data) -> None:
        """
        Save data to the catalog after validating it.

        Parameters
        ----------
        name: str
            Name of the data to be saved.
        data: Data
            Data to be saved.

        Raises
        ------
        ValidationError
            If the data is invalid.
        """
        self.catalog.save(name, self.validator.validate(name, data))
