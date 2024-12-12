"""Tests for ConfigurationBasedExpectationAddition."""

import pandas as pd
import pytest
from great_expectations.data_context import EphemeralDataContext
from great_expectations.exceptions.exceptions import (
    InvalidExpectationConfigurationError,
)

from acmetric.data.validators.gx import BatchManager
from acmetric.data.validators.gx.batch_managers.expectation_addition.configuration_based import (
    ConfigurationBasedExpectationAddition,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa


def test_add_expectations(data_context: EphemeralDataContext) -> None:
    """Test add_expectations."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    batch_manager = BatchManager(
        name="test_name",
        data=data,
        data_context=data_context,
    )
    addition = ConfigurationBasedExpectationAddition()
    expectations = [
        {
            "expect_column_values_to_be_in_set": {
                "column": "col1",
                "value_set": [1, 2, 3],
            },
        },
        {
            "expect_column_values_to_be_in_set": {
                "column": "col2",
                "value_set": [4.0, 5.0, 6.0],
            },
        },
    ]

    # Create expectation suite
    batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )

    # Add expectations
    addition.add_expectations(batch_manager, expectations)

    # Check that the expectation was added
    suite = batch_manager.data_context.get_expectation_suite("test_name_suite")
    assert len(suite.expectations) == 2
    assert suite.expectations[0].expectation_type == "expect_column_values_to_be_in_set"
    assert suite.expectations[0].kwargs == {
        "column": "col1",
        "value_set": [1, 2, 3],
    }


def test_add_invalid_xpectations(data_context: EphemeralDataContext) -> None:
    """Test add_expectations."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    batch_manager = BatchManager(
        name="test_name",
        data=data,
        data_context=data_context,
    )
    addition = ConfigurationBasedExpectationAddition()
    expectations = [
        {
            "invalid_expectation": {
                "column": "col1",
                "value_set": [1, 2, 3],
            }
        }
    ]

    # Create expectation suite
    batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )

    # assert that an error is raised
    with pytest.raises(InvalidExpectationConfigurationError):
        addition.add_expectations(batch_manager, expectations)
