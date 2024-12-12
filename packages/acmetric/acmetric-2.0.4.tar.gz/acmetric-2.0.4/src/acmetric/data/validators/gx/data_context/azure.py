"""Create an Azure-based data context."""

from great_expectations.data_context import AbstractDataContext


class AzureDataContext:
    """Data context for Azure."""

    def create(self) -> AbstractDataContext:
        """Create a data context stored in an Azure blob storage."""
        raise NotImplementedError
