"""Exploratory Data Analysis (EDA) example file."""

import os

import pandas as pd

from acmetric.eda.time_series.analysis import TimeSeries

# Example usage
if __name__ == "__main__":
    # Load example data
    data_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            os.pardir,
            "data",
            "elnino.csv",
        )
    )

    data = pd.read_csv(data_folder)

    # data = pd.DataFrame({
    #     'time': [2000, 2000, 2001, 2001],
    #     'entity': ['USA', 'Canada', 'USA', 'Canada'],
    #     'value': [10, 20, 15, 25]
    # })

    # print(data)

    # Initialize TimeSeries and CrossSectional analyses with default settings
    time_series_eda = TimeSeries(data)
    # cross_sectional_eda = CrossSectional(data)

    # Run analyses
    time_series_eda.analyze()
    # cross_sectional_eda.analyze()
