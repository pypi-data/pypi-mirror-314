"""Unit tests for the KedroDataCatalog class."""

import unittest
from unittest.mock import MagicMock, patch

from acmetric.data.abs import Data
from acmetric.data.catalogs.kedro.kedro_catalog import KedroDataCatalog


class TestKedroDataCatalog(unittest.TestCase):
    """Unit tests for the KedroDataCatalog class."""

    def setUp(self) -> None:
        """Set up."""
        self.config_loader = MagicMock()

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_init(
        self,
        mock_create_catalog: MagicMock,
        # mock_create_templated_config_loader: MagicMock,
    ) -> None:
        """Test that the data catalog is initialized correctly."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)

        mock_create_catalog.assert_called_once_with(self.config_loader)
        self.assertEqual(kedro_data_catalog._catalog, mock_catalog)

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_load(self, mock_create_catalog: MagicMock) -> None:
        """Test that the data catalog loads data correctly."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog
        mock_data = MagicMock(spec=Data)
        mock_catalog.load.return_value = mock_data

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        result = kedro_data_catalog.load("test_data")

        mock_catalog.load.assert_called_once_with("test_data")
        self.assertEqual(result, mock_data)

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_load_with_query(self, mock_create_catalog: MagicMock) -> None:
        """Test that the data catalog loads data correctly with a query."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog
        mock_data = MagicMock(spec=Data)
        mock_catalog.load.return_value = mock_data

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        kedro_data_catalog._catalog._data_sets["test_data"]._load_args = {
            "query": "{query_arg}"
        }
        result = kedro_data_catalog.load("test_data", query_arg="test_query")

        mock_catalog.load.assert_called_once_with("test_data")
        assert (
            kedro_data_catalog._catalog._data_sets["test_data"]._load_args["query"]
            == "{query_arg}"
        )
        self.assertEqual(result, mock_data)

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_load_with_query_not_supported(
        self, mock_create_catalog: MagicMock
    ) -> None:
        """Test that the data catalog raises an error when loading data with a query that is not supported."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        kedro_data_catalog._catalog._data_sets["test_data"]._load_args = {}
        with self.assertRaises(ValueError):
            kedro_data_catalog.load("test_data", query_arg="test_query")

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_save(self, mock_create_catalog: MagicMock) -> None:
        """Test that the data catalog saves data correctly."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog
        mock_data = MagicMock(spec=Data)

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        kedro_data_catalog._catalog = mock_catalog
        kedro_data_catalog.save("test_data", mock_data)

        mock_catalog.save.assert_called_once_with("test_data", mock_data)

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_load_with_dynamic_query(self, mock_create_catalog: MagicMock) -> None:
        """Test that the data catalog loads data with a dynamic query correctly."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        kedro_data_catalog._catalog._data_sets = {
            "test_data": MagicMock(_load_args={"query": "{query_arg}"})
        }
        kedro_data_catalog._load_with_dynamic_query("test_data", query_arg="test_query")

        assert (
            kedro_data_catalog._catalog._data_sets["test_data"]._load_args["query"]
            == "{query_arg}"
        )

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    def test_load_with_dynamic_query_not_supported(
        self, mock_create_catalog: MagicMock
    ) -> None:
        """Test that the data catalog raises an error when loading data with a dynamic query that is not supported."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog

        kedro_data_catalog = KedroDataCatalog("test/config/path", self.config_loader)
        kedro_data_catalog._catalog._data_sets = {"test_data": MagicMock(_load_args={})}
        with self.assertRaises(ValueError):
            kedro_data_catalog._load_with_dynamic_query(
                "test_data", query_arg="test_query"
            )

    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_catalog")
    @patch("acmetric.data.catalogs.kedro.kedro_catalog.create_templated_config_loader")
    def test_in_directory(
        self,
        mock_create_templated_config_loader: MagicMock,
        mock_create_catalog: MagicMock,
    ) -> None:
        """Test that the data catalog is initialized correctly with a directory path."""
        mock_catalog = MagicMock()
        mock_create_catalog.return_value = mock_catalog

        kedro_data_catalog = KedroDataCatalog.in_directory("test/config/path")

        mock_create_catalog.assert_called_once_with(
            mock_create_templated_config_loader.return_value
        )
        self.assertEqual(kedro_data_catalog._catalog, mock_catalog)
