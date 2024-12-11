#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.generation.video.noise.GeneratorVideoNoise``."""

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Seedable


class EditGeneratorVideoNoise(EditBase):
    """Allow to view and modify the properties of a generator of type ``GeneratorVideoNoise``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        Seedable(self)(grid_layout)
        self.setLayout(grid_layout)
