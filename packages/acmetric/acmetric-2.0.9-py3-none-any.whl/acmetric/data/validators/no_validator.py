"""Validators that do not validate."""

from acmetric.data.abs import Data


class NoValidator:
    """A validator that does not validate the data."""

    def validate(self, name: str, data: Data) -> Data:
        """Return the data without validating it."""
        return data
