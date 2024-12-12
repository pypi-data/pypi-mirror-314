"""Tests of examples."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from typing import Any


def test_example_urljsf(an_example_urljsf: dict[str, Any]) -> None:
    """Verify a full urljsf examples is valid."""
    from urljsf.schema import URLJSF_VALIDATOR

    errors = [*URLJSF_VALIDATOR.iter_errors(an_example_urljsf)]
    assert not errors


def test_example_ui_schema(an_example_ui_schema: dict[str, Any]) -> None:
    """Verify a ui schema examples is valid."""
    from urljsf.schema import UI_VALIDATOR

    errors = [*UI_VALIDATOR.iter_errors(an_example_ui_schema)]
    assert not errors
