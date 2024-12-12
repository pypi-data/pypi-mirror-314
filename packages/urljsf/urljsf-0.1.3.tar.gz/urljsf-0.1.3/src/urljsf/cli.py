"""Standalone CLI for building URL forms."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .config import DEFAULTS, Config
from .constants import __dist__, __version__
from .urljsf import Urljsf


def get_parser() -> ArgumentParser:
    """Get a parser for the command line arguments."""
    parser = ArgumentParser(__dist__, add_help=False, description=__doc__)
    parser.add_argument(
        "input_",
        metavar="INPUT",
        help="a urljsf definition file as JSON, TOML, or YAML",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="path to a folder to generate",
        default=DEFAULTS["output_dir"],
    )
    parser.add_argument(
        "-h",
        "--html-filename",
        help="name of an HTML file to generate",
        default=DEFAULTS["html_filename"],
    )
    parser.add_argument(
        "--html-title",
        help="HTML page title",
    )
    parser.add_argument(
        "--template",
        help="name of the template to use",
        default=DEFAULTS["template"],
    )
    parser.add_argument("--help", action="help", help="show program's usage and exit")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line interface."""
    parser = get_parser()
    parsed_args = parser.parse_args(argv)
    config = Config(**vars(parsed_args))
    urljsf = Urljsf(config)
    urljsf.log.error("argv: %s", parsed_args)
    return urljsf.run_cli()
