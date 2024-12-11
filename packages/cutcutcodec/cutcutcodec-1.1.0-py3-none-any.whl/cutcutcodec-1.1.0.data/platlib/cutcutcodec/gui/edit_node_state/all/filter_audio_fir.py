#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.generation.audio.noise.GeneratorAudioNoise``."""

import re

from qtpy import QtWidgets
import torch

from cutcutcodec.core.filter.audio.fir import FilterAudioFIR
from cutcutcodec.gui.edit_node_state.base import EditBase


class EditFilterAudioFIR(EditBase):
    """Allow to view and modify the properties of a filter of type ``FilterAudioFIR``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)

        self.rep_textedit = self.rate_textbox = None

        self.grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_fir(self.grid_layout)
        self.init_rate(self.grid_layout, ref_span)
        self.setLayout(self.grid_layout)

    def init_fir(self, grid_layout, ref_span=0):
        """Display and allows to modify the impulsional resp."""
        grid_layout.addWidget(QtWidgets.QLabel("Impulsional Response:"), ref_span, 0)
        self.rep_textedit = QtWidgets.QTextEdit()  # QtWidgets.QLineEdit()
        self.rep_textedit.setText(
            ", ".join(map(str, FilterAudioFIR.decode_fir(self.state["fir_encoded"]).tolist()))
        )
        self.rep_textedit.textEdited.connect(self.validate_fir)
        grid_layout.addWidget(self.rep_textedit, ref_span, 1)
        return ref_span + 1

    def init_rate(self, grid_layout, ref_span=0):
        """Display and allows to modify the samplerate."""
        grid_layout.addWidget(QtWidgets.QLabel("Sample Rate (Hz):"), ref_span, 0)
        self.rate_textbox = QtWidgets.QLineEdit()
        self.rate_textbox.setText(str(self.state["fir_rate"]))
        self.rate_textbox.editingFinished.connect(self.validate_rate)
        grid_layout.addWidget(self.rate_textbox, ref_span, 1)
        return ref_span + 1

    def validate_fir(self):
        """Check than the numbers are correct and update the list."""
        text = self.rep_textedit.toPlainText()
        if not (items := list(map(float, re.findall(r"\d+(?:\.\d*)", text)))):
            self.rep_textedit.setStyleSheet("background:red;")
            return
        fir = FilterAudioFIR.encode_fir(torch.tensor(items, dtype=torch.float64))
        self.try_set_state(self.get_updated_state_dict({"fir_encoded": fir}), self.rep_textedit)

    def validate_rate(self, text):
        """Check than the framerate is correct and update it."""
        raise NotImplementedError
