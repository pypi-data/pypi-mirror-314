"""
This module contains the BatchValidator class.

The BatchValidator class is used to validate the data. Unlike the GXValidator class, it can't be
used inside ValidatedDataCatalog. It is used to validate the data as a batch.
"""

from great_expectations.data_context import AbstractDataContext

from acmetric.data.abs import Data
from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager
from acmetric.data.validators.gx.batch_managers.checkpoint_manager import (
    CheckpointManager,
)
from acmetric.data.validators.gx.batch_managers.expectation_addition_strategy import (
    ExpectationAdditionStrategy,
)
from acmetric.data.validators.gx.batch_managers.expectation_suite_lookup_strategy import (
    ExpectationSuiteLookupStrategy,
)


def validate_dataset(
    name: str,
    data: Data,
    data_context: AbstractDataContext,
    expectation_suite_lookup_strategy: ExpectationSuiteLookupStrategy,
    expectation_addition_strategy: ExpectationAdditionStrategy,
) -> Data:
    """
    Validate the data.

    This function validates the data. It looks up the expectation suite, creates a batch request,
    adds expectations to the expectation suite, runs a checkpoint and evaluates the checkpoint.

    Parameters
    ----------
    name: `str`
        Name of the data to be validated.
    data: `Data`
        Data to be validated.
    data_context: `AbstractDataContext`
        Great Expectations data context.
    expectation_suite_lookup_strategy: `ExpectationSuiteLookupStrategy`
        Expectation suite lookup strategy.
    expectation_addition_strategy: `ExpectationAdditionStrategy`
        Expectation creation strategy.
    """
    expectation_suite_lookup_strategy.lookup_expectation_suite(name, data_context)
    batch_manager = BatchManager(name, data, data_context)
    expectation_addition_strategy.add_expectations(batch_manager)
    CheckpointManager(batch_manager).run_checkpoint_and_evaluate()
    return data
