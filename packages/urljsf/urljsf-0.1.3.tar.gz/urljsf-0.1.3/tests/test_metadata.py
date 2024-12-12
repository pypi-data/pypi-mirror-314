"""Tests of packaging metadata."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.


def test_version() -> None:
    """Verify version the version is present."""
    from urljsf import __version__

    assert __version__
