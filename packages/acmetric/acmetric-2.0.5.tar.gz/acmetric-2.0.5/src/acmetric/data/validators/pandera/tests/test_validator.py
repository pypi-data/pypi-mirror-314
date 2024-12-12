"""Tests for Pandera Validator."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from acmetric.data.validators.pandera.validator import PanderaValidator


def test_pandera_validator_init() -> None:
    """Test the initialization of PanderaValidator."""
    validator = PanderaValidator("test/path")
    assert validator.config_path == Path("test/path/pandera_schemas")


def test_pandera_validator_in_directory() -> None:
    """Test the in_directory method of PanderaValidator."""
    path = "test/path"
    validator = PanderaValidator.in_directory(path)
    assert validator.config_path == Path(path) / "pandera_schemas"


@patch("acmetric.data.validators.pandera.validator.validate_data")
def test_pandera_validator_validate(mock_validate_data: MagicMock) -> None:
    """Test the validate method of PanderaValidator."""
    # Arrange
    mock_data = MagicMock()
    mock_validate_data.return_value = mock_data
    validator = PanderaValidator("test/path")
    name = "test_schema"

    # Act
    result = validator.validate(name, mock_data)

    # Assert
    mock_validate_data.assert_called_once_with(name, mock_data, validator.config_path)
    assert result == mock_data
