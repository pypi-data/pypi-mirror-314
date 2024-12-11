#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.generation.audio.noise.GeneratorAudioNoise``."""

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import AudioLayoutable, Seedable


class EditGeneratorAudioNoise(EditBase):
    """Allow to view and modify the properties of a generator of type ``GeneratorAudioNoise``."""

    def __init__(self, parent, node_name):
        EditBase.__init__(self, parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        ref_span = AudioLayoutable(self, enable_default=False)(grid_layout)
        Seedable(self)(grid_layout, ref_span)
        self.setLayout(grid_layout)
