"""Test batch_validation module."""

import pandas as pd
import pytest
from great_expectations.data_context import EphemeralDataContext

from acmetric.data.validators.gx.batch_managers.batch_validation import validate_dataset
from acmetric.data.validators.gx.batch_managers.expectation_addition_strategy import (
    SchemaExpectationAddition,
    SkipExpectationAddition,
)
from acmetric.data.validators.gx.batch_managers.expectation_suite_lookup_strategy import (
    AutoExpectationSuiteCreation,
    CustomExpectationSuiteStrategy,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa
from acmetric.utils.exceptions import ExpectationSuiteNotFoundError


def test_validate_dataset(
    data_context: EphemeralDataContext,
) -> None:
    """Test validate_dataset function."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    name = "test_name"
    dataset = validate_dataset(
        name=name,
        data=data,
        data_context=data_context,
        expectation_suite_lookup_strategy=AutoExpectationSuiteCreation(),
        expectation_addition_strategy=SchemaExpectationAddition(),
    )
    pd.testing.assert_frame_equal(dataset, data)
    suite = data_context.get_expectation_suite(expectation_suite_name="test_name_suite")
    assert (
        suite.expectations[0]["expectation_type"] == "expect_batch_schema_to_match_dict"
    )
    assert len(suite.expectations) == 1


def test_validate_dataset_custom_expectation_suite_lookup(
    data_context: EphemeralDataContext,
) -> None:
    """Test validate_dataset function with custom expectation suite lookup strategy."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    name = "test_name"
    with pytest.raises(ExpectationSuiteNotFoundError):
        validate_dataset(
            name=name,
            data=data,
            data_context=data_context,
            expectation_suite_lookup_strategy=CustomExpectationSuiteStrategy(),
            expectation_addition_strategy=SchemaExpectationAddition(),
        )


def test_validate_dataset_skip_expectation_addition(
    data_context: EphemeralDataContext,
) -> None:
    """Test validate_dataset function with SkipExpectationAddition class."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    name = "test_name"
    dataset = validate_dataset(
        name=name,
        data=data,
        data_context=data_context,
        expectation_suite_lookup_strategy=AutoExpectationSuiteCreation(),
        expectation_addition_strategy=SkipExpectationAddition(),
    )
    pd.testing.assert_frame_equal(dataset, data)
    suite = data_context.get_expectation_suite(expectation_suite_name="test_name_suite")
    assert suite.expectations == []
