"""Tests for default_attributes module."""

import unittest
from unittest.mock import MagicMock, patch

import pytest

from acmetric.data.default_attributes import default_catalog, default_validator


class TestDefaultCatalog(unittest.TestCase):
    """Tests for default_catalog function."""

    @patch("acmetric.data.default_attributes.find_spec")
    @patch("acmetric.data.catalogs.kedro.KedroDataCatalog")
    def test_kedro_installed(
        self, kedro_data_catalog: MagicMock, mock_find_spec: MagicMock
    ) -> None:
        """Test default_catalog when kedro is installed."""
        mock_find_spec.return_value = MagicMock()
        result = default_catalog("test/path")
        kedro_data_catalog.assert_called_once_with("test/path")
        assert result == kedro_data_catalog.return_value

    @patch("acmetric.data.default_attributes.find_spec")
    def test_kedro_not_installed(self, mock_find_spec: MagicMock) -> None:
        """Test default_catalog when kedro is not installed."""
        mock_find_spec.return_value = None
        with self.assertRaises(ImportError):
            default_catalog("test/path")


class TestDefaultValidator(unittest.TestCase):
    """Tests for default_validator function."""

    @patch("acmetric.data.default_attributes.find_spec")
    @patch("acmetric.data.validators.gx.GXValidator")
    def test_great_expectations_installed(
        self, gx_validator: MagicMock, mock_find_spec: MagicMock
    ) -> None:
        """Test default_validator when great_expectations is installed."""
        mock_find_spec.side_effect = [MagicMock(), None]
        result = default_validator("test/path")
        gx_validator.in_directory.assert_called_once_with("test/path")
        assert result == gx_validator.in_directory.return_value

    @patch("acmetric.data.default_attributes.find_spec")
    @patch("acmetric.data.validators.pandera.PanderaValidator")
    def test_pandera_installed(
        self, pandera_validator: MagicMock, mock_find_spec: MagicMock
    ) -> None:
        """Test default_validator when pandera is installed."""
        mock_find_spec.side_effect = [None, MagicMock()]
        with pytest.warns(
            UserWarning,
            match=(
                "Default data validator is GXValidator. "
                "Great Expectations is not installed. "
                "Using PanderaValidator instead."
            ),
        ):
            result = default_validator("test/path")
        pandera_validator.in_directory.assert_called_once_with("test/path")
        assert result == pandera_validator.in_directory.return_value

    @patch("acmetric.data.default_attributes.find_spec")
    def test_neither_package_installed(self, mock_find_spec: MagicMock) -> None:
        """Test default_validator when neither package is installed."""
        mock_find_spec.return_value = None
        with self.assertRaises(ImportError):
            default_validator("test/path")
