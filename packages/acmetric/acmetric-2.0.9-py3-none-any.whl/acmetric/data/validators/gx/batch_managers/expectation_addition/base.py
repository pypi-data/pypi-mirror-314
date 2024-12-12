"""Expectation addition base class."""

from typing import Dict, List, Protocol

from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager


class ExpectationAddition(Protocol):
    """Expectation addition."""

    def add_expectations(
        self, batch_manager: BatchManager, expectations: List[Dict]
    ) -> None:
        """Add expectations to the expectation suite."""
        ...
