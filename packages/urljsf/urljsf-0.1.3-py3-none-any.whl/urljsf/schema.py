"""JSON Schema for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft7Validator, validators

from .constants import SCHEMA_VERSION, UTF8

HERE = Path(__file__).parent
STATIC = HERE / "_static"
SCHEMA = STATIC / "urljsf/schema"
CURRENT_SCHEMA = SCHEMA / SCHEMA_VERSION

FORM_SCHEMA = CURRENT_SCHEMA / "form.schema.json"
PROPS_SCHEMA = CURRENT_SCHEMA / "props.schema.json"
UI_SCHEMA = CURRENT_SCHEMA / "ui.schema.json"

_StrictDraft7Validator = validators.create(
    dict(Draft7Validator.META_SCHEMA, additionalProperties=False),
    Draft7Validator.VALIDATORS,
    "StrictDraft7",
)


def _make_strict_validator(path: Path) -> Draft7Validator:
    """Validate the schema."""
    raw = json.loads(path.read_text(**UTF8))
    _StrictDraft7Validator.check_schema(raw)
    return Draft7Validator(raw, format_checker=Draft7Validator.FORMAT_CHECKER)


URLJSF_VALIDATOR = _make_strict_validator(FORM_SCHEMA)
PROPS_VALIDATOR = _make_strict_validator(PROPS_SCHEMA)
UI_VALIDATOR = _make_strict_validator(UI_SCHEMA)
