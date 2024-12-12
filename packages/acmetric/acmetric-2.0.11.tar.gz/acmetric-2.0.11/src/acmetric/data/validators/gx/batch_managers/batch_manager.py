"""Batch manager."""

from dataclasses import dataclass, field

from great_expectations.data_context.data_context.abstract_data_context import (
    AbstractDataContext,
)
from great_expectations.datasource.fluent import BatchRequest

from acmetric.data.abs import Data
from acmetric.data.validators.gx.batch_managers.datasource_manager import (
    DatasourceManager,
)


@dataclass
class BatchManager:
    """
    Batch manager.

    This class is used to store all the main information about the batch.

    Parameters
    ----------
    name: str
        Dataframe name.
    data: Data
        Dataframe.
    data_context: AbstractDataContext
        Data context.
    """

    name: str
    data: Data
    data_context: AbstractDataContext
    batch_request: BatchRequest = field(init=False)

    def __post_init__(self) -> None:
        """Post init."""
        self.batch_request = self.create_batch_request()

    def create_batch_request(self) -> BatchRequest:
        """Batch request."""
        datasource = DatasourceManager(
            self.data, self.data_context
        ).add_or_update_datasource()
        data_asset = datasource.add_dataframe_asset(name=self.name)
        return data_asset.build_batch_request(dataframe=self.data)
