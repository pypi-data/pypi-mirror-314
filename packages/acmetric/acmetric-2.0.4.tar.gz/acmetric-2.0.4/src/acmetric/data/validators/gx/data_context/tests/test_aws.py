"""Test S3DataContext."""

import pytest

from acmetric.data.validators.gx.data_context.aws import S3DataContext


def test_s3_data_context() -> None:
    """Test S3DataContext."""
    data_context = S3DataContext()
    with pytest.raises(NotImplementedError):
        data_context.create()
