"""Module for managing python modules."""

import importlib
import sys
from types import ModuleType


def import_or_reload_module(name: str) -> ModuleType:
    """
    Import or reload module.

    This function imports or reloads module.

    Parameters
    ----------
    name : str
        Name of the module.

    Returns
    -------
    ModuleType
        Module.
    """
    if name in sys.modules:
        return importlib.reload(sys.modules[name])
    else:
        return importlib.import_module(name)
