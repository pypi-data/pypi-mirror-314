"""Datasource manager for the data."""

from typing import Union

from great_expectations.data_context.data_context.abstract_data_context import (
    AbstractDataContext,
)
from great_expectations.datasource import PandasDatasource, SparkDFDatasource

from acmetric.data.abs import Data
from acmetric.data.validators.table_utils.table_properties import extract_dataframe_type


class DatasourceManager:
    """Datasource manager for the data."""

    data_reading_methods = {
        "pandas": "add_or_update_pandas",
        "pyspark": "add_or_update_spark",
    }

    def __init__(self, data: Data, data_context: AbstractDataContext) -> None:
        """
        Initialize the datasource manager.

        This method initializes the datasource manager.

        Parameters
        ----------
        data: Data
            Data to be validated.
        data_context: AbstractDataContext
            Great Expectations data context.

        Attributes
        ----------
        data: Data
            Data to be validated.
        data_context: AbstractDataContext
            Great Expectations data context.
        dataframe_type: str
            Type of the dataframe.
        """
        self.data = data
        self.data_context = data_context
        self.datasource_type = extract_dataframe_type(self.data)

    def add_or_update_datasource(self) -> Union[PandasDatasource, SparkDFDatasource]:
        """
        Add or update a datasource.

        This method adds or updates a datasource in the data context
        depending on the type of the dataframe.

        Returns
        -------
        Union[PandasDatasource, SparkDFDatasource]
            Datasource for the data.
        """
        datasource = getattr(
            self.data_context.sources, self.data_reading_methods[self.datasource_type]
        )(name=f"{self.datasource_type}_datasource")
        return datasource
