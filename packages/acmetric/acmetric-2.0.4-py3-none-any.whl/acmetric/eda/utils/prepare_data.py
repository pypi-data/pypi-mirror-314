"""
This module contains utility functions for general EDA purposes.

The relevant functions for the module are the following:
    - convert_vertical_data_alignment_to_horizontal
    - get_data_subset
"""

from typing import Any

import numpy as np
import pandas as pd

from acmetric.logger import Logger

logger = Logger()


def convert_vertical_data_alignment_to_horizontal(
    data: pd.DataFrame, settings: dict[str, Any], required_keys: list[str]
) -> pd.DataFrame:
    """
    Transform a vertically stacked DataFrame into an unstacked format based on settings.

    If the data structure type in the settings is 'vertical', the function will pivot the DataFrame
    so that each unique entity becomes a separate column, and the values are filled accordingly.

    If the data structure type is not 'vertical', the original DataFrame is returned as is.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to be transformed. It should have the columns specified
        in the 'time_series' section of the settings if the data type is 'vertical'.

    settings : dict[str, Any]
        A dictionary representing the configuration settings loaded from a YAML file. It should include
        the following structure:
        - data_structure:
            - type: 'vertical' or other (only 'vertical' triggers the transformation)
            - time_series:
                - entity_column: column containing entities
                - value_column: column containing values
                - time_column: column containing time information
    required_keys : list[str]
        A list of required keys that should be present in the 'time_series' section of the settings.

    Returns:
    --------
    pd.DataFrame
        The transformed DataFrame if the data type is 'vertical', otherwise the original DataFrame.

    Raises:
    -------
    KeyError
        If the 'time_series' section or required keys ('entity_column', 'value_column', 'time_column')
        are missing in the settings for 'vertical' data.

    ValueError
        If any of the required columns ('entity_column', 'value_column', 'time_column') are missing in the DataFrame.

    Example:
    --------
    >>> settings = {
            'data_structure': {
                'type': 'vertical',
                'time_series': {
                    'entity_column': 'entity',
                    'value_column': 'value',
                    'time_column': 'time'
                }
            }
        }
    >>> data = pd.DataFrame({
            'entity': ['A', 'A', 'B', 'B'],
            'value': [10, 15, 20, 25],
            'time': [1, 2, 1, 2]
        })
    >>> unstacked_df = convert_vertical_data_alignment_to_horizontal(data, settings)
    >>> print(unstacked_df)
       time   A   B
    0     1  10  20
    1     2  15  25
    """
    # Extract relevant settings from the YAML structure
    data_type = settings.get("data_structure", {}).get("type")

    # If the data type is not 'vertical', return the DataFrame as is
    if data_type == "horizontal":
        return data

    # Ensure the required keys exist in the settings
    time_series_settings = settings.get("data_structure", {}).get("time_series", {})

    if not time_series_settings:
        error_msg = "The 'time_series' section is missing in the settings."
        logger.error(error_msg)
        raise KeyError(error_msg)

    # Ensure the required keys exist in settings
    validate_missing_keys(time_series_settings, required_keys)

    # Extract the required column names from the settings
    entity_column = time_series_settings["entity_column"]
    value_column = time_series_settings["value_column"]
    time_column = time_series_settings["time_column"]

    # Ensure the required columns exist in the DataFrame
    validate_columns_exist(data, entity_column, value_column, time_column)

    # Unstack the DataFrame and return
    return unstack_dataframe(data, entity_column, value_column, time_column)


def unstack_dataframe(
    data: pd.DataFrame, entity_column: str, value_column: str, time_column: str
) -> pd.DataFrame:
    """
    Unstack the DataFrame by converting long-format data into a wide-format DataFrame.

    Long-format data has observations stacked vertically and the result of unstacking is a wide-format DataFrame,
    where each unique value of the entity column becomes a separate column.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame containing the data to be unstacked. It should contain at least three columns:
        one representing time, one representing entities (e.g., different variables or groups), and one
        representing values.

    entity_column : str
        The name of the column in the DataFrame that represents the entities (e.g., regions, products, or categories).
        Each unique value in this column will become a separate column in the unstacked DataFrame.

    value_column : str
        The name of the column in the DataFrame that contains the values that should be unstacked. This is the data
        that will populate the cells of the resulting wide-format DataFrame.

    time_column : str
        The name of the column in the DataFrame that represents time (or another sequential variable). This column
        will be used as the index in the unstacked DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame in wide format, where each unique value from the `entity_column` becomes a separate column. The
        index of the returned DataFrame is based on the `time_column`, and the values come from the `value_column`.

    Raises
    ------
    ValueError
        If the specified `entity_column`, `value_column`, or `time_column` do not exist in the input DataFrame.

    Notes
    -----
    This function assumes that the input DataFrame is in long format, meaning that observations are stored in rows,
    with each row representing a specific entity at a given time. The function uses the `pivot` method to transform
    the data into a wide format. It then ensures that the columns of the resulting DataFrame are flattened (i.e.,
    no MultiIndex is retained) and resets the index to treat the time variable as a regular column.

    Example
    -------
    Suppose you have a DataFrame `df` with the following structure:

    >>> df = pd.DataFrame({
    >>>     'year': [2000, 2000, 2001, 2001],
    >>>     'country': ['USA', 'Canada', 'USA', 'Canada'],
    >>>     'gdp': [10, 20, 15, 25]
    >>> })

    If you call the function:

    >>> unstack_dataframe(df, entity_column='country', value_column='gdp', time_column='year')

    The result will be:

    >>>    year   USA  Canada
    >>>    2000    10     20
    >>>    2001    15     25
    """
    # Use pivot to unstack the DataFrame
    df_unstacked = data.pivot(
        index=time_column, columns=entity_column, values=value_column
    )

    # Flatten the columns (to remove MultiIndex if created)
    df_unstacked.columns.name = None

    # Reset the index to have the time_column as a regular column
    df_unstacked.reset_index(inplace=True)

    return df_unstacked


def validate_columns_exist(data: pd.DataFrame, *columns: str) -> None:
    """
    Check if the specified columns are missing in the DataFrame.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to check for missing columns.

    *columns : str
        Variable number of strings representing the column names to check in the DataFrame.

    Raises:
    -------
    ValueError
        If any of the specified columns are missing in the DataFrame.

    Example:
    --------
    >>> data = pd.DataFrame({
            'entity': ['A', 'A', 'B', 'B'],
            'value': [10, 15, 20, 25],
            'time': [1, 2, 1, 2]
        })
    >>> validate_columns_exist(data, 'entity', 'value', 'time')
    """
    missing_columns = [col for col in columns if col not in data.columns]

    if missing_columns:
        error_msg = f"Missing columns in DataFrame: {', '.join(missing_columns)}"
        logger.error(error_msg)
        raise ValueError(error_msg)


def validate_missing_keys(settings: dict[str, Any], required_keys: list[str]) -> None:
    """
    Check if the required keys are missing in the settings.

    Parameters:
    -----------
    settings : dict
        A dictionary containing the settings to be checked for missing keys.

    required_keys : list
        A list of strings representing the keys that are required in the settings.

    Raises:
    -------
    KeyError
        If any of the required keys are missing in the settings.

    Example:
    --------
    >>> settings = {
            'entity_column': 'entity',
            'value_column': 'value',
            'time_column': 'time'
        }
    >>> required_keys = ['entity_column', 'value_column', 'time_column']
    >>> validate_missing_keys(settings, required_keys)
    """
    missing_keys = [key for key in required_keys if key not in settings]

    if missing_keys:
        error_msg = f"Missing keys in the settings: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise KeyError(error_msg)


def get_data_subset(data: pd.DataFrame, settings: dict[str, Any]) -> pd.DataFrame:
    """
    Return a subset of the DataFrame based on the settings.

    Parameters:
    data (pd.DataFrame): The input DataFrame from which the subset will be extracted.
    settings (dict): A dictionary containing the data selection settings.

    Settings Structure:
    settings = {
        'data_selection': {
            'column_names': list of str,  # List of column names to include in the subset
            'include_all_columns': bool,  # If True, include all columns from the DataFrame
            'max_number_of_columns': int,  # Maximum number of columns to include in the subset
            'max_number_of_rows': int  # Maximum number of rows to include in the subset
        }
    }

    Returns:
    pd.DataFrame: A subset of the input DataFrame based on the provided settings.
    """
    data_selection = settings.get("data_selection", {})

    # Determine columns to include
    columns = determine_columns_to_include(data, settings)

    # Determine rows to include
    max_rows = data_selection.get("max_number_of_rows", len(data))
    if max_rows is None:
        max_rows = len(data)

    # Return the subset of the DataFrame
    return data.loc[: max_rows - 1, columns]


def determine_columns_to_include(
    data: pd.DataFrame, settings: dict[str, Any]
) -> list[str]:
    """
    Determine the columns to include in the subset based on the settings.

    Parameters:
    data (pd.DataFrame): The input DataFrame from which the subset will be extracted.
    settings (dict): A dictionary containing the data selection settings.

    Returns:
    list[str]: A list of column names to include in the subset.
    """
    data_structure = settings.get("data_structure", {})
    data_selection = settings.get("data_selection", {})
    include_all_columns = data_selection.get("include_all_columns", False)
    data_structure_type = data_structure.get("type")

    if include_all_columns or data_structure_type == "vertical":
        return data.columns.tolist()

    columns = data_selection.get("column_names", [])
    if not columns:
        columns = data.columns
    else:
        # Check if provided column names exist in the DataFrame
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            logger.warning(
                f"The following columns are not in the DataFrame: {missing_columns}"
            )
        columns = [col for col in columns if col in data.columns]

    max_columns = data_selection.get("max_number_of_columns", len(columns))
    if max_columns is None:
        max_columns = len(columns)

    return columns[:max_columns]


def handle_missing_values(data: pd.DataFrame, settings: dict[str, Any]) -> pd.DataFrame:
    """
    Handle missing values in a DataFrame based on the strategy specified in the provided settings dictionary.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data with potential missing values.
    settings : dict
        A dictionary containing the missing values handling configuration.

    Returns:
    --------
    pd.DataFrame
        The cleaned DataFrame with missing values handled according to the provided strategy.

    Settings dictionary should contain:
    -----------------------------------
    data_handling:
      missing_values: 'ignore'  # How to handle missing values ('drop', 'fill', 'ignore', 'interpolate')
      fill_value: 0  # Value to fill missing data if 'fill' is chosen

    Raises:
    -------
    ValueError:
        If an unknown missing values strategy is provided or the fill value is invalid for the 'fill' strategy.
    KeyError:
        If the expected configuration keys are missing in the settings dictionary.
    """
    missing_values_strategy = settings.get("data_handling", {}).get(
        "missing_values", "ignore"
    )
    fill_value = settings.get("data_handling", {}).get("fill_value", 0)

    # Check if the fill_value is appropriate
    if missing_values_strategy == "fill" and not isinstance(
        fill_value, (int, float, str)
    ):
        error_msg = f"Invalid fill_value: {fill_value}. Expected int, float, or str."
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Handle missing values based on the specified strategy
    if missing_values_strategy == "drop":
        df_cleaned = data.dropna().reset_index(
            drop=True
        )  # Reset index after dropping rows
    elif missing_values_strategy == "fill":
        df_cleaned = data.fillna(fill_value)
    elif missing_values_strategy == "interpolate":
        df_cleaned = data.interpolate()

        # Forward fill for NaNs at the start, and backward fill for NaNs at the end
        df_cleaned = df_cleaned.ffill().bfill()
    elif missing_values_strategy == "ignore":
        df_cleaned = data  # Do nothing, leave missing values as-is
    else:
        error_msg = f"Unknown missing values strategy: {missing_values_strategy}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    return df_cleaned


def drop_non_numeric_columns(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Log the names of columns that were dropped because they are not numeric.

    Args:
        dataset (pd.DataFrame): The original dataset from which numeric data is selected.

    Returns:
        pd.DataFrame: A DataFrame with only numeric columns.
    """
    # Select only numeric columns
    numeric_data = dataset.select_dtypes(include=[np.number])

    # Get the dropped columns
    dropped_columns = dataset.columns.difference(numeric_data.columns)

    # Log dropped columns
    if not dropped_columns.empty:
        logger.info(
            f"Columns dropped due to not being numeric: {list(dropped_columns)}"
        )

    return numeric_data
