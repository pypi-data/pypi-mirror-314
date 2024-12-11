#!/usr/bin/env python3

"""Allow to generate a multitude of objects.

Doesn't perform any test itself but allows to lighten the other tests.
"""

import importlib
import inspect

from cutcutcodec.core.classes.node import Node
from cutcutcodec.utils import get_project_root


def extract_cls_and_default():
    """Initialize and yield the example of each class."""
    done = set()
    for filepath in (get_project_root() / "core").rglob("*.py"):
        mod = importlib.import_module(
            ".".join(
                ("cutcutcodec" / filepath.relative_to(get_project_root()).with_suffix("")).parts
            )
        )
        for name, node_cls in inspect.getmembers(mod):  # getmembers_static
            if (
                inspect.isclass(node_cls) and issubclass(node_cls, Node)
                and node_cls not in done
                and name not in {
                    "Filter", "MetaFilter", "Node", "ContainerInput", "ContainerOutput"
                }
            ):
                yield node_cls, node_cls.default()
                done.add(node_cls)


def extract_cls_and_streams():
    """Yield all streams of all default examples."""
    for node_cls, node in extract_cls_and_default():
        for stream in node.out_streams:
            yield node_cls, stream


def extract_default():
    """Like ``extract_cls_and_default`` without the class."""
    for _, node in extract_cls_and_default():
        yield node


def extract_streams():
    """Like ``extract_cls_and_streams`` without the class."""
    for _, stream in extract_cls_and_streams():
        yield stream
