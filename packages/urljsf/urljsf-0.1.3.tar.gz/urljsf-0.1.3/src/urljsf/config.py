"""Configuration for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .source import DefSource


@dataclass
class Config:
    """Configuration for ``urljsf``."""

    input_: str | None
    definition: DefSource | None = None
    defaults: dict[str, Any] | None = None

    # meta...
    url_base: str = "./"
    # end up as ``data-`` attributes..
    # cli...
    html_filename: str = "index.html"
    html_title: str | None = None
    output_dir: Path = Path("./_urljsf_output")
    template: str = "urljsf/standalone.j2"
    extra_template_paths: list[Path] = field(default_factory=list)
    # app...
    log_level: str = "DEBUG"
    # more?


DEFAULTS = {fn: f.default for fn, f in Config.__dataclass_fields__.items()}
