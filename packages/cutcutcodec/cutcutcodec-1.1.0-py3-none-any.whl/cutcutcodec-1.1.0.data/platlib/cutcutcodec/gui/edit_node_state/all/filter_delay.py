#!/usr/bin/env python3

"""Properties of a ``FilterDelay``."""

import math

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Numerable


class EditFilterDelay(EditBase):
    """Allow to view and modify the properties of a filter of type ``FilterDelay``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        Numerable(self, "delay", (-math.inf, math.inf), isfinite=True)(grid_layout)
        self.setLayout(grid_layout)
