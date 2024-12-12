"""Utilities for ``urljsf``."""

# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .errors import BadImportError


def import_dotted_dict(dotted: str) -> dict[str, Any]:
    """Get a JSON object from a dotted python import."""
    module_path, member = dotted.split(":")
    submodules = module_path.split(".")[1:]
    current = __import__(module_path)
    for sub in submodules:
        current = getattr(current, sub)
    candidate = getattr(current, member)
    if callable(candidate):
        candidate = candidate()

    if not isinstance(candidate, dict):  # pragma: no cover
        msg = f"Failed to resolve {dotted} as a dict, found {type(candidate)}"
        raise BadImportError(msg)

    return candidate


def merge_deep(
    left: dict[str, Any] | None, right: dict[str, Any] | None
) -> dict[str, Any]:
    """Merge dictionaries."""
    left = deepcopy(left or {})
    right = deepcopy(right or {})
    for key, value in right.items():
        if isinstance(value, dict):
            left[key] = merge_deep(left.get(key), value)
            continue
        left[key] = value
    return left
