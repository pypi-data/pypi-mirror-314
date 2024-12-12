"""Create a GCP-based data context."""

from great_expectations.data_context import AbstractDataContext


class GCPDataContext:
    """Data context for GCP."""

    def create(self) -> AbstractDataContext:
        """Create a data context stored in a GCP bucket."""
        raise NotImplementedError
