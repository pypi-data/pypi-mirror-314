"""Custom exceptions for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.


class UrljsfError(Exception):
    """A ``urljsf`` error."""


class InvalidInputError(UrljsfError, ValueError):
    """An error related to invalid input."""


class InvalidDefinitionError(UrljsfError, ValueError):
    """No valid definition."""


class BadImportError(UrljsfError, ValueError):
    """An unexpected import."""
