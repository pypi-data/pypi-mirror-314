"""Test GCPDataContext."""

import pytest

from acmetric.data.validators.gx.data_context.gcp import GCPDataContext


def test_gcp_data_context() -> None:
    """Test GCPDataContext."""
    data_context = GCPDataContext()
    with pytest.raises(NotImplementedError):
        data_context.create()
