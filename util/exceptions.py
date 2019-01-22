""" Custom errors and exceptions. """


class IllegalArgumentError(Exception):
    """
    Raised if wrong argument values are passed to functions.
    (Similar to ValueError for build-in functions.)
    """
    pass


class IllegalStateError(Exception):
    """
    Raised if application is in an illegal state.
    (e.g., values not initialized, functions not called in intended order, etc.)
    """
    pass


class IllegalConfigurationError(Exception):
    """
    Raised if an illegal configuration is provided/parsed.
    (e.g., fields missing)
    """
    pass
