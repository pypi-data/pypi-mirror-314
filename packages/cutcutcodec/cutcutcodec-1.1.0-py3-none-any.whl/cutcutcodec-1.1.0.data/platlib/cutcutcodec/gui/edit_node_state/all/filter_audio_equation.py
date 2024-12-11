#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.filter.audio.equation.FilterAudioEquation``."""

from qtpy import QtWidgets

from cutcutcodec.core.classes.layout import AllLayouts, Layout
from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import AudioLayoutable, Equationable


class EditFilterAudioEquation(EditBase):
    """Allow to view and modify the properties of a node of type ``FilterAudioEquation``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.signals = []
        self.re_symb = r"t|" + r"|".join(fr'{p}_\d+' for p in sorted(AllLayouts().individuals))

        self.grid_layout = QtWidgets.QGridLayout()
        self.signals_ref_span = AudioLayoutable(self, enable_default=True)(self.grid_layout)
        self.init_signal(self.grid_layout, self.signals_ref_span)
        self.setLayout(self.grid_layout)

    def init_signal(self, grid_layout, ref_span=0):
        """Display and allows to modify the signals."""
        state = self.state  # static
        profile = Layout(state["layout"] or len(state["signals"]))
        state["signals"] += ["0"] * (len(profile.channels)-len(state["signals"]))
        state["signals"] = state["signals"][:len(profile.channels)]
        for i, (channel, desc) in enumerate(profile.channels):
            self.signals.append(
                Equationable(self, (i, "signals"), f"{desc} ({channel}):", self.re_symb)
            )
        for equation in self.signals:
            equation(grid_layout, ref_span)
            ref_span += 1
        return ref_span + 1

    def reset(self):
        """Help when called by the signals interface."""
        for signal in self.signals:
            signal.delete()
        self.signals = []
        self.init_signal(self.grid_layout, ref_span=self.signals_ref_span)
