"""General Sphinx directive for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from docutils.parsers.rst.directives import choice, uri
from sphinx.util.docutils import SphinxDirective

from ...config import Config
from ...constants import EXTENSION_FORMAT
from ...source import DefSource
from ...urljsf import Urljsf
from ...utils import import_dotted_dict
from ..nodes import urljsf

if TYPE_CHECKING:
    from docutils import nodes


def a_format(argument: str) -> str:
    """Conversion function a valid source definition."""
    return choice(argument, sorted({*EXTENSION_FORMAT.values()}))


class UrljsfDirective(SphinxDirective):
    """Base class for ``urljsf`` directives."""

    optional_arguments = 1
    has_content = True

    option_spec: ClassVar = {
        "path": uri,
        "format": a_format,
    }

    _urljsf: Urljsf | None

    def run(self) -> list[nodes.Node]:
        """Generate a single RJSF form."""
        config = self.options_to_config()
        self._urljsf = Urljsf(config)

        self._urljsf.load_definition()

        return [urljsf("", self._urljsf.render())]

    def options_to_config(self) -> Config:
        """Convert ``sphinx-options`` to ``urljsf_options``."""
        current_source = self.state.document.current_source

        if current_source is None:  # pragma: no cover
            msg = "don't know how to handle documents without source"
            raise NotImplementedError(msg)

        if self.arguments:
            self.options["path"] = self.arguments[0]

        opt = self.options.get

        here = Path(current_source).parent
        rel = os.path.relpath(self.env.app.srcdir, here)
        path = opt("path")
        fmt = opt("format")
        definition: DefSource | None = None
        input_: str | None = None
        app_defaults = self.env.config.__dict__.get("urljsf", {})

        def_kwargs = {"defaults": app_defaults, "resource_path": here}

        if path and path.startswith("py:"):
            definition = DefSource(
                raw=import_dotted_dict(path[3:]),
                **def_kwargs,
            )
        elif path:
            input_ = str(here / path)
        elif self.content and fmt:
            definition = DefSource(
                format=fmt, text="\n".join(self.content), **def_kwargs
            )

        return Config(
            input_=input_,
            definition=definition,
            defaults=app_defaults,
            # meta
            template="urljsf/sphinx.j2",
            url_base=f"{rel}/_static/urljsf-forms/",
        )
