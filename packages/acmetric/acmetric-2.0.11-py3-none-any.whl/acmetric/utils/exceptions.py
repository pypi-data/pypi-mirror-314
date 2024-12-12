"""Custom exceptions."""


class ValidationError(Exception):
    """Raised when a validation check fails."""


class ExpectationSuiteNotFoundError(Exception):
    """Raised when an expectation suite is not found."""


class InvalidExpectationDictionaryError(Exception):
    """Raised when an expectation dictionary is invalid."""


class InvalidExpectationNameTypeError(Exception):
    """Raised when type of expectation name is invalid."""


class InvalidExpectationKwargsTypeError(Exception):
    """Raised when type of expectation kwargs is invalid."""
