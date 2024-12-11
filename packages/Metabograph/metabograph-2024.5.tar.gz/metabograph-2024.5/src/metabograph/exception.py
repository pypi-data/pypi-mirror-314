#!/usr/bin/env python3
"""
Exceptions.
"""


class MetabographException(Exception):
    """
    Base class for custom exceptions raised by this package.
    """


class MetabographIOError(MetabographException):
    """
    Metabograph IO error.
    """


class MetabographRuntimeError(MetabographException):
    """
    Metabograph Runtime error.
    """


class MetabographConfigError(MetabographException):
    """
    Metabograph configuration error.
    """
