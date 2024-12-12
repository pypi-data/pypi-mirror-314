"""Compile schema script from dictionary of column names and types."""

from abc import ABC, abstractmethod

from acmetric.data.abs import Data
from acmetric.data.validators.table_utils.table_properties import (
    extract_dataframe_schema,
    extract_dataframe_schema_spark_native_format,
    extract_dataframe_type,
)


class SchemaScriptCompiler(ABC):
    """Schema script compiler."""

    @abstractmethod
    def extract_dataframe_schema(self, data: Data) -> dict[str, str]:
        """Extract dataframe schema."""

    @abstractmethod
    def compile_schema_string(self, df_schema: dict) -> str:
        """Compile schema string from dictionary of column names and types."""

    @abstractmethod
    def insert_schema_string_to_script(self, df_schema_string: str) -> str:
        """Insert schema string to script."""
        ...

    def compile_schema_script(self, data: Data) -> str:
        """Compile schema script from dictionary of column names and types."""
        df_schema = self.extract_dataframe_schema(data)
        df_schema_string = self.compile_schema_string(df_schema)
        schema_script = self.insert_schema_string_to_script(df_schema_string)
        return schema_script


class PandasSchemaScriptCompiler(SchemaScriptCompiler):
    """Pandas schema script compiler."""

    def extract_dataframe_schema(self, data: Data) -> dict[str, str]:
        """
        Extract dataframe schema.

        This function extracts the schema of the dataframe
        from the dtypes attribute.

        Parameters
        ----------
        data : Data
            Dataframe.

        Returns
        -------
        dict[str, str]
            Dictionary of column names and types.
        """
        return extract_dataframe_schema(data)

    def compile_schema_string(self, df_schema: dict) -> str:
        """
        Compile schema string from dictionary of column names and types.

        Parameters
        ----------
        df_schema : dict
            Dictionary of column names and types.

        Returns
        -------
        str
            Schema string.
        """
        schema_string = ""
        for col_name, col_type in df_schema.items():
            schema_string += f'\t"{col_name}": pa.Column("{col_type}", checks=[]),\n'
        return schema_string

    def insert_schema_string_to_script(self, df_schema_string: str) -> str:
        """
        Insert schema string to script.

        Parameters
        ----------
        df_schema_string : str
            Schema string.

        Returns
        -------
        str
            Schema script.
        """
        schema_script = f'''"""Pandera schema for Pandas."""
import pandera as pa

# Insert your additional checks to `checks` list parameter for each column
# e.g. checks=[pa.Check(lambda s: s.str.len() > 0, element_wise=True)]
# refer to https://pandera.readthedocs.io/en/stable/checks.html for more details.

schema = pa.DataFrameSchema({{
{df_schema_string}}})
'''
        return schema_script


class SparkSchemaScriptCompiler(SchemaScriptCompiler):
    """Spark schema script compiler."""

    def extract_dataframe_schema(self, data: Data) -> dict[str, str]:
        """
        Extract dataframe schema.

        This function extracts the schema of the dataframe
        from the dtypes attribute.

        Parameters
        ----------
        data : Data
            Dataframe.

        Returns
        -------
        dict[str, str]
            Dictionary of column names and types.
        """
        return extract_dataframe_schema_spark_native_format(data)

    def compile_schema_string(self, df_schema: dict) -> str:
        """
        Compile schema string from dictionary of column names and types.

        Parameters
        ----------
        df_schema : dict
            Dictionary of column names and types.

        Returns
        -------
        str
            Schema string.
        """
        schema_string = ""
        for col_name, col_type in df_schema.items():
            schema_string += f"\t{col_name}: T.{col_type}\n"
        return schema_string

    def insert_schema_string_to_script(self, df_schema_string: str) -> str:
        """
        Insert schema string to script.

        Parameters
        ----------
        df_schema_string : str
            Schema string.

        Returns
        -------
        str
            Schema script.
        """
        schema_script = f'''"""Pandera schema for Spark."""
import pandera.pyspark as pa  # noqa
import pyspark.sql.types as T
from pandera.pyspark import DataFrameModel

# To add more checks, use ` = pa.Field(...)` after each column
# e.g. username: T.StringType = pa.Field(str_startswith("user_"))
# refer to https://pandera.readthedocs.io/en/stable/pyspark_sql.html for more details.

class Schema(DataFrameModel):
\t"""Pandera schema."""

{df_schema_string}

schema = Schema.to_schema()
'''
        return schema_script


def determine_compiler(df_type: str) -> SchemaScriptCompiler:
    """
    Determine compiler.

    Parameters
    ----------
    df_type : str
        Dataframe type.

    Returns
    -------
    SchemaStringCompiler
        Schema string compiler.
    """
    compiler_dict = {
        "pandas": PandasSchemaScriptCompiler,
        "pyspark": SparkSchemaScriptCompiler,
    }
    if df_type not in compiler_dict.keys():
        raise ValueError(f"Dataframes of type {df_type} are not supported.")
    return compiler_dict[df_type]()


def compile_type_specific_schema_script(data: Data) -> str:
    """
    Extract dataframe type, determine compiler and compile schema script.

    Parameters
    ----------
    data : Data
        Dataframe.

    Returns
    -------
    str
        Schema script.
    """
    df_type = extract_dataframe_type(data)
    compiler = determine_compiler(df_type)
    return compiler.compile_schema_script(data)
