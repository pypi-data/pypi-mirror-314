"""Create an S3-based data context."""

from great_expectations.data_context import AbstractDataContext


class S3DataContext:
    """Data context for S3."""

    def create(self) -> AbstractDataContext:
        """Create a data context stored in an S3 bucket."""
        raise NotImplementedError
