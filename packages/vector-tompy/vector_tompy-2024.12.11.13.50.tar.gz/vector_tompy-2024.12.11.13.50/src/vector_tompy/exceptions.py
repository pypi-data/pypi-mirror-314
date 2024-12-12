class BaseVectorException(Exception):
    """Base exception for Vector project."""


class EmptyIterableError(BaseVectorException):
    """Raise when an iterable is found to be empty."""
