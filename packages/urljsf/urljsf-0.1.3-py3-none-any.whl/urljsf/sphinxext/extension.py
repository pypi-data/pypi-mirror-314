"""A sphinx extension for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..urljsf import Urljsf
from .nodes import urljsf

if TYPE_CHECKING:
    from sphinx.application import Sphinx


ROOT_CLASS = "urljsf-form"


def build_finished(app: Sphinx, _err: Exception | None) -> None:
    """Copy all static assets."""
    static = Path(app.builder.outdir) / "_static"

    Urljsf.deploy_static(Path(app.builder.outdir) / static)


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: Any,
) -> None:
    """Add JS/CSS to the page."""
    if not doctree or not doctree.traverse(urljsf):
        return

    app.add_js_file("urljsf/index.js", type="module")
    app.add_css_file(
        "urljsf/index.js",
        rel="modulepreload",
        type=None,
    )
