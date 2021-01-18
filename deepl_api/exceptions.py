"""DeepL API exception classes."""


class DeeplBaseError(Exception):
    """Base class for exceptions in this module."""

    pass


class DeeplAuthorizationError(DeeplBaseError):
    """Authorization failed."""

    pass


class DeeplServerError(DeeplBaseError):
    """Received an error message from the server."""

    pass


class DeeplDeserializationError(DeeplBaseError):
    """Exception raised when deserialization the server response."""

    pass
