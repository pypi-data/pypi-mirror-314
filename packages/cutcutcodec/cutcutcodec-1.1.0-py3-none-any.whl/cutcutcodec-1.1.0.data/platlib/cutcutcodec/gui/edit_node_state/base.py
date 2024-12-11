#!/usr/bin/env python3

"""Allow to unify all node editing windows.

Defines several accessors that allow to lighten the code of child classes.
"""

import copy
import typing

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class EditBase(CutcutcodecWidget, QtWidgets.QWidget):
    """Common base class for all node editing classes."""

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        assert node_name in self.app.graph.nodes, (node_name, set(self.app.graph.nodes))
        self.node_name = node_name
        self.ref = []  # for keeping the reference of the interfaces

    def get_class(self) -> type:
        """Return the node class."""
        return self.app.graph.nodes[self.node_name]["class"]

    def get_updated_state(
        self, getter: typing.Callable, setter: typing.Callable, value
    ) -> dict[str]:
        """Return an independant copy of the current state, with the new attribute."""
        old_value = getter()
        setter(value)
        new_state = copy.deepcopy(self.state)
        setter(old_value)
        return new_state

    def get_updated_state_dict(self, changes: dict[str]) -> dict[str]:
        """Return a copy of the old state with the new attribute."""
        return {k: changes.get(k, o) for k, o in self.state.items()}

    @property
    def state(self) -> dict[str]:
        """Return a pointer of the node state.

        Returns the updated reference of the graph state with the tree node state.
        Dosen't change the graph dict id, change it inplace.
        """
        updated_state = self.app.tree_node(self.node_name).getstate()
        self.app.graph.nodes[self.node_name]["state"].clear()
        self.app.graph.nodes[self.node_name]["state"].update(updated_state)
        return self.app.graph.nodes[self.node_name]["state"]

    def try_set_state(self, new_state: dict[str], textbox=None) -> bool:
        """If possible, try to apply the change to the node.

        In case of AssertionError, the changes are not applied
        and a popup window appears to display the error message.
        Dosen't change the graph dict id, change it inplace.

        Parameters
        ----------
        new_state : dict
            The new different state.
        textbox : PyQt6.QWidget, optional
            Must accepts the method setStyleSheet for changing the bakground color.

        Returns
        -------
        failed : boolean
            False if succes and True if AssertionError raise in check.
        """
        state = self.state
        old_state = state.copy()
        assert new_state.keys() == old_state.keys(), (new_state, old_state)

        # search and format differences
        changes = {k: (o, new_state[k]) for k, o in old_state.items() if o != new_state[k]}
        changes_str = "\n".join(f"change {k} from {o} to {n}" for k, (o, n) in changes.items())

        # apply changes
        state.clear()
        state.update(new_state)
        try:
            self.app.tree_node(self.node_name)
            self.main_window.refresh()  # maybe can cause indirect errors
        except AssertionError as err:
            state.clear()
            state.update(old_state)
            if textbox is not None:
                textbox.setStyleSheet("background:red;")
            QtWidgets.QMessageBox.warning(
                None,
                f"Invalid state of {self.node_name}",
                f"{changes_str}\n\n{err}"
            )
            return True
        if textbox is not None:
            textbox.setStyleSheet("background:none;")
        return False
