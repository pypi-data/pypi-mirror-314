"""Test RepoDataContext."""

import unittest
from unittest.mock import MagicMock, patch

from great_expectations.data_context.data_context.abstract_data_context import (
    AbstractDataContext,
)
from great_expectations.data_context.data_context.file_data_context import (
    FileDataContext,
)

from acmetric.data.validators.gx.data_context.repo import RepoDataContext


class TestRepoDataContext(unittest.TestCase):
    """Tests for RepoDataContext."""

    def setUp(self) -> None:
        """Set up."""
        self.repo_data_context = RepoDataContext("test/path")

    @patch.object(FileDataContext, "create")
    def test_create(self, mock_create: MagicMock) -> None:
        """Test create."""
        mock_create.return_value = MagicMock(spec=AbstractDataContext)

        result = self.repo_data_context.create()

        self.assertIsInstance(result, AbstractDataContext)
        mock_create.assert_called_once_with(project_root_dir="test/path")
