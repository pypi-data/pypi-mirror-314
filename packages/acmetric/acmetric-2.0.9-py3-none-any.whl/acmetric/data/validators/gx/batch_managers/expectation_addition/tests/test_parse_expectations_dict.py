"""Tests for parse_expectations_dict function."""

import unittest

from acmetric.data.validators.gx.batch_managers.expectation_addition.parse_expectations_dict import (
    InvalidExpectationDictionaryError,
    InvalidExpectationKwargsTypeError,
    InvalidExpectationNameTypeError,
    parse_expectations_dict,
)


class TestParseExpectationsDict(unittest.TestCase):
    """Tests for parse_expectations_dict function."""

    def test_parse_expectations_dict_valid_input(self) -> None:
        """Test parse_expectations_dict function with valid input."""
        expectation_dictionary = {
            "expect_column_values_to_be_in_set": {
                "column": "col1",
                "value_set": [1, 2, 3],
            },
        }
        expectation_type, expectation_kwargs = parse_expectations_dict(
            expectation_dictionary
        )
        self.assertEqual(expectation_type, "expect_column_values_to_be_in_set")
        self.assertEqual(expectation_kwargs, {"column": "col1", "value_set": [1, 2, 3]})

    def test_parse_expectations_dict_multiple_keys(self) -> None:
        """Test parse_expectations_dict function with multiple keys."""
        expectation_dictionary = {
            "expect_column_values_to_be_in_set": {
                "column": "col1",
                "value_set": [1, 2, 3],
            },
            "expect_column_values_to_be_of_type": {"column": "col2", "type": "int"},
        }
        with self.assertRaises(InvalidExpectationDictionaryError):
            parse_expectations_dict(expectation_dictionary)

    def test_parse_expectations_dict_invalid_expectation_type(self) -> None:
        """Test parse_expectations_dict function with invalid expectation type."""
        expectation_dictionary = {123: {"column": "col1", "value_set": [1, 2, 3]}}
        with self.assertRaises(InvalidExpectationNameTypeError):
            parse_expectations_dict(expectation_dictionary)

    def test_parse_expectations_dict_invalid_expectation_kwargs(self) -> None:
        """Test parse_expectations_dict function with invalid expectation kwargs."""
        expectation_dictionary = {"expect_column_values_to_be_in_set": "invalid"}
        with self.assertRaises(InvalidExpectationKwargsTypeError):
            parse_expectations_dict(expectation_dictionary)
