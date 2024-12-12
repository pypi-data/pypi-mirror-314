"""
This module contains functions for printing of statistics for eda.

The relevant functions for the module are the following:
    - print_summary_statistics
    - print_jarque_bera_test
    - print_stationarity_test
    - print_ljung_box_test
    - print_time_series_statistics
"""

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera
from statsmodels.tsa.stattools import adfuller


def collect_summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Compute summary statistics for each column in the input DataFrame.

    This function returns common summary statistics (e.g., mean, standard deviation, min, max, and quartiles)
    for each numerical column in the DataFrame using `pd.DataFrame.describe`.

    Args:
        data (pd.DataFrame): A DataFrame containing numerical data.

    Returns:
        pd.DataFrame: A DataFrame with summary statistics for each column.
                      Returns an empty DataFrame if the input is empty.
    """
    if data.empty:
        return pd.DataFrame()  # Return an empty DataFrame for empty input
    return data.describe()


def collect_jarque_bera_test(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform the Jarque-Bera test for normality on each column of the input DataFrame.

    The Jarque-Bera test checks whether sample data has the skewness and kurtosis matching
    a normal distribution. It returns a DataFrame with the test statistic, p-value, skewness,
    and kurtosis for each column.

    Args:
        data (pd.DataFrame): A DataFrame containing numerical data.

    Returns:
        pd.DataFrame: A DataFrame where each column corresponds to a variable from the input DataFrame,
                      and the rows provide the JB statistic, p-value, skewness, and kurtosis for each.
    """
    results = {}

    for column in data.columns:
        jb_stat, jb_p_value, skew, kurtosis = jarque_bera(data[column])
        results[column] = {
            "JB Statistic": jb_stat,
            "P-value": jb_p_value,
            "Skewness": skew,
            "Kurtosis": kurtosis,
        }
    return pd.DataFrame(results)


def collect_stationarity_test(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform the Augmented Dickey-Fuller (ADF) test for stationarity on each column of the input DataFrame.

    The ADF test checks for the presence of unit roots in time series data,
    indicating whether a series is stationary. The result includes the test statistic, p-value,
    and critical values at 1%, 5%, and 10% significance levels.

    Args:
        data (pd.DataFrame): A DataFrame containing time series data.

    Returns:
        pd.DataFrame: A DataFrame where each column corresponds to a variable from the input DataFrame,
                      and the rows provide the ADF statistic, p-value, and critical values for each.
    """
    results = {}

    for column in data.columns:
        adf_stat, p_value, _, _, critical_values, _ = adfuller(data[column])
        results[column] = {
            "ADF Statistic": adf_stat,
            "P-value": p_value,
            "1% Critical": critical_values["1%"],
            "5% Critical": critical_values["5%"],
            "10% Critical": critical_values["10%"],
        }
    return pd.DataFrame(results)


def collect_ljung_box_test(data: pd.DataFrame, max_lag: int) -> pd.DataFrame:
    """
    Perform the Ljung-Box test for autocorrelation on each column of the input DataFrame.

    The Ljung-Box test checks whether any of a group of autocorrelations
    of a time series are significantly different from zero. It returns a DataFrame with
    p-values for each lag from 1 to the specified max_lag.

    Args:
        data (pd.DataFrame): A DataFrame containing time series data.
        max_lag (int): The maximum number of lags to test for autocorrelation.

    Returns:
        pd.DataFrame: A DataFrame where each column corresponds to a variable from the input DataFrame,
                      and the rows provide p-values for each lag from 1 to max_lag.

    Raises:
        ValueError: If max_lag is not a positive integer.
    """
    if max_lag < 1:
        raise ValueError("max_lag must be a positive integer.")

    results = {}

    for column in data.columns:
        ljung_box_test = acorr_ljungbox(
            data[column], lags=list(range(1, max_lag + 1)), return_df=True
        )
        results[column] = ljung_box_test["lb_pvalue"]
    return pd.DataFrame(results)


def print_time_series_statistics(data: pd.DataFrame, settings: dict) -> None:
    """
    Print time series statistics for each column in the given DataFrame based on the specified settings.

    This function organizes statistical tests by type (rather than by column), providing a consolidated view
    of the results for multiple time series. It performs the following tests depending on the settings:

    1. **Summary Statistics**: Basic descriptive statistics for each series (mean, standard deviation, quartiles, etc.).
    2. **Jarque-Bera Test**: A test for checking if the data is normally distributed, reporting the JB statistic,
       p-value, skewness, and kurtosis.
    3. **ADF Test (Stationarity)**: The Augmented Dickey-Fuller test for stationarity, returning the ADF statistic,
       p-value, and critical values.
    4. **Ljung-Box Test**: A test for detecting autocorrelation in the data, reporting p-values for up to a specified
       number of lags.

    Each test result is printed in a tabular format for easier comparison across all columns. The function also provides
    an explanation and interpretation of the results after each test output, helping users understand the implications
    of the test results.

    Parameters:
    ----------
    data : pd.DataFrame
        A pandas DataFrame containing the time series data, where each column represents a different series.

    settings : dict
        A dictionary containing test configurations and parameters. Expected keys are:

        - 'statistics': A dictionary with the following possible boolean keys:
            - 'summary_statistics': If True, prints summary statistics for each column.
            - 'normality_test': If True, performs the Jarque-Bera normality test for each column.
            - 'stationarity_test': If True, performs the ADF test for stationarity on each column.
            - 'autocorrelation_test': If True, performs the Ljung-Box test for autocorrelation on each column.
            - 'max_lag': (Optional) Specifies the maximum lag to use in the Ljung-Box test. Default is 10.

    Returns:
    -------
    None
        This function prints the results of the selected statistical tests and does not return any value.

    Examples:
    --------
    >>> settings = {
            'statistics': {
                'summary_statistics': True,
                'normality_test': True,
                'stationarity_test': True,
                'autocorrelation_test': True,
                'max_lag': 10  # Maximum lag for autocorrelation test
            }
        }
    >>> print_time_series_statistics(data, settings)

    The output will be a series of tables showing the results of the selected tests for all columns in the DataFrame,
    along with interpretations such as:
    - For the Jarque-Bera test, a low p-value indicates non-normality.
    - For the ADF test, a low p-value suggests that the series is stationary.
    - For the Ljung-Box test, a low p-value indicates significant autocorrelation.
    """
    statistics_settings = settings.get("statistics", {})
    max_lag = statistics_settings.get("max_lag", 10)  # Default to 10 if not provided

    # Summary statistics
    if statistics_settings.get("summary_statistics", False):
        print("\n=== Summary Statistics ===")
        summary_stats = collect_summary_statistics(data)
        print(summary_stats)
        print("\nInterpretation:\nThese are basic statistics for each series.\n")

    # Jarque-Bera test
    if statistics_settings.get("normality_test", False):
        print("\n=== Jarque-Bera Normality Test ===")
        jb_test = collect_jarque_bera_test(data)
        print(jb_test.T)  # Transpose to display columns in rows
        print(
            "\nInterpretation:\n"
            "The Jarque-Bera test checks if the data is normally distributed.\nA low p-value (< 0.05) "
            "indicates non-normality, while a high p-value indicates the data is likely normally distributed.\n"
        )

    # Stationarity test (ADF Test)
    if statistics_settings.get("stationarity_test", False):
        print("\n=== Augmented Dickey-Fuller (ADF) Test for Stationarity ===")
        adf_test = collect_stationarity_test(data)
        print(adf_test.T)
        print(
            "\nInterpretation:\n"
            "The ADF test checks for stationarity in the time series.\nA low p-value (< 0.05) suggests "
            "that the series is stationary, while a higher p-value indicates the series is non-stationary.\n"
            "The critical values show thresholds for rejecting the null hypothesis.\n"
        )

    # Ljung-Box test
    if statistics_settings.get("autocorrelation_test", False):
        print(f"\n=== Ljung-Box Test for Autocorrelation (up to {max_lag} lags) ===")
        ljung_box_test = collect_ljung_box_test(data, max_lag)
        print(ljung_box_test)
        print(
            "\nInterpretation:\n"
            "The Ljung-Box test checks for autocorrelation in the time series.\nA low p-value (< 0.05) indicates "
            "significant autocorrelation, suggesting that the series is not independently distributed at the "
            "given lag.\n"
        )
