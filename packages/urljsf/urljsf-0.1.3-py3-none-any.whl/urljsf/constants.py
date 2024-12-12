"""Constants for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._schema import FileFormat

__dist__ = "urljsf"
__version__ = f"""{__import__("importlib.metadata").metadata.version(__dist__)}"""

UTF8 = {"encoding": "utf-8"}

HERE = Path(__file__).parent
TEMPLATES = HERE / "_templates"
STATIC = HERE / "_static"

SCHEMA_VERSION = "v0"
MIME_PREFIX = f"application/vnd.deathbeds.urljsf.{SCHEMA_VERSION}"


EXTENSION_FORMAT: dict[str, FileFormat] = {
    ".yaml": "yaml",
    ".toml": "toml",
    ".json": "json",
}
EXTENSION_FORMAT[".yml"] = EXTENSION_FORMAT[".yaml"]
