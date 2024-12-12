"""Tests for execute_schema_script module."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from acmetric.data.validators.pandera.execute_schema_script import (
    construct_module_name,
    execute_validation,
    validate_data_with_script_from_path,
)


class TestConstructModuleName(unittest.TestCase):
    """Tests for construct_module_name function."""

    @patch(
        "acmetric.data.validators.pandera.execute_schema_script.extract_relative_path"
    )
    def test_construct_module_name(self, mock_relative_path: MagicMock) -> None:
        """Test construct_module_name with valid inputs."""
        name = "test_table"
        path = Path(
            "/home/user/project_folder/project_name/src/data/validators/pandera/schemas"
        )
        mock_relative_path.return_value = Path("src/data/validators/pandera/schemas")
        expected_output = "src.data.validators.pandera.schemas.test_table"
        result = construct_module_name(name, path)
        self.assertEqual(result, expected_output)

    @patch(
        "acmetric.data.validators.pandera.execute_schema_script.extract_relative_path"
    )
    def test_construct_module_name_with_empty_name(
        self, mock_relative_path: MagicMock
    ) -> None:
        """Test construct_module_name with empty name."""
        name = ""
        path = Path(
            "/home/user/project_folder/project_name/src/data/validators/pandera/schemas"
        )
        mock_relative_path.return_value = Path("src/data/validators/pandera/schemas")
        expected_output = "src.data.validators.pandera.schemas."
        result = construct_module_name(name, path)
        self.assertEqual(result, expected_output)

    @patch(
        "acmetric.data.validators.pandera.execute_schema_script.extract_relative_path"
    )
    def test_construct_module_name_with_empty_path(
        self, mock_relative_path: MagicMock
    ) -> None:
        """Test construct_module_name with empty path."""
        name = "test_table"
        path = Path("")
        mock_relative_path.return_value = Path("")
        expected_output = "..test_table"
        result = construct_module_name(name, path)
        self.assertEqual(result, expected_output)


@patch("acmetric.data.validators.pandera.execute_schema_script.ModuleType")
def test_execute_validation(mock_module: MagicMock) -> None:
    """Test execute_validation with valid inputs."""
    mock_module.schema.validate.return_value = "validated_data"
    module = mock_module
    data = MagicMock()
    expected_output = "validated_data"
    result = execute_validation(module, data)
    assert result == expected_output


@patch("acmetric.data.validators.pandera.execute_schema_script.import_or_reload_module")
@patch("acmetric.data.validators.pandera.execute_schema_script.construct_module_name")
@patch("acmetric.data.validators.pandera.execute_schema_script.execute_validation")
def test_validate_data_with_script_from_path(
    mock_execute_validation: MagicMock,
    mock_construct_module_name: MagicMock,
    mock_import_or_reload_module: MagicMock,
) -> None:
    """Test validate_data_with_script_from_path with valid inputs."""
    mock_execute_validation.return_value = "validated_data"
    mock_construct_module_name.return_value = "module_name"
    mock_import_or_reload_module.return_value = MagicMock()
    name = "test_table"
    data = MagicMock()
    path = Path(
        "/home/user/project_folder/project_name/src/data/validators/pandera/schemas"
    )
    expected_output = "validated_data"
    result = validate_data_with_script_from_path(name, data, path)
    assert result == expected_output
