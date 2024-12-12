"""Tests for NoValidator."""

import unittest

import pandas as pd

from acmetric.data.validators.no_validator import NoValidator


class TestNoValidator(unittest.TestCase):
    """Tests for NoValidator."""

    def setUp(self) -> None:
        """Set up."""
        self.validator = NoValidator()

    def test_validate(self) -> None:
        """Test validate."""
        name = "test_name"
        data = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
            }
        )

        result = self.validator.validate(name, data)

        pd.testing.assert_frame_equal(result, data)
