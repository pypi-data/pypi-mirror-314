"""Validator-based expectation addition."""

from typing import Dict, List

from great_expectations.validator.validator import Validator

from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager
from acmetric.data.validators.gx.batch_managers.expectation_addition.parse_expectations_dict import (
    parse_expectations_dict,
)


class ValidatorBasedExpectationAddition:
    """
    Validator-based expectation addition.

    This class adds expectations to the expectation suite based on a validator.
    """

    def add_expectations(
        self, batch_manager: BatchManager, expectations: List[Dict]
    ) -> None:
        """
        Add expectations to the expectation suite.

        This method adds expectations to the expectation suite based on a validator.

        Parameters
        ----------
        batch_manager: BatchManager
            Batch manager.
        expectations: List[Dict]
            List of dictionaries containing the expectation configuration.

        Examples
        --------
        >>> ValidatorBasedExpectationAddition(...).add_expectations(
        ...     batch_manager,
        ...     expectations=[
        ...         {
        ...             "expect_column_values_to_be_in_set": {
        ...                 "column": "col1",
        ...                 "value_set": [1, 2, 3],
        ...             },
        ...         },
        ...         {
        ...             "expect_column_values_to_be_in_set": {
        ...                 "column": "col2",
        ...                 "value_set": [4.0, 5.0, 6.0],
        ...             },
        ...         },
        ...     ]
        ... )
        """
        validator = create_batch_validator(batch_manager)
        for expectation in expectations:
            expectation_name, kwargs = parse_expectations_dict(
                expectation_dictionary=expectation
            )
            getattr(validator, expectation_name)(**kwargs)
            validator.save_expectation_suite()


def create_batch_validator(batch_manager: BatchManager) -> Validator:
    """
    Create a batch validator.

    This method creates a batch validator. This is a part of the Great Expectations API.
    This validator is not the same as the one used in the `validate` method.

    Parameters
    ----------
    batch_manager: BatchManager
        Batch manager.

    Returns
    -------
    Validator
        Batch validator.
    """
    validator = batch_manager.data_context.get_validator(
        batch_request=batch_manager.batch_request,
        expectation_suite_name=f"{batch_manager.name}_suite",
    )
    return validator
