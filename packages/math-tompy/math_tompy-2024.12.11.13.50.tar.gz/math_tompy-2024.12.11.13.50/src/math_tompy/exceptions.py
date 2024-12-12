class BaseMathException(Exception):
    """Base exception for math project."""


class EmptyListError(BaseMathException):
    """Raise when a list is found to be empty"""
