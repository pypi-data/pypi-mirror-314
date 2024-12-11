#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.filter.video.equation.FilterVideoEquation``."""

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Equationable


class EditFilterVideoEquation(EditBase):
    """Allow to view and modify the properties of a node of type ``FilterVideoEquation``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.colors = []
        self.re_symb = r"i|j|t|[bgra]\d+"

        self.grid_layout = QtWidgets.QGridLayout()
        self.init_colors(self.grid_layout)
        self.setLayout(self.grid_layout)

    def init_colors(self, grid_layout, ref_span=0):
        """Display and allows to modify the equations."""
        if len(self.state["colors"]) == 1:
            self.colors.append(Equationable(self, (0, "colors"), "Gray:", self.re_symb))
            self.colors.append(Equationable(self, (1, "colors"), "Alpha:", self.re_symb))
        elif len(self.state["colors"]) == 2:
            self.colors.append(Equationable(self, (0, "colors"), "Gray (or Blue):", self.re_symb))
            self.colors.append(Equationable(self, (1, "colors"), "Alpha (or Green):", self.re_symb))
            self.colors.append(Equationable(self, (2, "colors"), "Red:", self.re_symb))
        elif len(self.state["colors"]) == 3:
            self.colors.append(Equationable(self, (0, "colors"), "Blue (or Gray):", self.re_symb))
            self.colors.append(Equationable(self, (1, "colors"), "Green (or Alpha):", self.re_symb))
            self.colors.append(Equationable(self, (2, "colors"), "Red:", self.re_symb))
            self.colors.append(Equationable(self, (3, "colors"), "Alpha:", self.re_symb))
        else:
            self.colors.append(Equationable(self, (0, "colors"), "Blue:", self.re_symb))
            self.colors.append(Equationable(self, (1, "colors"), "Green:", self.re_symb))
            self.colors.append(Equationable(self, (2, "colors"), "Red:", self.re_symb))
            self.colors.append(Equationable(self, (3, "colors"), "Alpha:", self.re_symb))

        for equation in self.colors:
            equation(grid_layout, ref_span)
            ref_span += 1
        return ref_span + 1

    def reset(self):
        """Help when called by the colors interface."""
        for color in self.colors:
            color.delete()
        self.colors = []
        self.init_colors(self.grid_layout)
