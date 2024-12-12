# Data Module

This module contains tools for managing data in the project. It includes classes for data catalogs, validators, and various utilities.

## Table of Contents

- [Data Catalog](#data-catalog)
- [Validators](#validators)
  - [Great Expectations validator](#great-expectations-validator)
    - [Adding expectations manually](#adding-expectations-manually)
  - [Pandera validator](#pandera-validator)
- [Usage](#usage)
- [General user flow](#general-user-flow)

## Data Catalog

The data catalog is implemented in the [`ValidatedDataCatalog`](catalog.py) class. It provides methods for loading and saving data. The data catalog is a singleton, so it can be instantiated without any parameters and provides quick access to the data catalog in your project.

The [`KedroDataCatalog`](catalogs/kedro/kedro_catalog.py) class is a specific implementation of the data catalog that uses Kedro. It can be instantiated without any parameters and provides quick access to the data catalog in your project.

## Validators

The validators are used to validate the data before it is saved to the catalog. The [`DataValidator`](abs.py) class is used for this purpose.

### Great Expectations validator

The [`GXValidator`](./validators/gx/validator.py) class is designed to be instantiated automatically and create a so-called expectation suite for each data set.

The expectation suite is created automatically based on the data set schema. If you don't want `GXValidator` to create a schema-based expectation suite, you can use `SkipExpectationAddition` as a `expectation_addition_strategy` parameter. In this case, an empty expectation suite will be created, and you can add expectations manually.

#### Adding expectations manually

To add expectations manually, follow the example below:

```python
from acmetric.data.validators.gx import (
    ConfigurationBasedExpectationAddition,
    BatchManager,
)

dataframe_batch_manager = BatchManager(
    "my_data.raw",  # name and layer according to catalog.yml
    df,  # dataframe
)

expectation_adder = ConfigurationBasedExpectationAddition()

expectations = [
    {
        "expect_column_values_to_not_be_null": {"column": "SalePrice"},
    },
    {
        "expect_column_values_to_be_between": {
            "column": "SalePrice",
            "min_value": 0,
            "max_value": 1,
        }
    },
]

expectation_adder.add_expectations(
    dataframe_batch_manager,
    expectations,
)
```

Two new expectations will be added to the expectation suite for the data set `my_data.raw`.

To update an already existing expectation, use the same method. It will automatically rewrite the expectation if it already exists.

### Pandera validator

The [`PanderaValidator`](./validators/pandera/validator.py) class is designed to be instantiated automatically and create a script containing the schema for you.

The schema is the main concept of the Pandera library. It is a set of rules that the data must follow. For more information on how this works, see the [Pandera documentation](https://pandera.readthedocs.io/en/stable/dataframe_schemas.html).

To create a schema for the data set, follow the example below:

```python
from acmetric.data.validators.pandera import PanderaValidator

validator = PanderaValidator()

validated_df = validator.validate(
    df,  # dataframe
    "my_data.raw",  # name and layer according to catalog.yml
)
```

Running this code will create a schema for the data set `my_data.raw` and save it to the `pandera` folder in the `configuration/base/` directory. The schema will be saved in the `raw.py` file in the `my_data` subfolder.

If the schema already exists, it will be loaded from the file and used to validate the data.

To add more checks to the schema, follow the instructions provided in the created file.

## Usage

To use the data catalog, define yours in the `catalog.yml` file. For more information on how to do this, see the [Kedro documentation](https://docs.kedro.org/en/stable/data/data_catalog.html).

After the catalog is defined, instantiate the class and then call the `load` or `save` methods. For example:

```python
from src.data.catalog import ValidatedDataCatalog
from src.processing import process_data  # some function that processes data

catalog = ValidatedDataCatalog()

df = catalog.load("my_data.raw")  # name and layer according to catalog.yml

processed_df = process_data(df)

catalog.save("my_data.processed", processed_df)
```

It will validate the data after loading and before saving. If the data is invalid, it will raise an exception.

## General user flow

1. Define the data catalog in the `catalog.yml` file.
2. Instantiate the data catalog class.
3. Load the data from the catalog.
4. Add more expectations to the created expectation suite if needed.
