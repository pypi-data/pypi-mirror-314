"""Test AzureDataContext."""

import pytest

from acmetric.data.validators.gx.data_context.azure import AzureDataContext


def test_azure_data_context() -> None:
    """Test AzureDataContext."""
    data_context = AzureDataContext()
    with pytest.raises(NotImplementedError):
        data_context.create()
