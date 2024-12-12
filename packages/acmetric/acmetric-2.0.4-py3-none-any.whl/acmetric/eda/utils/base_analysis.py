"""
This module provides the base class for performing exploratory data analysis (EDA).

It includes:
- `ExploratoryDataAnalysis`: A base class for initializing EDA analysis.

The module uses configuration files to customize the analysis.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd

from acmetric.eda.utils.load_config import load_default_settings, merge_dicts
from acmetric.eda.utils.prepare_data import (
    convert_vertical_data_alignment_to_horizontal,
    get_data_subset,
    handle_missing_values,
)
from acmetric.logger import Logger
from acmetric.utils.load_config import get_config_directory

logger = Logger()


class ExploratoryDataAnalysis(ABC):
    """
    Base class for performing exploratory data analysis (EDA).

    This class initializes the dataset and loads default configuration settings which can be overwritten by
    user-specified settings. It provides abstract methods `analyze` and `get_default_config_name` that must be
    implemented by subclasses.

    Attributes:
        DEFAULT_CONFIG_FILE_NAME (str): Default configuration file name.
        DEFAULT_CONFIG_FOLDER (str): Default directory where configuration files are located.
        dataset (pd.DataFrame): The dataset to be analyzed.
        settings (dict): User-provided configuration settings for the analysis.

    Methods:
        _prepare_data_for_eda: Prepare the dataset for exploratory data analysis.
        analyze: Abstract method to be implemented by subclasses for performing analysis.
    """

    DEFAULT_CONFIG_FILE_NAME: str
    DEFAULT_CONFIG_FOLDER = os.path.join(get_config_directory(), "eda")

    def __init__(
        self, dataset: pd.DataFrame, settings: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Initialize the ExploratoryDataAnalysis class.

        Args:
            dataset (pd.DataFrame): The dataset to be analyzed.
            settings (Optional[dict[str, Any]]): User-provided settings to be used for analysis.
        """
        self.settings = load_default_settings(
            os.path.join(self.DEFAULT_CONFIG_FOLDER, self.DEFAULT_CONFIG_FILE_NAME)
        )

        # Overwrite default settings with user-provided settings
        if settings:
            self.settings = merge_dicts(self.settings, settings)

        self.dataset = self._prepare_data_for_eda(dataset)

    def _prepare_data_for_eda(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare the dataset for exploratory data analysis.

        This method prepares the dataset for analysis by performing any necessary
        transformations and data cleaning steps. It returns the processed dataset.

        Returns:
            pd.DataFrame: The processed dataset ready for analysis.
        """
        # Get subset of DataFrame based on settings
        processed_data = get_data_subset(dataset, self.settings)

        # Check if REQUIRED_KEYS exists in the subclass, otherwise pass empty list
        required_keys = getattr(self, "REQUIRED_KEYS", [])

        # Unstack DataFrame based on settings (only applicable for 'vertical' type data_structure)
        processed_data = convert_vertical_data_alignment_to_horizontal(
            processed_data, self.settings, required_keys
        )

        if processed_data.empty:
            error_msg = "No data available for analysis."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Process missing values based on settings
        processed_data = handle_missing_values(processed_data, self.settings)

        return processed_data

    @abstractmethod
    def analyze(self) -> None:
        """
        Abstract method to be implemented by subclasses for performing analysis.

        This method should be overridden in any subclass to define the specific analysis
        logic required for that particular implementation. The method does not return any
        value (returns `None`), and its purpose is to enforce a contract where all
        subclasses must implement their version of the analysis behavior.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
