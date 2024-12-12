"""Test table properties functions."""

from unittest.mock import MagicMock

import pandas as pd
from pyspark.sql import Row, SparkSession

from acmetric.data.validators.table_utils.table_properties import (
    extract_dataframe_schema,
    extract_dataframe_schema_spark_native_format,
    extract_dataframe_type,
)
from acmetric.utils.tests.spark_session import spark  # noqa


def test_extract_dataframe_type_pandas() -> None:
    """Test extract_dataframe_type function."""
    assert extract_dataframe_type(pd.DataFrame()) == "pandas"


def test_extract_dataframe_type_spark() -> None:
    """Test extract_dataframe_schema function."""
    data = MagicMock()
    type(data).__module__ = "pyspark.sql.dataframe"
    assert extract_dataframe_type(data) == "pyspark"


def test_extract_dataframe_schema() -> None:
    """Test extract_dataframe_schema function."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    expected_schema = {
        "col1": "int64",
        "col2": "float64",
        "col3": "object",
    }
    assert extract_dataframe_schema(data) == expected_schema


def test_extract_dataframe_schema_spark_native_format(spark: SparkSession) -> None:
    """Test extract_dataframe_schema_spark_native_format function."""
    data = spark.createDataFrame(
        [
            Row(col1=1, col2=4.0, col3="a"),
            Row(col1=2, col2=5.0, col3="b"),
            Row(col1=3, col2=6.0, col3="c"),
        ]
    )
    expected_schema = {
        "col1": "LongType",
        "col2": "DoubleType",
        "col3": "StringType",
    }
    assert extract_dataframe_schema_spark_native_format(data) == expected_schema
