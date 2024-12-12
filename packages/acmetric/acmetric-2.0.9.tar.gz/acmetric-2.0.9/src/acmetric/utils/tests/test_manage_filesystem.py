"""Test manage_filesystem.py."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from acmetric.utils.manage_filesystem import (
    check_if_file_exists,
    create_directory,
    create_file,
    create_file_in_directory_if_not_exists,
    extract_relative_path,
    write_string_to_file,
)


@patch("acmetric.utils.manage_filesystem.Path")
def test_extract_relative_path(mock_path: MagicMock) -> None:
    """Test extract_relative_path with valid inputs."""
    path = mock_path
    path.relative_to.return_value = Path("src/data/validators/pandera/schemas")
    expected_output = Path("src/data/validators/pandera/schemas")
    result = extract_relative_path(path)
    assert result == expected_output


@patch("acmetric.utils.manage_filesystem.open")
def test_write_string_to_file(mock_open: MagicMock) -> None:
    """Test write_string_to_file with valid inputs."""
    mock_open.return_value = MagicMock()
    string = "test_string"
    path = Path("test_path")
    write_string_to_file(string, path)
    mock_open.assert_called_once_with(path, "w")
    mock_open.return_value.__enter__.return_value.write.assert_called_once_with(string)


@patch("acmetric.utils.manage_filesystem.Path")
def test_check_if_file_exists(mock_path: MagicMock) -> None:
    """Test check_if_file_exists with valid inputs."""
    mock_path.exists.return_value = True
    path = mock_path
    expected_output = True
    result = check_if_file_exists(path)
    assert result == expected_output


@patch("acmetric.utils.manage_filesystem.Path")
def test_create_directory(mock_path: MagicMock) -> None:
    """Test create_directory with valid inputs."""
    mock_path.mkdir.return_value = None
    path = mock_path
    create_directory(path)
    mock_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)


@patch("acmetric.utils.manage_filesystem.Path")
def test_create_file(mock_path: MagicMock) -> None:
    """Test create_file with valid inputs."""
    mock_path.touch.return_value = None
    path = mock_path
    create_file(path)
    mock_path.touch.assert_called_once_with()


@patch("acmetric.utils.manage_filesystem.create_directory")
@patch("acmetric.utils.manage_filesystem.create_file")
@patch("acmetric.utils.manage_filesystem.check_if_file_exists")
@patch("acmetric.utils.manage_filesystem.Path")
def test_create_file_in_directory_if_not_exists(
    mock_path: MagicMock,
    mock_check_if_file_exists: MagicMock,
    mock_create_file: MagicMock,
    mock_create_directory: MagicMock,
) -> None:
    """Test create_file_in_directory_if_not_exists with valid inputs."""
    mock_check_if_file_exists.return_value = False
    path = mock_path
    create_file_in_directory_if_not_exists(path)
    mock_check_if_file_exists.assert_called_once_with(path)
    mock_create_directory.assert_called_once_with(path.parent)
    mock_create_file.assert_called_once_with(path)
