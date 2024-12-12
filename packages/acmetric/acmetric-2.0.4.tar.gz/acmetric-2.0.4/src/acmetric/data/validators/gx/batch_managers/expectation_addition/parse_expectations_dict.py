"""Parse expectation dictionary."""

from acmetric.utils.exceptions import (
    InvalidExpectationDictionaryError,
    InvalidExpectationKwargsTypeError,
    InvalidExpectationNameTypeError,
)


def parse_expectations_dict(expectation_dictionary: dict) -> tuple[str, dict]:
    """
    Parse the expectation dictionary.

    This function parses the expectation dictionary.

    Parameters
    ----------
    expectation_dictionary: `dict`
        Expectation dictionary.

    Returns
    -------
    `tuple[str, dict]`
        Expectation type and expectation kwargs.

    Examples
    --------
    >>> parse_expectations_dict(
    ...     expectation_dictionary={
    ...         "expect_column_values_to_be_in_set": {
    ...             "column": "col1",
    ...             "value_set": [1, 2, 3],
    ...         },
    ...     }
    ... )
    ('expect_column_values_to_be_in_set', {'column': 'col1', 'value_set': [1, 2, 3]})
    """
    if len(expectation_dictionary) != 1:
        raise InvalidExpectationDictionaryError(
            f"Expectation dictionary should have exactly one key, got {len(expectation_dictionary)} keys."
        )
    expectation_type = list(expectation_dictionary.keys())[0]
    expectation_kwargs = expectation_dictionary[expectation_type]
    if not isinstance(expectation_type, str):
        raise InvalidExpectationNameTypeError(
            f"Expectation type should be a string, got {type(expectation_type)}."
        )
    if not isinstance(expectation_kwargs, dict):
        raise InvalidExpectationKwargsTypeError(
            f"Expectation kwargs should be a dictionary, got {type(expectation_kwargs)}."
        )
    return expectation_type, expectation_kwargs
