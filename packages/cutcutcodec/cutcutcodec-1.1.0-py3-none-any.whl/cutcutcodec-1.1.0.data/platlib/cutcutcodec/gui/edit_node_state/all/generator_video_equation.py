#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.generation.video.equation.GeneratorVideoEquation``."""

from cutcutcodec.gui.edit_node_state.all.filter_video_equation import EditFilterVideoEquation


class EditGeneratorVideoEquation(EditFilterVideoEquation):
    """Allow to view and modify the properties of a node of type ``GeneratorVideoEquation``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.re_symb = r"i|j|t"
