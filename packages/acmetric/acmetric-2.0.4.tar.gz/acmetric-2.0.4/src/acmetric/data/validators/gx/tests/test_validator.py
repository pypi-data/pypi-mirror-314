"""Tests for Great Expectations Validator."""

from unittest.mock import MagicMock, patch

import pandas as pd
from great_expectations.data_context.data_context.ephemeral_data_context import (
    EphemeralDataContext,
)

from acmetric.data.validators.gx.batch_managers.expectation_addition_strategy import (
    SchemaExpectationAddition,
)
from acmetric.data.validators.gx.batch_managers.expectation_suite_lookup_strategy import (
    AutoExpectationSuiteCreation,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa
from acmetric.data.validators.gx.validator import GXValidator


def test_gx_validator(data_context: EphemeralDataContext) -> None:
    """Test Great Expectations Validator."""
    data = pd.DataFrame({"a": [1, 2, 3]})
    name = "test_name"
    validator = GXValidator(
        data_context=data_context,
        expectation_suite_lookup_strategy=AutoExpectationSuiteCreation(),
        expectation_addition_strategy=SchemaExpectationAddition(),
    )
    validated_data = validator.validate(name, data)
    assert isinstance(validated_data, pd.DataFrame)
    pd.testing.assert_frame_equal(validated_data, data)
    suite = data_context.get_expectation_suite(f"{name}_suite")
    assert suite.expectations[0].expectation_type == "expect_batch_schema_to_match_dict"


@patch("acmetric.data.validators.gx.validator.RepoDataContext")
def test_gx_validator_in_directory(mock_repo_data_context: MagicMock) -> None:
    """Test initializing Great Expectations Validator with a directory."""
    validator = GXValidator.in_directory("test/path")
    assert (
        validator.data_context
        == mock_repo_data_context.return_value.create.return_value
    )
    assert mock_repo_data_context.return_value.create.called_once_with()
    assert isinstance(validator, GXValidator)


def test_instant_gx_validator(data_context: EphemeralDataContext) -> None:
    """Test Instant Great Expectations Validator."""
    data = pd.DataFrame({"a": [1, 2, 3]})
    name = "test_name"

    validator = GXValidator(data_context=data_context)

    validated_data = validator.validate(name, data)

    assert isinstance(validated_data, pd.DataFrame)
    pd.testing.assert_frame_equal(validated_data, data)
    suite = data_context.get_expectation_suite(f"{name}_suite")
    assert suite.expectations[0].expectation_type == "expect_batch_schema_to_match_dict"
