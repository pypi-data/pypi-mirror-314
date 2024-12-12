"""Create a repo-based data context."""

from pathlib import Path
from typing import Union

from great_expectations.data_context.data_context.abstract_data_context import (
    AbstractDataContext,
)
from great_expectations.data_context.data_context.file_data_context import (
    FileDataContext,
)


class RepoDataContext:
    """Data context for a repo."""

    def __init__(self, project_config_dir: Union[str, Path]) -> None:
        """
        Create a new instance of the data context.

        Parameters
        ----------
        project_config_dir: Union[str, Path]
            Path to the project configuration directory.
        """
        self.project_config_dir = project_config_dir

    def create(self) -> AbstractDataContext:
        """Create a data context stored in a repo."""
        return FileDataContext.create(project_root_dir=self.project_config_dir)
