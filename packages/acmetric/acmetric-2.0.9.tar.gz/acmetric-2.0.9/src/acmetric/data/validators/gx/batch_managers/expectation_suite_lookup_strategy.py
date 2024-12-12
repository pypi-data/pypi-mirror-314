"""
This module contains the expectation suite lookup strategy.

The expectation suite lookup strategy is used to lookup an expectation suite in the data context.
Depending on the strategy, different actions will be taken if the expectation suite does not exist.
"""

from abc import ABC, abstractmethod

from great_expectations.data_context import AbstractDataContext
from great_expectations.exceptions import DataContextError

from acmetric.utils.exceptions import ExpectationSuiteNotFoundError


class ExpectationSuiteLookupStrategy(ABC):
    """Expectation suite lookup strategy."""

    @abstractmethod
    def _treat_expectation_suite_not_found(
        self, name: str, data_context: AbstractDataContext
    ) -> None:
        """Treat expectation suite not found."""

    @classmethod
    def lookup_expectation_suite(
        cls, name: str, data_context: AbstractDataContext
    ) -> None:
        """
        Lookup expectation suite.

        This method looks up an expectation suite in the data context.
        Depending on the strategy, different actions will be taken
        if the expectation suite does not exist.

        Parameters
        ----------
        name: str
            Name of the data to be validated.
        data_context: AbstractDataContext
            Great Expectations data context.

        Returns
        -------
        None
        """
        try:
            data_context.get_expectation_suite(expectation_suite_name=f"{name}_suite")
        except DataContextError:
            cls()._treat_expectation_suite_not_found(name, data_context)


class CustomExpectationSuiteStrategy(ExpectationSuiteLookupStrategy):
    """Raise an exception if the expectation suite does not exist."""

    def _treat_expectation_suite_not_found(
        self, name: str, data_context: AbstractDataContext
    ) -> None:
        """Raise an exception if the expectation suite does not exist."""
        error_message = f"""
        Expectation suite {name}_suite does not exist. Create it before validating data.
        Please refer to the documentation for more information:
        https://docs.greatexpectations.io/docs/guides/expectations/create_manage_expectations_lp/.
        If you are unfamiliar with Great Expectations and would like
        to easily create an expectation suite,
        consider using `InstantGXValidator` instead of `GXValidator`.
        """
        raise ExpectationSuiteNotFoundError(error_message)


class AutoExpectationSuiteCreation(ExpectationSuiteLookupStrategy):
    """Create an expectation suite if it does not exist."""

    def _treat_expectation_suite_not_found(
        self, name: str, data_context: AbstractDataContext
    ) -> None:
        """Create an expectation suite if it does not exist."""
        data_context.add_or_update_expectation_suite(
            expectation_suite_name=f"{name}_suite"
        )
