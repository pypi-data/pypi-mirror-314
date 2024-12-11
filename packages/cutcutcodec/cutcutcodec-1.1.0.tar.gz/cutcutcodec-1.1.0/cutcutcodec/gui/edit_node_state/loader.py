#!/usr/bin/env python3

"""Allow to import dynamically the windows associated to the edition of a node."""

import importlib
import inspect
import re

from cutcutcodec.core.classes.node import Node
from cutcutcodec.gui.edit_node_state.default import ViewNodeState


def load_edit_windows(node_subclass: type) -> type:
    """Find and import the edit window for a specific node.

    Parameters
    ----------
    node_subclass : type
        A subclass that inherits from ``cutcutcodec.core.classes.node.Node``.

    Returns
    -------
    edit_class : type
        Subclass of ``cutcutcodec.gui.edit_node_state.base.EditBase``.
        The uninstantiated class of a window allowing to see
        and if possible to edit the properties of the node.
        If this class is not defined,
        ``cutcutcodec.gui.edit_node_state.default.ViewNodeState`` is returned.
    """
    assert issubclass(node_subclass, Node), node_subclass.__name__

    class_name = node_subclass.__name__
    class_name_snake = re.sub(r"(?!^)([A-Z]+)", r"_\1", class_name).lower()
    try:
        mod = importlib.import_module(f"cutcutcodec.gui.edit_node_state.all.{class_name_snake}")
    except ModuleNotFoundError:
        return ViewNodeState
    members = dict(inspect.getmembers(mod))
    edit_class_name = f"Edit{class_name}"
    assert edit_class_name in members, f"{edit_class_name} not found in {mod.__name__}"
    return members[edit_class_name]
