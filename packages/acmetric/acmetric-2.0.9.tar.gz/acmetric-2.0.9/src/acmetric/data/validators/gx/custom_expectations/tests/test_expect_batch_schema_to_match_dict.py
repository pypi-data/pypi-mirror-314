"""Test ExpectBatchSchemaToMatchDict."""

from acmetric.data.validators.gx.custom_expectations.expect_batch_schema_to_match_dict import (
    ExpectBatchSchemaToMatchDict,
)


def test_expect_batch_schema_to_match_dict() -> None:
    """Test ExpectBatchSchemaToMatchDict."""
    diagnostics = ExpectBatchSchemaToMatchDict().run_diagnostics()
    assert diagnostics.errors == []
