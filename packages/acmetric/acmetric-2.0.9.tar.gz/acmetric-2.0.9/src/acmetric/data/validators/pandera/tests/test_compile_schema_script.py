"""Tests for compile_schema_script.py module."""

import pandas as pd
import pytest
from pyspark.sql import SparkSession

from acmetric.data.validators.pandera.compile_schema_script import (
    PandasSchemaScriptCompiler,
    SparkSchemaScriptCompiler,
    compile_type_specific_schema_script,
    determine_compiler,
)
from acmetric.utils.tests.spark_session import spark  # noqa


def test_extract_dataframe_schema_pandas() -> None:
    """Test the extract_dataframe_schema method of PandasSchemaScriptCompiler."""
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [1.0, 2.0, 3.0]})
    compiler = PandasSchemaScriptCompiler()

    result = compiler.extract_dataframe_schema(data)

    expected_result = {"col1": "int64", "col2": "float64"}
    assert result == expected_result


def test_compile_schema_string_pandas() -> None:
    """Test the compile_schema_string method of PandasSchemaScriptCompiler."""
    df_schema = {"col1": "int64", "col2": "float64"}
    compiler = PandasSchemaScriptCompiler()

    result = compiler.compile_schema_string(df_schema)

    expected_result = '\t"col1": pa.Column("int64", checks=[]),\n\t"col2": pa.Column("float64", checks=[]),\n'
    assert result == expected_result


def test_insert_schema_string_to_script_pandas() -> None:
    """Test the insert_schema_string_to_script method of PandasSchemaScriptCompiler."""
    df_schema_string = '\t"col1": pa.Column("int64", checks=[]),\n\t"col2": pa.Column("float64", checks=[]),\n'
    compiler = PandasSchemaScriptCompiler()

    result = compiler.insert_schema_string_to_script(df_schema_string)

    expected_result = '''"""Pandera schema for Pandas."""
import pandera as pa

# Insert your additional checks to `checks` list parameter for each column
# e.g. checks=[pa.Check(lambda s: s.str.len() > 0, element_wise=True)]
# refer to https://pandera.readthedocs.io/en/stable/checks.html for more details.

schema = pa.DataFrameSchema({
\t"col1": pa.Column("int64", checks=[]),
\t"col2": pa.Column("float64", checks=[]),
})
'''
    assert result == expected_result


def test_compile_schema_script_pandas() -> None:
    """Test the compile_schema_script method of PandasSchemaScriptCompiler."""
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [1.0, 2.0, 3.0]})
    compiler = PandasSchemaScriptCompiler()

    result = compiler.compile_schema_script(data)

    expected_result = '''"""Pandera schema for Pandas."""
import pandera as pa

# Insert your additional checks to `checks` list parameter for each column
# e.g. checks=[pa.Check(lambda s: s.str.len() > 0, element_wise=True)]
# refer to https://pandera.readthedocs.io/en/stable/checks.html for more details.

schema = pa.DataFrameSchema({
\t"col1": pa.Column("int64", checks=[]),
\t"col2": pa.Column("float64", checks=[]),
})
'''
    assert result == expected_result


def test_extract_dataframe_schema_spark(spark: SparkSession) -> None:
    """Test the extract_dataframe_schema method of SparkSchemaScriptCompiler."""
    data = spark.createDataFrame(
        [
            (1, 1.0),
            (2, 2.0),
            (3, 3.0),
        ],
        ["col1", "col2"],
    )
    compiler = SparkSchemaScriptCompiler()

    result = compiler.extract_dataframe_schema(data)

    expected_result = {"col1": "LongType", "col2": "DoubleType"}
    assert result == expected_result


def test_compile_schema_string_spark() -> None:
    """Test the compile_schema_string method of SparkSchemaScriptCompiler."""
    df_schema = {"col1": "LongType", "col2": "DoubleType"}
    compiler = SparkSchemaScriptCompiler()

    result = compiler.compile_schema_string(df_schema)

    expected_result = "\tcol1: T.LongType\n\tcol2: T.DoubleType\n"
    assert result == expected_result


def test_insert_schema_string_to_script_spark() -> None:
    """Test the insert_schema_string_to_script method of SparkSchemaScriptCompiler."""
    df_schema_string = "\tcol1: T.LongType\n\tcol2: T.DoubleType\n"
    compiler = SparkSchemaScriptCompiler()

    result = compiler.insert_schema_string_to_script(df_schema_string)

    expected_result = '''"""Pandera schema for Spark."""
import pandera.pyspark as pa  # noqa
import pyspark.sql.types as T
from pandera.pyspark import DataFrameModel

# To add more checks, use ` = pa.Field(...)` after each column
# e.g. username: T.StringType = pa.Field(str_startswith("user_"))
# refer to https://pandera.readthedocs.io/en/stable/pyspark_sql.html for more details.

class Schema(DataFrameModel):
\t"""Pandera schema."""

\tcol1: T.LongType
\tcol2: T.DoubleType


schema = Schema.to_schema()
'''
    assert result == expected_result


def test_compile_schema_script_spark(spark: SparkSession) -> None:
    """Test the compile_schema_script method of SparkSchemaScriptCompiler."""
    data = spark.createDataFrame(
        [
            (1, 1.0),
            (2, 2.0),
            (3, 3.0),
        ],
        ["col1", "col2"],
    )
    compiler = SparkSchemaScriptCompiler()

    result = compiler.compile_schema_script(data)

    expected_result = '''"""Pandera schema for Spark."""
import pandera.pyspark as pa  # noqa
import pyspark.sql.types as T
from pandera.pyspark import DataFrameModel

# To add more checks, use ` = pa.Field(...)` after each column
# e.g. username: T.StringType = pa.Field(str_startswith("user_"))
# refer to https://pandera.readthedocs.io/en/stable/pyspark_sql.html for more details.

class Schema(DataFrameModel):
\t"""Pandera schema."""

\tcol1: T.LongType
\tcol2: T.DoubleType


schema = Schema.to_schema()
'''
    assert result == expected_result


def test_determine_compiler_pandas() -> None:
    """Test the determine_compiler function for Pandas."""
    df_type = "pandas"

    result = determine_compiler(df_type)

    assert isinstance(result, PandasSchemaScriptCompiler)


def test_determine_compiler_spark() -> None:
    """Test the determine_compiler function for Spark."""
    df_type = "pyspark"

    result = determine_compiler(df_type)

    assert isinstance(result, SparkSchemaScriptCompiler)


def test_determine_compiler_error() -> None:
    """Test the determine_compiler function for an error."""
    df_type = "unknown"

    with pytest.raises(ValueError):
        determine_compiler(df_type)


def test_compile_type_specific_schema_script_pandas() -> None:
    """Test the compile_type_specific_schema_script function with pandas DataFrame."""
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [1.0, 2.0, 3.0]})

    result = compile_type_specific_schema_script(data)

    expected_result = '''"""Pandera schema for Pandas."""
import pandera as pa

# Insert your additional checks to `checks` list parameter for each column
# e.g. checks=[pa.Check(lambda s: s.str.len() > 0, element_wise=True)]
# refer to https://pandera.readthedocs.io/en/stable/checks.html for more details.

schema = pa.DataFrameSchema({
\t"col1": pa.Column("int64", checks=[]),
\t"col2": pa.Column("float64", checks=[]),
})
'''
    assert result == expected_result


def test_compile_type_specific_schema_script_spark(spark: SparkSession) -> None:
    """Test the compile_type_specific_schema_script function with Spark DataFrame."""
    data = spark.createDataFrame(
        [
            (1, 1.0),
            (2, 2.0),
            (3, 3.0),
        ],
        ["col1", "col2"],
    )

    result = compile_type_specific_schema_script(data)

    expected_result = '''"""Pandera schema for Spark."""
import pandera.pyspark as pa  # noqa
import pyspark.sql.types as T
from pandera.pyspark import DataFrameModel

# To add more checks, use ` = pa.Field(...)` after each column
# e.g. username: T.StringType = pa.Field(str_startswith("user_"))
# refer to https://pandera.readthedocs.io/en/stable/pyspark_sql.html for more details.

class Schema(DataFrameModel):
\t"""Pandera schema."""

\tcol1: T.LongType
\tcol2: T.DoubleType


schema = Schema.to_schema()
'''
    assert result == expected_result
