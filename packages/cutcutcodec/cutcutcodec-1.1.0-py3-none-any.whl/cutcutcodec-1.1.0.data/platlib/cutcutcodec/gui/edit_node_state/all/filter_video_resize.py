#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.filter.video.resize.FilterVideoResize``."""

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Booleanable, Shapeable


class EditFilterVideoResize(EditBase):
    """Allow to view and modify the properties of a generator of type ``GeneratorAudioNoise``."""

    def __init__(self, parent, node_name):
        EditBase.__init__(self, parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        ref_span = Shapeable(self)(grid_layout)
        Booleanable(self, var="keep_ratio", label="Keep Ratio:")(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)
