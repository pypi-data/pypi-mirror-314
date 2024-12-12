"""Test CheckpointManager class."""

import pandas as pd
import pytest
from great_expectations.checkpoint import Checkpoint
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import EphemeralDataContext

from acmetric.data.validators.gx import (
    BatchManager,
    ConfigurationBasedExpectationAddition,
)
from acmetric.data.validators.gx.batch_managers.checkpoint_manager import (
    CheckpointManager,
)
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa
from acmetric.utils.exceptions import ValidationError


def test_checkpoint_manager_create(data_context: EphemeralDataContext) -> None:
    """Test CheckpointManager class create method."""
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
    checkpoint_manager = CheckpointManager(
        batch_manager=batch_manager,
    )
    checkpoint_manager.batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )
    assert isinstance(checkpoint_manager.checkpoint, Checkpoint)
    assert checkpoint_manager.checkpoint.name == "test_name_checkpoint"


def test_checkpoint_manager_run(data_context: EphemeralDataContext) -> None:
    """Test CheckpointManager class run method."""
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
    checkpoint_manager = CheckpointManager(
        batch_manager=batch_manager,
    )
    checkpoint_manager.batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )
    expectation_addition = ConfigurationBasedExpectationAddition()
    expectation_addition.add_expectations(
        batch_manager=batch_manager,
        expectations=[
            {
                "expect_column_values_to_be_between": {
                    "column": "col1",
                    "min_value": 1,
                    "max_value": 3,
                }
            },
            {
                "expect_column_values_to_be_between": {
                    "column": "col2",
                    "min_value": 4,
                    "max_value": 6,
                },
            },
        ],
    )
    checkpoint_result = checkpoint_manager.run_checkpoint()
    assert isinstance(checkpoint_result, CheckpointResult)
    assert checkpoint_result.success


def test_checkpoint_manager_evaluate(data_context: EphemeralDataContext) -> None:
    """Test CheckpointManager class evaluate method."""
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
    checkpoint_manager = CheckpointManager(
        batch_manager=batch_manager,
    )
    checkpoint_manager.batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )
    expectation_addition = ConfigurationBasedExpectationAddition()
    expectation_addition.add_expectations(
        batch_manager=batch_manager,
        expectations=[
            {
                "expect_column_values_to_be_between": {
                    "column": "col1",
                    "min_value": 1,
                    "max_value": 3,
                }
            },
            {
                "expect_column_values_to_be_between": {
                    "column": "col2",
                    "min_value": 4,
                    "max_value": 6,
                },
            },
        ],
    )
    checkpoint_manager.run_checkpoint_and_evaluate()


def test_checkpoint_manager_evaluate_fail(data_context: EphemeralDataContext) -> None:
    """Test CheckpointManager class evaluate method with failure."""
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
    batch_manager.data_context.add_or_update_expectation_suite(
        expectation_suite_name="test_name_suite",
    )
    expectation_addition = ConfigurationBasedExpectationAddition()
    expectation_addition.add_expectations(
        batch_manager=batch_manager,
        expectations=[
            {
                "expect_column_values_to_be_between": {
                    "column": "col1",
                    "min_value": 2,
                    "max_value": 3,
                }
            },
            {
                "expect_column_values_to_be_between": {
                    "column": "col2",
                    "min_value": 4,
                    "max_value": 6,
                },
            },
        ],
    )
    checkpoint_manager = CheckpointManager(
        batch_manager=batch_manager,
    )
    with pytest.raises(ValidationError):
        checkpoint_manager.run_checkpoint_and_evaluate()
