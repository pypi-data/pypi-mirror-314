#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.generation.audio.equation.GeneratorAudioEquation``."""


from cutcutcodec.gui.edit_node_state.all.filter_audio_equation import EditFilterAudioEquation


class EditGeneratorAudioEquation(EditFilterAudioEquation):
    """Allow to view and modify the properties of a node of type ``GeneratorAudioEquation``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.re_symb = r"t"
