"""Tests for the BatchManager class."""

import pandas as pd
from great_expectations.data_context import EphemeralDataContext
from great_expectations.datasource.fluent import BatchRequest

from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager
from acmetric.data.validators.gx.data_context.tests import data_context  # noqa


def test_batch_manager(data_context: EphemeralDataContext) -> None:
    """Test that the BatchManager class creates a batch request."""
    data = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4.0, 5.0, 6.0],
            "col3": ["a", "b", "c"],
        }
    )
    batch_manager = BatchManager(
        name="test_name",
        data=data,
        data_context=data_context,
    )
    assert isinstance(batch_manager.batch_request, BatchRequest)
    assert batch_manager.batch_request.data_asset_name == "test_name"
    assert batch_manager.batch_request.datasource_name == "pandas_datasource"
