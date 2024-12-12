"""Test configuration for ``urljsf``."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import io
import json
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

import tomli_w
from ruamel.yaml import YAML as YAML_

YAML = YAML_(typ="safe")


if TYPE_CHECKING:
    from collections.abc import Generator


pytest_plugins = ("sphinx.testing.fixtures",)

WIN = os.name == "win32"
SEP = ";" if WIN else ":"
UTF8 = {"encoding": "utf-8"}
HERE = Path(__file__).parent
ROOT = HERE.parent
JS_EXAMPLES = ROOT / "js/demo"
FIXTURES = HERE / "fixtures"

SPHINX_PROJECTS = FIXTURES / "sphinx"
ALL_SPHINX_PROJECTS = {p.name: p for p in SPHINX_PROJECTS.glob("*") if p.is_dir()}

MKDOCS_PROJECTS = FIXTURES / "mkdocs"
ALL_MKDOCS_PROJECTS = {p.name: p for p in MKDOCS_PROJECTS.glob("*") if p.is_dir()}

CLI_PROJECTS = FIXTURES / "cli"
VALID_CLI_PROJECTS = CLI_PROJECTS / "valid"
ALL_VALID_CLI_PROJECTS = {p.name: p for p in VALID_CLI_PROJECTS.glob("*") if p.is_dir()}

ALL_DEMO_URLJSF_EXAMPLES = {p.name: p for p in JS_EXAMPLES.rglob("urljsf.*")}
ALL_DEMO_UI_EXAMPLES = {p.name: p for p in JS_EXAMPLES.rglob("*.uischema.*")}

#: names of fixture projects that won't deploy `schema.json`
NO_SCHEMA_JSON = ["remote"]

FORMATS = ["json", "toml", "yaml"]


@pytest.fixture
def py_tmp_path(tmp_path: Path) -> Generator[Path, None, None]:
    """Wrap a temporary directory added to ``PYTHONPATH``."""
    var_name = "PYTHONPATH"
    old_py_path = os.environ.get(var_name)

    new_py_path = str(tmp_path.resolve())
    if old_py_path:
        new_py_path = SEP.join([new_py_path, old_py_path])
    os.environ[var_name] = new_py_path
    yield tmp_path
    if old_py_path:
        os.environ[var_name] = old_py_path
    else:
        os.environ.pop(var_name)


@pytest.fixture(params=sorted(ALL_SPHINX_PROJECTS.keys()))
def a_sphinx_project(request: pytest.FixtureRequest, tmp_path: Path) -> str:
    """Provide a sphinx project."""
    dest = tmp_path / "src"
    shutil.copytree(SPHINX_PROJECTS / request.param, dest)
    return f"{request.param}"


@pytest.fixture(params=sorted(ALL_MKDOCS_PROJECTS.keys()))
def an_mkdocs_project(request: pytest.FixtureRequest, tmp_path: Path) -> str:
    """Provide an mkdocs project."""
    dest = tmp_path / "project"
    shutil.copytree(MKDOCS_PROJECTS / request.param, dest)
    return f"{request.param}"


@pytest.fixture(params=sorted(ALL_VALID_CLI_PROJECTS.keys()))
def a_valid_cli_project(request: pytest.FixtureRequest, tmp_path: Path) -> str:
    """Provide a CLI project."""
    dest = tmp_path / "src"
    shutil.copytree(VALID_CLI_PROJECTS / request.param, dest)
    return f"{request.param}"


@pytest.fixture(params=FORMATS)
def a_format(request: pytest.FixtureRequest) -> str:
    """Provide a format."""
    return f"{request.param}"


@pytest.fixture(params=sorted(ALL_VALID_CLI_PROJECTS.keys()))
def a_valid_formatted_cli_project(
    request: pytest.FixtureRequest,
    tmp_path: Path,
    a_format: str,
) -> str:
    """Provide a project fixture in different formats."""
    a_valid_cli_project = request.param
    dest = tmp_path / "src"
    original = VALID_CLI_PROJECTS / request.param
    original_defn = original / f"urljsf.{a_format}"
    if original_defn.exists():
        pytest.skip(f"{a_valid_cli_project} is already {a_format}")

    shutil.copytree(original, dest)
    old_defn, data = _load_any("urljsf", dest)
    old_defn.unlink()

    suffix = f".{a_format}"
    defn_as_fmt = _dumps(data, suffix)
    new_defn = dest / f"urljsf{suffix}"
    new_defn.write_text(defn_as_fmt, **UTF8)
    return f"{a_valid_cli_project}-as-{a_format}"


@pytest.fixture(params=sorted(ALL_VALID_CLI_PROJECTS.keys()))
def a_valid_extracted_cli_project(
    request: pytest.FixtureRequest,
    a_format: str,
    tmp_path: Path,
) -> str:
    """Provide a project fixture with data extracted to files."""
    a_valid_cli_project = request.param
    dest = tmp_path / "src"
    original = VALID_CLI_PROJECTS / request.param

    shutil.copytree(original, dest)
    old_defn, data = _load_any("urljsf", dest)
    old_defn.unlink()

    suffix = f".{a_format}"

    for form_name, form in data["forms"].items():
        for field in ["schema", "ui_schema", "props", "form_data"]:
            value = form.get(field)
            if not isinstance(value, dict):
                continue
            field_path = dest / f"{form_name}-{field}{suffix}"
            field_path.write_text(_dumps(value, suffix), **UTF8)
            form[field] = f"./{field_path.name}"

    defn_as_fmt = _dumps(data, suffix)
    new_defn = dest / f"urljsf{suffix}"
    new_defn.write_text(defn_as_fmt, **UTF8)
    return f"{a_valid_cli_project}-as-{a_format}-extracted"


@pytest.fixture(params=sorted(ALL_VALID_CLI_PROJECTS.keys()))
def a_valid_py_cli_project(
    request: pytest.FixtureRequest,
    a_format: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> str:
    """Provide a project fixture."""
    a_valid_cli_project = request.param
    dest = tmp_path / "src"
    original = VALID_CLI_PROJECTS / request.param

    shutil.copytree(original, dest)
    old_defn, data = _load_any("urljsf", dest)
    old_defn.unlink()

    suffix = f".{a_format}"

    for form_name, form in data["forms"].items():
        for field in ["schema", "ui_schema", "props", "form_data"]:
            value = form.get(field)
            if not isinstance(value, dict):
                continue
            member = field.upper()
            field_path = dest / f"{form_name}_{field}.py"
            field_path.write_text(f"{member} = {value}", **UTF8)
            form[field] = f"py:{field_path.stem}:{member}"

    defn_as_fmt = _dumps(data, suffix)
    new_defn = dest / f"urljsf{suffix}"
    new_defn.write_text(defn_as_fmt, **UTF8)

    monkeypatch.setenv("PYTHONPATH", str(dest))
    return f"{a_valid_cli_project}-as-py"


@pytest.fixture(params=sorted(ALL_DEMO_URLJSF_EXAMPLES.keys()))
def an_example_urljsf(request: pytest.FixtureRequest) -> dict[str, Any]:
    """Provide an example."""
    src = ALL_DEMO_URLJSF_EXAMPLES[request.param]
    return _parse(src)


@pytest.fixture(params=sorted(ALL_DEMO_UI_EXAMPLES.keys()))
def an_example_ui_schema(request: pytest.FixtureRequest) -> dict[str, Any]:
    """Provide an example."""
    src = ALL_DEMO_UI_EXAMPLES[request.param]
    return _parse(src)


def _load_any(stem: str, path: Path) -> tuple[Path, dict[str, Any]]:
    """Load a fixtured file as data."""
    src: Path | None = None
    data: dict[str, Any] = {}
    for fmt in FORMATS:
        src = path / f"{stem}.{fmt}"
        if not src.exists():
            continue
        data = _parse(src)
        break

    assert src is not None, "no source found"
    return src, data


def _parse(path: Path) -> dict[str, Any]:
    """Parse something."""
    text = path.read_text(**UTF8)
    suffix = path.suffix
    if suffix == ".toml":
        return tomllib.loads(text)
    if suffix in {".yaml", ".yml"}:
        return YAML.load(text)  # type: ignore[no-any-return]
    if suffix == ".json":
        return json.loads(text)  # type: ignore[no-any-return]
    msg = f"Can't parse {path}"
    raise NotImplementedError(msg)


def _dumps(data: dict[str, Any], suffix: str) -> str:
    """Dump something."""
    if suffix == ".toml":
        return tomli_w.dumps(data)
    if suffix in {".yaml", ".yml"}:
        with io.StringIO() as fp:
            YAML.dump(data, fp)
            return fp.getvalue()
    elif suffix == ".json":
        return json.dumps(data, indent=2)
    else:
        msg = f"Can't dump {data}"
        raise NotImplementedError(msg)
