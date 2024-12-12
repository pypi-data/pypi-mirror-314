"""Fixture for a data context."""

from great_expectations.data_context import EphemeralDataContext
from great_expectations.data_context.types.base import (
    DataContextConfig,
    InMemoryStoreBackendDefaults,
)
from pytest import fixture


@fixture
def data_context() -> EphemeralDataContext:
    """Return a data context."""
    project_config = DataContextConfig(
        store_backend_defaults=InMemoryStoreBackendDefaults()
    )
    return EphemeralDataContext(project_config=project_config)
