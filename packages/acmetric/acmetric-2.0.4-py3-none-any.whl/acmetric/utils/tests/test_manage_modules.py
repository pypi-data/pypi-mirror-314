"""Tests for manage_modules module."""

import importlib
import sys
import unittest
from types import ModuleType
from unittest.mock import MagicMock, patch

from acmetric.utils.manage_modules import import_or_reload_module


class TestImportOrReloadModule(unittest.TestCase):
    """Tests for import_or_reload_module function."""

    def test_import_module(self) -> None:
        """Test import_or_reload_module with a module that is not in sys.modules."""
        name = "math"
        if name in sys.modules:
            del sys.modules[name]
        result = import_or_reload_module(name)
        self.assertIsInstance(result, ModuleType)
        self.assertEqual(result.__name__, name)

    def test_reload_module(self) -> None:
        """Test import_or_reload_module with a module that is already in sys.modules."""
        name = "math"
        importlib.import_module(name)
        result = import_or_reload_module(name)
        self.assertIsInstance(result, ModuleType)
        self.assertEqual(result.__name__, name)

    def test_import_module_with_invalid_name(self) -> None:
        """Test import_or_reload_module with an invalid module name."""
        name = "invalid_module_name"
        with self.assertRaises(ModuleNotFoundError):
            import_or_reload_module(name)

    @patch("acmetric.utils.manage_modules.importlib.import_module")
    @patch("acmetric.utils.manage_modules.importlib.reload")
    def test_import_module_already_exist(
        self, mock_reload: MagicMock, mock_import_module: MagicMock
    ) -> None:
        """Test import_or_reload_module with a module that is already in sys.modules."""
        name = "math"
        mock_import_module.return_value = ModuleType(name)
        mock_reload.return_value = ModuleType(name)
        sys.modules[name] = mock_import_module.return_value
        result = import_or_reload_module(name)
        self.assertIsInstance(result, ModuleType)
        self.assertEqual(result.__name__, name)
        mock_import_module.assert_not_called()
        mock_reload.assert_called_once_with(sys.modules[name])
