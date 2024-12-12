"""Custom docutils nodes."""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from typing import Any

from docutils import nodes


class urljsf(nodes.raw):
    """A vanity node we can ``traverse`` for during ``html-page-context``."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a new form node."""
        kwargs.update({"format": "html", "class": "urljsf-node"})
        super().__init__(*args, **kwargs)
