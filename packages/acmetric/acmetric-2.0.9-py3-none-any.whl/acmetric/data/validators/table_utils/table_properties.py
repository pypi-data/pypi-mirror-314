"""Extract dataframe properties."""

from acmetric.data.abs import Data


def extract_dataframe_type(data: Data) -> str:
    """
    Extract dataframe type.

    This function extracts the type of the dataframe
    from the module it belongs to.
    For example, `type(pd.DataFrame()).__module__` returns string `"pandas.core.frame"`.

    Parameters
    ----------
    data : Data
        Dataframe.

    Returns
    -------
    str
        Dataframe type.
    """
    return type(data).__module__.split(".")[0]


def extract_dataframe_schema(data: Data) -> dict[str, str]:
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
    return {col_name: str(col_type) for col_name, col_type in dict(data.dtypes).items()}


def extract_dataframe_schema_spark_native_format(data: Data) -> dict[str, str]:
    """
    Extract dataframe schema in Spark native format.

    This function extracts the schema of the dataframe
    from the dtypes attribute in Spark native format.

    Parameters
    ----------
    data : Data
        Dataframe.

    Returns
    -------
    dict[str, str]
        Dictionary of column names and types.
    """
    return {x.name: str(x.dataType)[:-2] for x in list(data.schema)}  # type: ignore
