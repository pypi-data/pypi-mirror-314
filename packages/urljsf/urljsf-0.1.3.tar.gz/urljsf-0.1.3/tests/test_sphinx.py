"""Verify behavior when run under ``sphinx-build``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from pathlib import Path

from pytest_console_scripts import ScriptRunner

from .conftest import UTF8


def test_sphinx_build(
    a_sphinx_project: str, script_runner: ScriptRunner, tmp_path: Path
) -> None:
    """Verify a site builds."""
    from urljsf.constants import MIME_PREFIX

    build = tmp_path / "build"

    args = ["sphinx-build", "-b", "html", "src", "build", "-vvv", "-W"]
    res = script_runner.run(args, cwd=str(tmp_path))

    assert res.success
    assert build.exists()
    built = sorted(build.rglob("*"))
    print("\n".join(list(map(str, built))))
    static = build / "_static"
    assert (static / "urljsf/index.js").exists()
    index_ = build / "index.html"
    index_text = index_.read_text(**UTF8)
    assert "urljsf/index.js" in index_text
    assert MIME_PREFIX in index_text
