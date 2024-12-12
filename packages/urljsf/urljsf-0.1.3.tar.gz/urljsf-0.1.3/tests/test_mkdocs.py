"""Verify behavior when run under ``mkdocs build``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from pathlib import Path

import pytest
from pytest_console_scripts import ScriptRunner

from .conftest import UTF8

try:
    __import__("mkdocs")
except ImportError:
    pytest.skip("mkdocs is not installed", allow_module_level=True)


def test_sphinx_build(
    an_mkdocs_project: str, script_runner: ScriptRunner, tmp_path: Path
) -> None:
    """Verify a site builds."""
    from urljsf.constants import MIME_PREFIX

    site = tmp_path / "project/site"

    args = ["mkdocs", "build", "--verbose"]
    res = script_runner.run(args, cwd=str(tmp_path / "project"))

    assert res.success
    assert site.exists()
    built = sorted(site.rglob("*"))
    print("\n".join(list(map(str, built))))
    static = site / "_static"
    assert (static / "urljsf/index.js").exists()
    index_ = site / "index.html"
    if an_mkdocs_project == "nested-file":
        index_ = site / "deeply/nested/index.html"
    index_text = index_.read_text(**UTF8)
    print(index_text)
    assert "urljsf/index.js" in index_text
    assert MIME_PREFIX in index_text
