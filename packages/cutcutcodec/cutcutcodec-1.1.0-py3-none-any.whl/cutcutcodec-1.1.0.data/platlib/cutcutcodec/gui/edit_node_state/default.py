#!/usr/bin/env python3

"""Default editing window in case the main one is not defined.

When the specific edit window for a node is not defined,
it is still possible to display its internal read-only state.
"""

import pprint

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase


class ViewNodeState(EditBase):
    """If you can't change the node's properties, you can still display them."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)

        grid_layout = QtWidgets.QGridLayout()
        state = self.state  # avoid to many func call
        for i, key in enumerate(sorted(self.state)):
            grid_layout.addWidget(QtWidgets.QLabel(f"{key}:", self), i, 0)
            grid_layout.addWidget(QtWidgets.QLabel(pprint.pformat(state[key]), self), i, 1)
        self.setLayout(grid_layout)
