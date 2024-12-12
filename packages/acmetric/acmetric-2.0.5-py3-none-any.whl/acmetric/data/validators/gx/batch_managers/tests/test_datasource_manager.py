"""Test the DatasourceManager class."""

from unittest.mock import MagicMock

import pandas as pd
from great_expectations.data_context import EphemeralDataContext

from acmetric.data.validators.gx.batch_managers.datasource_manager import (
    DatasourceManager,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa


def test_datasource_manager_pandas(data_context: EphemeralDataContext) -> None:
    """Test that the DatasourceManager class creates a pandas datasource."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    datasource_manager = DatasourceManager(
        data=data,
        data_context=data_context,
    )
    assert datasource_manager.datasource_type == "pandas"
    datasource_manager.add_or_update_datasource()
    datasorces = data_context.list_datasources()
    assert len(datasorces) == 1
    assert datasorces[0]["name"] == "pandas_datasource"


def test_datasource_manager_spark(data_context: EphemeralDataContext) -> None:
    """Test that the DatasourceManager class creates a spark datasource."""
    data = MagicMock()
    type(data).__module__ = "pyspark.sql.dataframe"
    datasource_manager = DatasourceManager(
        data=data,
        data_context=data_context,
    )
    assert datasource_manager.datasource_type == "pyspark"
    datasource_manager.add_or_update_datasource()
    datasorces = data_context.list_datasources()
    assert len(datasorces) == 1
    assert datasorces[0]["name"] == "pyspark_datasource"
