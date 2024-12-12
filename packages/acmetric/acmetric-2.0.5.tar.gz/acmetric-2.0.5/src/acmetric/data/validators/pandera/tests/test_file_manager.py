"""Tests for FileManager class."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from acmetric.data.validators.pandera.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Tests for FileManager class."""

    def setUp(self) -> None:
        """Set up."""
        self.name = "test_folder.test_file"
        self.path = Path("/test_path")
        self.file_manager = FileManager(self.name, self.path)

    def test_post_init(self) -> None:
        """Test __post_init__ method."""
        self.assertEqual(
            self.file_manager.file_path, self.path / "test_folder" / "test_file.py"
        )

    @patch("acmetric.data.validators.pandera.file_manager.check_if_file_exists")
    def test_check_if_file_exists(self, mock_check_if_file_exists: MagicMock) -> None:
        """Test check_if_file_exists method."""
        mock_check_if_file_exists.return_value = True
        result = self.file_manager.check_if_file_exists()
        self.assertTrue(result)
        mock_check_if_file_exists.assert_called_once_with(self.file_manager.file_path)

    @patch(
        "acmetric.data.validators.pandera.file_manager.create_file_in_directory_if_not_exists"
    )
    def test_create_directory_and_empty_file(
        self, mock_create_file_in_directory_if_not_exists: MagicMock
    ) -> None:
        """Test create_directory_and_empty_file method."""
        self.file_manager.create_directory_and_empty_file()
        mock_create_file_in_directory_if_not_exists.assert_called_once_with(
            self.file_manager.file_path
        )

    def test_split_table_name_into_subfolder_and_filename(self) -> None:
        """Test split_table_name_into_subfolder_and_filename method."""
        result = self.file_manager.split_table_name_into_subfolder_and_filename()
        self.assertEqual(result, ("test_folder", "test_file.py"))

    def test_create_full_path(self) -> None:
        """Test create_full_path method."""
        result = self.file_manager.create_full_path()
        self.assertEqual(result, self.path / "test_folder" / "test_file.py")

    @patch("acmetric.data.validators.pandera.file_manager.write_string_to_file")
    def test_write_file(self, mock_write_string_to_file: MagicMock) -> None:
        """Test write_file method."""
        string = "test_string"
        self.file_manager.write_file(string)
        mock_write_string_to_file.assert_called_once_with(
            string, self.file_manager.file_path
        )
