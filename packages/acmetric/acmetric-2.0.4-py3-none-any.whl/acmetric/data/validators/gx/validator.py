"""Great Expectations validators."""

from pathlib import Path
from typing import Optional, Union

from great_expectations.data_context.data_context.abstract_data_context import (
    AbstractDataContext,
)

from acmetric.data.abs import Data
from acmetric.data.validators.gx.batch_managers import (
    AutoExpectationSuiteCreation,
    ExpectationAdditionStrategy,
    ExpectationSuiteLookupStrategy,
    SchemaExpectationAddition,
    validate_dataset,
)
from acmetric.data.validators.gx.data_context import RepoDataContext


class GXValidator:
    """
    Great Expectations validator.

    This validator creates a data context and an expectation suite if they do not exist.
    During the instantiation, the class creates a data context in the default location
    defined in the passed Data Context object.

    If no expectation suite is found for the data to be validated,
    the class will "freeze" the dataframe schema and create an expectation suite out of it.
    "Freezing" the dataframe schema means that the validator will fix the column list
    and the column types of the dataframe. Next time the data is validated,
    the validator will expect the dataframe to have the same schema.

    It is also possible to pass custom data context, expectation suite lookup strategy,
    and expectation addition strategy.

    Parameters
    ----------
    data_context: AbstractDataContext
        Great Expectations data context. Defaults to repo-based data context.
    expectation_suite_lookup_strategy: ExpectationSuiteLookupStrategy
        Expectation suite lookup strategy. Defaults to AutoExpectationSuiteCreation.
    expectation_addition_strategy: ExpectationAdditionStrategy
        Expectation creation strategy. Defaults to SchemaExpectationAddition.
    """

    __slots__ = [
        "data_context",
        "expectation_suite_lookup_strategy",
        "expectation_addition_strategy",
    ]

    def __init__(
        self,
        data_context: AbstractDataContext,
        expectation_suite_lookup_strategy: Optional[
            ExpectationSuiteLookupStrategy
        ] = None,
        expectation_addition_strategy: Optional[ExpectationAdditionStrategy] = None,
    ) -> None:
        """
        Create a new instance of the Great Expectations validator.

        You can either pass the path to the repo context directory or the data context object.

        Parameters
        ----------
        data_context: AbstractDataContext
            Great Expectations data context.
        expectation_suite_lookup_strategy: Optional[ExpectationSuiteLookupStrategy]
            Expectation suite lookup strategy. Defaults to AutoExpectationSuiteCreation.
        expectation_addition_strategy: Optional[ExpectationAdditionStrategy]
            Expectation creation strategy. Defaults to SchemaExpectationAddition.

        Raises
        ------
        ValueError
            If neither `repo_context_dir` nor `data_context` is provided.

        Examples
        --------
        >>> validator = GXValidator(repo_context_dir="path/to/repo")
        >>> validator = GXValidator(data_context=data_context)
        """
        self.data_context = data_context
        self.expectation_suite_lookup_strategy = (
            expectation_suite_lookup_strategy or AutoExpectationSuiteCreation()
        )
        self.expectation_addition_strategy = (
            expectation_addition_strategy or SchemaExpectationAddition()
        )

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "GXValidator":
        """
        Create a new instance of the Great Expectations validator with a repo-based data context.

        Parameters
        ----------
        path: Union[str, Path]
            Path to the configuration directory.

        Returns
        -------
        GXValidator
            Great Expectations validator.
        """
        return cls(data_context=RepoDataContext(path).create())

    def validate(self, name: str, data: Data) -> Data:
        """
        Validate data.

        This method creates a checkpoint (or updates it if it already exists) and runs it.
        If the checkpoint fails, it raises a `ValidationError`.

        Parameters
        ----------
        name: str
            Name of the data to be validated.
        data: Data
            Data to be validated.

        Returns
        -------
        Data
            Validated data.

        Raises
        ------
        ValidationError
            If the data is invalid.
        ExpectationSuiteNotFoundError
            If the expectation suite for the dataset does not exist.
        """
        return validate_dataset(
            name,
            data,
            self.data_context,
            self.expectation_suite_lookup_strategy,
            self.expectation_addition_strategy,
        )
