"""Test expectation suite lookup strategy classes."""

import pytest
from great_expectations.data_context import EphemeralDataContext

from acmetric.data.validators.gx.batch_managers.expectation_suite_lookup_strategy import (
    AutoExpectationSuiteCreation,
    CustomExpectationSuiteStrategy,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa
from acmetric.utils.exceptions import ExpectationSuiteNotFoundError


def test_custom_expectation_suite_strategy_treat_expectation_suite_not_found(
    data_context: EphemeralDataContext,
) -> None:
    """Test CustomExpectationSuiteStrategy class lookup_expectation_suite method."""
    with pytest.raises(ExpectationSuiteNotFoundError):
        CustomExpectationSuiteStrategy().lookup_expectation_suite(
            name="test_name", data_context=data_context
        )


def test_auto_expectation_suite_creation_treat_expectation_suite_not_found(
    data_context: EphemeralDataContext,
) -> None:
    """Test AutoExpectationSuiteCreation class lookup_expectation_suite method."""
    AutoExpectationSuiteCreation().lookup_expectation_suite(
        name="test_name", data_context=data_context
    )
    suite = data_context.get_expectation_suite(expectation_suite_name="test_name_suite")
    suite.expectations = []
