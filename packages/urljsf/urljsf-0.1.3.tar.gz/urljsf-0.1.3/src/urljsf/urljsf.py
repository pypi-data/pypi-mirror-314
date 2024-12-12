"""Main application for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from logging import Logger, getLogger
from pathlib import Path
from typing import TYPE_CHECKING

import jinja2

from .constants import MIME_PREFIX, STATIC, TEMPLATES, __dist__
from .errors import InvalidDefinitionError, InvalidInputError
from .source import DefSource

if TYPE_CHECKING:
    from ._schema import Urljsf as UrljsfSchema
    from .config import Config


class Urljsf:
    """Main class for ``urljsf``."""

    config: Config
    log: Logger
    env: jinja2.Environment

    def __init__(self, config: Config) -> None:
        """Initialize a urljsf."""
        self.log = getLogger(__dist__)
        self.config = config
        self.log.setLevel(self.config.log_level)
        self.log.debug("urljsf config: %s", self.config)
        self.init_env()

    def init_env(self) -> None:
        """Prepare a jinja environment."""
        loader = jinja2.FileSystemLoader(
            searchpath=[TEMPLATES, *self.config.extra_template_paths],
        )
        self.env = jinja2.Environment(
            loader=loader, undefined=jinja2.StrictUndefined, autoescape=True
        )

    def run_cli(self) -> int:
        """Generate output."""
        cfg = self.config
        self.log.debug("config: %s", cfg)
        self.load_definition()

        if not cfg.definition:  # pragma: no cover
            self.log.error("No definition found %s", self.config)
            return 1
        if cfg.definition.validation_errors:  # pragma: no cover
            self.log.error(
                "Found validation errors: %s", cfg.definition.validation_errors
            )
            return 2

        rendered = self.render()
        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        out_html = cfg.output_dir / cfg.html_filename
        out_html.write_text(rendered, encoding="utf-8")
        self.deploy_static(cfg.output_dir / "_static")
        return 0

    def load_definition(self) -> None:
        """Load a configuration from a file or dotted python module."""
        if self.config.definition:
            return

        cfg = self.config

        if cfg.input_ is None:  # pragma: no cover
            msg = f"No valid input from {cfg}"
            raise InvalidInputError(msg)

        input_path = Path(cfg.input_)

        if input_path.exists():
            cfg.definition = DefSource(input_path, defaults=cfg.defaults, log=self.log)
        else:  # pragma: no cover
            msg = f"No form definition found in {self.config}"
            raise InvalidDefinitionError(msg)

    @property
    def definition(self) -> UrljsfSchema:
        """Get the validated source."""
        bad = self.config.definition is None or self.config.definition.data is None
        if bad:  # pragma: no cover
            msg = f"No form definition found in {self.config}"
            raise InvalidDefinitionError(msg)
        return self.config.definition.data  # type: ignore[return-value,union-attr]

    def render(self) -> str:
        """Render a template."""
        cfg = self.config
        self.log.debug("rendering: %s", cfg)
        tmpl = self.env.get_template(cfg.template)
        context = dict(cfg.__dict__)
        context.update(definition_json=self.definition, mime_prefix=MIME_PREFIX)
        return tmpl.render(context)

    @staticmethod
    def deploy_static(path: Path) -> None:
        """Copy the static assets into the right place."""
        for child in (STATIC / "urljsf").rglob("*"):
            if child.is_dir():
                continue
            rel = str(child.relative_to(STATIC))
            dest = path / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(child.read_bytes())
