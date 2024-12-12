"""Configuration for ``urljsf`` in ``mkdocs``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type


class UrljsfMkdocsConfig(Config):  # type: ignore[no-untyped-call]
    """A minimal configuration for ``urljsf`` in ``mkdocs.yml``."""

    defaults = Type(dict, default={})
