"""
This module provides a class for performing exploratory data analysis (EDA) on cross-sectional data.

The module uses configuration files to customize the analysis.
"""

from acmetric.eda.utils.base_analysis import ExploratoryDataAnalysis


class CrossSectional(ExploratoryDataAnalysis):
    """
    Class for performing cross-sectional-specific exploratory data analysis.

    Methods:
        analyze: Run cross-sectional specific analysis.
    """

    DEFAULT_CONFIG_FILE_NAME = "cs_parameters.yaml"

    def analyze(self) -> None:
        """Run cross-sectional specific analysis."""
