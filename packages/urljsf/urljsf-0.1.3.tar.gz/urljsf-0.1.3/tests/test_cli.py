"""Verify the standalone cli."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_console_scripts import ScriptRunner


def test_cli_help(script_runner: ScriptRunner) -> None:
    """Verify help is printed."""
    r = script_runner.run(["urljsf", "--help"], check=True)
    assert "help" in r.stdout


def test_cli_version(script_runner: ScriptRunner) -> None:
    """Verify version is printed."""
    import urljsf

    r = script_runner.run(["urljsf", "--version"], check=True)
    assert urljsf.__version__ in r.stdout


def test_cli_run(
    script_runner: ScriptRunner, a_valid_cli_project: str, tmp_path: Path
) -> None:
    """Verify a site is built from a project."""
    _assert_builds(tmp_path / "src", script_runner)


def test_cli_run_format(
    script_runner: ScriptRunner, a_valid_formatted_cli_project: str, tmp_path: Path
) -> None:
    """Verify a site is built from a derived project."""
    _assert_builds(tmp_path / "src", script_runner)


def test_cli_run_extracted(
    script_runner: ScriptRunner, a_valid_extracted_cli_project: str, tmp_path: Path
) -> None:
    """Verify a site is built from extracted files."""
    _assert_builds(tmp_path / "src", script_runner)


def test_cli_run_py(
    script_runner: ScriptRunner, a_valid_py_cli_project: str, tmp_path: Path
) -> None:
    """Verify a site is built from python files."""
    src = tmp_path / "src"
    _assert_builds(src, script_runner)


def _assert_builds(src: Path, script_runner: ScriptRunner) -> None:
    all_files = [*src.glob("urljsf.*")]
    assert all_files
    defn = next(p for p in all_files if p.stem == "urljsf")
    r = script_runner.run(
        ["urljsf", f"src/{defn.name}"],
        cwd=str(src.parent),
    )
    assert r.success
    _assert_outputs(src.parent)


def _assert_outputs(
    path: Path, *, out: Path | None = None, extra_files: list[Path] | None = None
) -> None:
    """Assert a number of files exist."""
    expected = [
        "index.html",
        "_static/urljsf/third-party-licenses.json",
        *(extra_files or []),
    ]
    out = out or (path / "_urljsf_output")
    missing = {}

    for rel in expected:
        found = sorted(out.glob(rel))
        if not found:
            missing[out / rel] = True

    if missing:
        print("\n".join(map(str, path.rglob("*"))))

    assert not missing
