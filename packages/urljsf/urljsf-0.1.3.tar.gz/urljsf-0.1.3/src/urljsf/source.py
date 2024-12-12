"""Configuration for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

from ._schema import Urljsf as UrljsfSchema
from .constants import EXTENSION_FORMAT, UTF8
from .schema import URLJSF_VALIDATOR
from .utils import import_dotted_dict, merge_deep

if TYPE_CHECKING:
    from pathlib import Path

    from jsonschema.protocols import Validator


@dataclass
class DataSource:
    """Parsed data from a source."""

    path: Path | None = None
    raw: dict[str, Any] | None = None
    text: str | None = None
    format: str | None = None
    log: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))

    def __post_init__(self) -> None:
        """Trigger parsing."""
        self.parse()

    def suffix(self) -> str:
        """Get the file type suffix."""
        if TYPE_CHECKING:
            assert self.path

        return self.path.suffix

    def read_text(self) -> str:
        """Get the source of a path."""
        if TYPE_CHECKING:
            assert self.path
        return self.path.read_text(**UTF8)

    def guess_format(self) -> str:
        """Guess the format from a suffix."""
        suffix = self.suffix()
        fmt = EXTENSION_FORMAT.get(suffix)
        if TYPE_CHECKING:
            assert fmt is not None
        return fmt

    def parse(self) -> None:
        """Parse a path."""
        if self.raw:
            return

        fmt = self.format = self.format or self.guess_format()
        text = self.text = self.text or self.read_text()

        if fmt == "toml":
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib  # type: ignore[no-redef]

            self.raw = tomllib.loads(text)
        elif fmt == "yaml":
            from ruamel.yaml import YAML

            self.raw = YAML(typ="safe").load(text)
        elif fmt == "json":
            self.raw = json.loads(text)
            self.format = "json"
        else:  # pragma: no cover
            msg = f"Can't parse {self.format}: {self.path}"
            raise NotImplementedError(msg)
        self.log.debug("parsed %s: %s", self.format, self.path)


@dataclass
class ValidatedSource(DataSource):
    """A validated source."""

    validator: Draft7Validator | None = None
    validation_errors: list[Any] = field(default_factory=list)
    as_type: Callable[..., Any] = field(default_factory=lambda: lambda: dict)
    data: Any | None = None
    defaults: dict[str, Any] | None = None

    def parse(self) -> None:
        """Validate, and attempt to parse the data."""
        super().parse()
        if not self.validator:  # pragma: no cover
            msg = f"No validator for {self.__class__.__name__}"
            raise NotImplementedError(msg)
        if self.raw is None:  # pragma: no cover
            msg = f"No data for {self.__class__.__name__}"
            raise NotImplementedError(msg)

        self.raw = merge_deep(self.defaults, self.raw)
        self.validate()

        self.data = self.as_type(**self.raw)

    def validate(self) -> None:
        """Capture validation errors."""
        self.validation_errors = (
            [*self.validator.iter_errors(self.raw)] if self.validator else []
        )


@dataclass
class DefSource(ValidatedSource):
    """A validated ``urljsf`` definition."""

    data: UrljsfSchema | None = None
    as_type: Callable[..., UrljsfSchema] = field(default_factory=lambda: UrljsfSchema)
    validator: Draft7Validator = field(default_factory=lambda: URLJSF_VALIDATOR)
    resource_path: Path | None = None

    def parse(self) -> None:
        """Extend parsing with path resolution."""
        super().parse()

        if self.raw is None:  # pragma: no cover
            msg = f"unexpected empty raw data {self}"
            raise NotImplementedError(msg)

        for form_name, form in self.raw.get("forms", {}).items():
            if form is None:
                continue
            self.parse_form(form_name, form)

    def parse_form(self, form_name: str, form: dict[str, Any]) -> None:
        """Parse common fields of a single form."""
        schema: dict[str, Any] | None = None

        for key in ["schema", "ui_schema", "props", "form_data"]:
            value = form.get(key)
            if value is None:
                continue
            if isinstance(value, str):
                form[key] = self.resolve_url(value)
            if key == "schema":
                schema = form[key]

        if not schema:  # pragma: no cover
            return

        validator_cls: type[Validator] = validator_for(schema, default=Draft7Validator)

        try:
            validator_cls.check_schema(schema)
        except SchemaError as err:  # pragma: no cover
            self.log.exception("Error in %s schema", form_name)
            self.validation_errors += [err]

    def resolve_url(self, url: str) -> dict[str, Any]:
        """Maybe resolve a URL."""
        if url.startswith("py:"):
            return import_dotted_dict(url[3:])
        if url.startswith("."):
            rel_path = self.resource_path or (self.path.parent if self.path else None)
            if rel_path is None:  # pragma: no cover
                msg = f"no rel path for {self}"
                raise NotImplementedError(msg)
            source = DataSource(rel_path / url)
            if source.raw is not None:
                return source.raw
        msg = f"unexpected url {url}"  # pragma: no cover
        raise NotImplementedError(msg)  # pragma: no cover
