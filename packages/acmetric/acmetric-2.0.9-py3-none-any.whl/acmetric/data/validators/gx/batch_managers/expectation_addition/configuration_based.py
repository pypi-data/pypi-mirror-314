"""Configuration-based expectation addition."""

from typing import Dict, List

from great_expectations.expectations.expectation import ExpectationConfiguration

from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager
from acmetric.data.validators.gx.batch_managers.expectation_addition.parse_expectations_dict import (
    parse_expectations_dict,
)


class ConfigurationBasedExpectationAddition:
    """
    Configuration-based expectation addition.

    This class adds expectations to the expectation suite based on a configuration.
    """

    def add_expectations(
        self, batch_manager: BatchManager, expectations: List[Dict]
    ) -> None:
        """
        Add expectations to the expectation suite.

        This method adds expectations based on a configuration.

        Parameters
        ----------
        batch_manager: BatchManager
            Batch manager.
        expectations: List[Dict]
            List of dictionaries containing the expectation configuration.

        Examples
        --------
        >>> ConfigurationBasedExpectationAddition(...).add_expectations(
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
        suite = batch_manager.data_context.get_expectation_suite(
            expectation_suite_name=f"{batch_manager.name}_suite"
        )
        for expectation in expectations:
            expectation_type, expectation_kwargs = parse_expectations_dict(
                expectation_dictionary=expectation
            )
            expectation_configuration = ExpectationConfiguration(
                expectation_type=expectation_type,
                kwargs=expectation_kwargs,
            )
            suite.add_expectation(expectation_configuration)
        batch_manager.data_context.update_expectation_suite(suite)
