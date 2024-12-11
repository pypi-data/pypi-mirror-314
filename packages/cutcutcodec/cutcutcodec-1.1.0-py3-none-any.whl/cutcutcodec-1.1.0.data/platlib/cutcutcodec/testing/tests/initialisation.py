#!/usr/bin/env python3

"""Ensures all source files are importable."""

import importlib

from cutcutcodec.testing.generation import extract_cls_and_default
from cutcutcodec.utils import get_project_root


def test_default():
    """Initialize the example of each class."""
    for node_cls, node in extract_cls_and_default():
        assert isinstance(node, node_cls)


def test_import():
    """Recursively browse all files to import them."""
    for filepath in get_project_root().rglob("*.py"):
        importlib.import_module(
            ".".join(
                ("cutcutcodec" / filepath.relative_to(get_project_root()).with_suffix("")).parts
            )
        )
