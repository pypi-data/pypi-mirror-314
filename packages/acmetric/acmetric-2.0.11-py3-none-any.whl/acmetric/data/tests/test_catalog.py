"""Tests for validated catalog."""

import unittest
from unittest.mock import MagicMock, patch

from acmetric.data.catalog import Data, DataCatalog, DataValidator, ValidatedDataCatalog


class TestValidatedDataCatalog(unittest.TestCase):
    """Tests for ValidatedDataCatalog."""

    def setUp(self) -> None:
        """Set up."""
        self.catalog = MagicMock(spec=DataCatalog)
        self.validator = MagicMock(spec=DataValidator)
        self.validated_catalog = ValidatedDataCatalog(
            catalog=self.catalog, validator=self.validator
        )

    def test_init(self) -> None:
        """Test init."""
        self.assertEqual(self.validated_catalog.catalog, self.catalog)
        self.assertEqual(self.validated_catalog.validator, self.validator)

    @patch("acmetric.data.catalog.default_catalog")
    @patch("acmetric.data.catalog.default_validator")
    def test_in_directory(
        self, mock_validator: MagicMock, mock_catalog: MagicMock
    ) -> None:
        """Test in_directory."""
        mock_catalog.return_value = self.catalog
        mock_validator.return_value = self.validator

        validated_catalog = ValidatedDataCatalog.in_directory("path/to/config")

        self.assertEqual(validated_catalog.catalog, self.catalog)
        self.assertEqual(validated_catalog.validator, self.validator)

        mock_catalog.assert_called_once_with("path/to/config")
        mock_validator.assert_called_once_with("path/to/config")

    def test_load(self) -> None:
        """Test load."""
        name = "test_name"
        data = MagicMock(spec=Data)

        self.catalog.load.return_value = data
        self.validator.validate.return_value = data

        result = self.validated_catalog.load(name)

        self.assertEqual(result, data)
        self.catalog.load.assert_called_once_with(name)
        self.validator.validate.assert_called_once_with(name, data)

    def test_save(self) -> None:
        """Test save."""
        name = "test_name"
        data = MagicMock(spec=Data)

        self.validator.validate.return_value = data

        self.validated_catalog.save(name, data)

        self.validator.validate.assert_called_once_with(name, data)
        self.catalog.save.assert_called_once_with(name, data)
