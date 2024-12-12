"""An ``mkdocs`` plugin for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from mkdocs.plugins import BasePlugin

from ..config import Config
from ..source import DefSource
from ..urljsf import Urljsf
from ..utils import import_dotted_dict
from .config import UrljsfMkdocsConfig

if TYPE_CHECKING:
    from markdown.core import Markdown
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page


PMDX_SF = "pymdownx.superfences"
ATTR_LIST = "attr_list"
ENSURE_CONFIG = [PMDX_SF, ATTR_LIST]


class UrljsfMkdocs(BasePlugin[UrljsfMkdocsConfig]):  # type: ignore[no-untyped-call]
    """An ``mkdocs`` plugin for ``urljsf``."""

    _current_page: Page | None = None
    _docs_path: Path | None = None

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Handle mkdocs configuration."""
        self._docs_path = Path(config.docs_dir)

        for ext in ENSURE_CONFIG:
            if ext not in config.markdown_extensions:
                config.markdown_extensions += [ext]

        fences: list[dict[str, Any]] = config.mdx_configs.setdefault(
            PMDX_SF, {}
        ).setdefault("custom_fences", [])
        fence = {"name": "urljsf", "format": self._fence, "class": "urljsf"}
        fences.append(fence)
        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Capture the current markdown page."""
        self._current_page = page
        return markdown

    def on_post_build(self, config: MkDocsConfig) -> None:
        """Deploy static files."""
        Urljsf.deploy_static(Path(config["site_dir"]) / "_static")

    def _fence(
        self,
        source: Any,
        language: Any,
        css_class: Any,
        options: Any,
        md: Markdown,
        classes: Any | None = None,
        id_value: str | None = "",
        attrs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        config = self._attrs_to_config(source, attrs or {})
        urljsf = Urljsf(config)
        urljsf.load_definition()
        return f"""
            <script type="module" src="{config.url_base}index.js"></script>
            {urljsf.render()}
        """

    def _attrs_to_config(self, source: str, attrs: dict[str, Any]) -> Config:
        """Convert ``sphinx-options`` to ``urljsf_options``."""
        current_page = self._current_page
        attr = attrs.get
        abs_src_path = current_page.file.abs_src_path if current_page else None

        if abs_src_path is None or self._docs_path is None:  # pragma: no cover
            msg = "don't know how to handle documents without source"
            raise NotImplementedError(msg)

        here = Path(abs_src_path).parent.resolve()
        rel = os.path.relpath(self._docs_path, here)
        path = attr("path")
        fmt = attr("format")
        definition: DefSource | None = None
        input_: str | None = None
        app_defaults: dict[str, Any] = self.config.defaults
        def_kwargs: Any = {"defaults": app_defaults, "resource_path": here}

        if path and path.startswith("py:"):
            definition = DefSource(
                raw=import_dotted_dict(path[3:]),
                **def_kwargs,
            )
        elif path:
            input_ = str(here / path)
        elif source and fmt:
            definition = DefSource(format=fmt, text=source, **def_kwargs)

        return Config(
            input_=input_,
            definition=definition,
            defaults=app_defaults,
            # meta
            template="urljsf/mkdocs.j2",
            url_base=f"{rel}/_static/urljsf/",
        )
