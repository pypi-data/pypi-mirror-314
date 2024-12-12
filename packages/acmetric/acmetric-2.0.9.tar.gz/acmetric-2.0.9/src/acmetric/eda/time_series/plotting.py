"""
This module contains functions for time series plotting utilities.

The relevant functions for the module are the following:
    - time_series_eda
    - plot_line
    - plot_differenced_line
    - plot_distribution
    - plot_acf
    - plot_pacf
    - plot_qq
    - plot_generic
    - plot_stat_function
"""

from typing import Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.graphics.gofplots import qqplot as sm_qqplot
from statsmodels.graphics.tsaplots import plot_acf as sm_plot_acf
from statsmodels.graphics.tsaplots import plot_pacf as sm_plot_pacf


def time_series_eda(data: pd.DataFrame, settings: dict) -> None:
    """
    Conducts exploratory data analysis (EDA) for time series data based on settings.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    settings (dict): Dictionary of settings specifying which plots to generate.
    """
    # Disable interactive mode to keep all figures open
    plt.ioff()

    # Extract settings for plotting
    plot_type = settings.get("plotting", {}).get("type", "line")
    max_lines_per_plot = settings.get("plotting", {}).get("max_lines_per_plot", 10)
    separate_subplots = settings.get("plotting", {}).get("separate_subplots", False)
    max_number_of_subplots = settings.get("plotting", {}).get(
        "max_number_of_subplots", 10
    )

    plot_types = settings.get("plot_types", {})
    diff_lag = plot_types.get("diff_lag", 1)
    lag = plot_types.get("lag", 20)

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    # Filter data based on max lines and subplots
    columns = numeric_data.columns[:max_lines_per_plot]

    # Call specific plot functions based on settings
    if plot_types.get("line", False):
        plot_line(
            numeric_data, columns, plot_type, separate_subplots, max_number_of_subplots
        )

    if plot_types.get("differencing", False):
        plot_differenced_line(
            numeric_data,
            columns,
            diff_lag,
            plot_type,
            separate_subplots,
            max_number_of_subplots,
        )

    if plot_types.get("distribution", False):
        plot_distribution(
            numeric_data, columns, separate_subplots, max_number_of_subplots
        )

    if plot_types.get("acf", False):
        plot_acf(data, columns, lag, separate_subplots, max_number_of_subplots)

    if plot_types.get("pacf", False):
        plot_pacf(data, columns, lag, separate_subplots, max_number_of_subplots)

    if plot_types.get("qq_plot", False):
        plot_qq(numeric_data, columns, separate_subplots, max_number_of_subplots)

    # Show all figures at once
    plt.show()

    # Re-enable interactive mode
    plt.ion()


def plot_line(
    data: pd.DataFrame,
    columns: list[str],
    plot_type: str,
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot time series line charts for the specified columns.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    columns (list[str]): The columns to plot.
    plot_type (str): The type of plot (line, bar, scatter, etc.).
    separate_subplots (bool): Whether to use separate subplots for each line.
    max_number_of_subplots (int): Maximum number of subplots to display.
    """
    plot_generic(
        data, columns, plot_type, separate_subplots, max_number_of_subplots, "Line Plot"
    )


def plot_differenced_line(
    data: pd.DataFrame,
    columns: list[str],
    lag: int,
    plot_type: str,
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot the differenced time series line charts based on a specified lag.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    columns (list[str]): The columns to plot.
    lag (int): The lag to use for differencing the time series.
    plot_type (str): The type of plot (line, bar, scatter, etc.).
    separate_subplots (bool): Whether to use separate subplots for each line.
    max_number_of_subplots (int): Maximum number of subplots to display.
    """
    differenced_data = data.diff(periods=lag).dropna()
    plot_generic(
        differenced_data,
        columns,
        plot_type,
        separate_subplots,
        max_number_of_subplots,
        f"Differenced Line Plot (lag={lag})",
    )


def plot_distribution(
    data: pd.DataFrame,
    columns: list[str],
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot the distribution (histograms) of the specified columns.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data.
    columns : list[str]
        The columns to plot.
    separate_subplots : bool
        Whether to use separate subplots for each distribution.
    max_number_of_subplots : int
        Maximum number of subplots to display.

    Returns:
    --------
    None
    """
    num_plots = min(len(columns), max_number_of_subplots)

    if separate_subplots:
        plot_distribution_in_subplots(data, columns, num_plots)
    else:
        plot_distribution_in_single_plot(data, columns, num_plots)


def plot_distribution_in_subplots(
    data: pd.DataFrame,
    columns: list[str],
    num_plots: int,
) -> None:
    """
    Plot distributions (histograms) in separate subplots.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data.
    columns : list[str]
        The columns to plot.
    num_plots : int
        The number of subplots to display.

    Returns:
    --------
    None
    """
    nrows, ncols = calculate_grid(num_plots)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()  # Flatten axes for easier indexing

    for i, col in enumerate(columns[:num_plots]):
        plot_histogram_on_axis(data[col], axes[i], f"Distribution Plot - {col}")

    hide_unused_subplots(fig, axes, num_plots)
    plt.tight_layout()


def plot_distribution_in_single_plot(
    data: pd.DataFrame,
    columns: list[str],
    num_plots: int,
) -> None:
    """
    Plot distributions (histograms) for all specified columns in a single plot.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data.
    columns : list[str]
        The columns to plot.
    num_plots : int
        The number of plots to display (overlaid on a single plot).

    Returns:
    --------
    None
    """
    plt.figure(figsize=(10, 6))
    for col in columns[:num_plots]:
        data[col].plot(
            kind="hist", bins=30, alpha=0.5, label=col
        )  # Hist with transparency to avoid overlap
    plt.title("Distribution Plot")
    plt.legend()
    plt.tight_layout()


def plot_histogram_on_axis(data_column: pd.Series, ax: plt.Axes, title: str) -> None:
    """
    Plot a histogram for a single column on a specific axis.

    Parameters:
    -----------
    data_column : pd.Series
        The data for which to plot the histogram.
    ax : plt.Axes
        The axis object on which to plot the histogram.
    title : str
        The title for the subplot.

    Returns:
    --------
    None
    """
    ax.set_title(title)
    data_column.plot(kind="hist", ax=ax, bins=30)


def plot_acf(
    data: pd.DataFrame,
    columns: list[str],
    lag: int,
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot the autocorrelation function (ACF) for the specified columns.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    columns (list[str]): The columns to plot.
    lag (int): The number of lags to consider in the ACF plot.
    separate_subplots (bool): Whether to use separate subplots for each column.
    max_number_of_subplots (int): Maximum number of subplots to display.
    """
    plot_stat_function(
        sm_plot_acf,
        data,
        columns,
        lag,
        separate_subplots,
        max_number_of_subplots,
        "ACF Plot",
    )


def plot_pacf(
    data: pd.DataFrame,
    columns: list[str],
    lag: int,
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot the partial autocorrelation function (PACF) for the specified columns.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    columns (list[str]): The columns to plot.
    lag (int): The number of lags to consider in the PACF plot.
    separate_subplots (bool): Whether to use separate subplots for each column.
    max_number_of_subplots (int): Maximum number of subplots to display.
    """
    plot_stat_function(
        sm_plot_pacf,
        data,
        columns,
        lag,
        separate_subplots,
        max_number_of_subplots,
        "PACF Plot",
    )


def plot_qq(
    data: pd.DataFrame,
    columns: list[str],
    separate_subplots: bool,
    max_number_of_subplots: int,
) -> None:
    """
    Plot the quantile-quantile (QQ) plot for the specified columns.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the time series data.
    columns (list[str]): The columns to plot.
    separate_subplots (bool): Whether to use separate subplots for each column.
    max_number_of_subplots (int): Maximum number of subplots to display.
    """
    plot_stat_function(
        sm_qqplot,
        data,
        columns,
        None,
        separate_subplots,
        max_number_of_subplots,
        "QQ Plot",
        is_qq=True,
    )


def plot_stat_function(
    stat_function: Callable,
    data: pd.DataFrame,
    columns: list[str],
    lag: Optional[int],
    separate_subplots: bool,
    max_number_of_subplots: int,
    title: str,
    is_qq: bool = False,
) -> None:
    """
    Plot statistical functions like ACF, PACF, and QQ.

    Parameters:
    -----------
    stat_function : Callable
        The statistical plotting function (e.g., ACF, PACF, or QQ).
    data : pd.DataFrame
        The DataFrame containing the time series data.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    lag : Optional[int]
        The number of lags to use (ignored for QQ plot).
    separate_subplots : bool
        Whether to create separate subplots for each column.
    max_number_of_subplots : int
        Maximum number of subplots to display.
    title : str
        The title for the plot.
    is_qq : bool, optional
        Flag to indicate if the plot is a QQ plot, by default False.

    Returns:
    --------
    None
    """
    num_plots = min(len(columns), max_number_of_subplots)

    if separate_subplots:
        plot_stat_in_subplots(
            stat_function, data, columns, num_plots, lag, title, is_qq
        )
    else:
        plot_stat_in_single_plot(
            stat_function, data, columns, num_plots, lag, title, is_qq
        )


def plot_stat_in_subplots(
    stat_function: Callable,
    data: pd.DataFrame,
    columns: list[str],
    num_plots: int,
    lag: Optional[int],
    title: str,
    is_qq: bool,
) -> None:
    """
    Plot statistical functions (e.g., ACF, PACF, QQ) in separate subplots.

    Parameters:
    -----------
    stat_function : Callable
        The statistical plotting function (e.g., ACF, PACF, or QQ).
    data : pd.DataFrame
        The DataFrame containing the time series data.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    num_plots : int
        The number of subplots to display.
    lag : Optional[int]
        The number of lags to use (ignored for QQ plot).
    title : str
        The title for the plot.
    is_qq : bool
        Flag to indicate if the plot is a QQ plot.

    Returns:
    --------
    None
    """
    nrows, ncols = calculate_grid(num_plots)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()

    for i, col in enumerate(columns[:num_plots]):
        plot_stat_on_axis(
            stat_function, data[col], lag, axes[i], f"{title} - {col}", is_qq
        )

    hide_unused_subplots(fig, axes, num_plots)
    plt.tight_layout()


def plot_stat_in_single_plot(
    stat_function: Callable,
    data: pd.DataFrame,
    columns: list[str],
    num_plots: int,
    lag: Optional[int],
    title: str,
    is_qq: bool,
) -> None:
    """
    Plot statistical functions (e.g., ACF, PACF, QQ) on separate single plots.

    Parameters:
    -----------
    stat_function : Callable
        The statistical plotting function (e.g., ACF, PACF, or QQ).
    data : pd.DataFrame
        The DataFrame containing the time series data.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    num_plots : int
        The number of plots to display.
    lag : Optional[int]
        The number of lags to use (ignored for QQ plot).
    title : str
        The title for the plot.
    is_qq : bool
        Flag to indicate if the plot is a QQ plot.

    Returns:
    --------
    None
    """
    for col in columns[:num_plots]:
        _, ax = plt.subplots(figsize=(8, 4))
        plot_stat_on_axis(stat_function, data[col], lag, ax, f"{title} - {col}", is_qq)
        plt.tight_layout()


def plot_stat_on_axis(
    stat_function: Callable,
    data_column: pd.Series,
    lag: Optional[int],
    ax: plt.Axes,
    title: str,
    is_qq: bool,
) -> None:
    """
    Plot statistical function on a specific axis.

    Parameters:
    -----------
    stat_function : Callable
        The statistical plotting function (e.g., ACF, PACF, or QQ).
    data_column : pd.Series
        The specific column (series) to plot.
    lag : Optional[int]
        The number of lags to use (ignored for QQ plot).
    ax : plt.Axes
        The axis object on which to plot the data.
    title : str
        The title for the specific plot.
    is_qq : bool
        Flag to indicate if the plot is a QQ plot.

    Returns:
    --------
    None
    """
    if is_qq:
        stat_function(data_column, ax=ax)
    else:
        stat_function(
            data_column, lags=lag, ax=ax, title=None
        )  # Suppress default title
    ax.set_title(title, fontsize=12)


def plot_generic(
    data: pd.DataFrame,
    columns: list[str],
    plot_type: str,
    separate_subplots: bool,
    max_number_of_subplots: int,
    title: str,
) -> None:
    """
    Handle the generic plotting process based on the input parameters.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    plot_type : str
        The type of plot to create ("line", "bar", "scatter", etc.).
    separate_subplots : bool
        If True, create separate subplots for each column. If False, plot all columns on the same plot.
    max_number_of_subplots : int
        The maximum number of subplots or plots to display.
    title : str
        The overall title for the plot or plots.

    Returns:
    --------
    None
    """
    num_plots = min(len(columns), max_number_of_subplots)

    if separate_subplots:
        plot_in_subplots(data, columns, plot_type, num_plots, title)
    else:
        plot_in_single_plot(data, columns, plot_type, num_plots, title)


def plot_in_subplots(
    data: pd.DataFrame,
    columns: list[str],
    plot_type: str,
    num_plots: int,
    title: str,
) -> None:
    """
    Plot data in a grid of subplots when separate_subplots is True.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    plot_type : str
        The type of plot to create ("line", "bar", "scatter", etc.).
    num_plots : int
        Number of subplots to display, limited by the number of columns and max_number_of_subplots.
    title : str
        The overall title for the subplots.

    Returns:
    --------
    None
    """
    nrows, ncols = calculate_grid(num_plots)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()  # Flatten for easier iteration over axes

    for i, col in enumerate(columns[:num_plots]):
        plot_data_on_axis(data, col, plot_type, axes[i], f"{title} - {col}")

    # Hide unused subplots
    hide_unused_subplots(fig, axes, num_plots)

    plt.tight_layout()


def plot_in_single_plot(
    data: pd.DataFrame,
    columns: list[str],
    plot_type: str,
    num_plots: int,
    title: str,
) -> None:
    """
    Plot all specified columns on a single plot when separate_subplots is False.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    columns : list[str]
        list of column names from the DataFrame to be plotted.
    plot_type : str
        The type of plot to create ("line", "bar", "scatter", etc.).
    num_plots : int
        Number of plots to display, limited by the number of columns and max_number_of_subplots.
    title : str
        The title for the single plot.

    Returns:
    --------
    None
    """
    plt.figure(figsize=(10, 6))
    for col in columns[:num_plots]:
        if plot_type == "line":
            plt.plot(data.index, data[col], label=col)
        elif plot_type == "bar":
            plt.bar(data.index, data[col], label=col)
        elif plot_type == "scatter":
            plt.scatter(data.index, data[col], label=col)

    plt.title(title)
    plt.legend()
    plt.tight_layout()


def calculate_grid(num_plots: int) -> tuple[int, int]:
    """
    Calculate the number of rows and columns for the subplot grid.

    Parameters:
    -----------
    num_plots : int
        The total number of plots to display.

    Returns:
    --------
    tuple[int, int]
        A tuple representing the number of rows and columns for the grid.
    """
    grid_size = np.ceil(np.sqrt(num_plots))
    return int(grid_size), int(grid_size)


def plot_data_on_axis(
    data: pd.DataFrame, column: str, plot_type: str, ax: plt.Axes, title: str
) -> None:
    """
    Plot the data of a specific column on the given axis.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    column : str
        The specific column to plot.
    plot_type : str
        The type of plot to create ("line", "bar", "scatter", etc.).
    ax : plt.Axes
        The axis object on which to plot the data.
    title : str
        The title for the specific subplot.

    Returns:
    --------
    None
    """
    ax.set_title(title)
    if plot_type == "line":
        data[column].plot(ax=ax)
    elif plot_type == "bar":
        data[column].plot(kind="bar", ax=ax)
    elif plot_type == "scatter":
        ax.scatter(data.index, data[column])


def hide_unused_subplots(fig: plt.Figure, axes: np.ndarray, num_plots: int) -> None:
    """
    Hide any unused subplots if the number of plots is less than the grid size.

    Parameters:
    -----------
    fig : plt.Figure
        The figure object containing the subplots.
    axes : np.ndarray
        The array of axes (subplots).
    num_plots : int
        The number of plots that are actually being used.

    Returns:
    --------
    None
    """
    for j in range(num_plots, len(axes)):
        fig.delaxes(axes[j])
