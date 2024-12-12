"""Build structured data files for pull requests with JSON schema."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from .constants import __version__
from .urljsf import Urljsf

__all__ = ["Urljsf", "__version__"]
