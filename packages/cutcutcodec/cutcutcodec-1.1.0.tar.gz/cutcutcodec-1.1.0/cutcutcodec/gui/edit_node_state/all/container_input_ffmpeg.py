#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.io.read_ffmpeg.ContainerInputFFMPEG``."""

import json

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase


class EditContainerInputFFMPEG(EditBase):
    """Allow to view and modify the properties of a node of type ``ContainerInputFFMPEG``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self._filename_av_kwargs = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_path(grid_layout)
        self.init_av_kwargs(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)

    def _validate_av_kwargs(self, text):
        """Check that the av kwargs are correct and update the color."""
        try:
            av_kwargs = json.loads(text)
        except json.JSONDecodeError:
            self._av_kwargs_textbox.setStyleSheet("background:red;")
            return
        if not all(isinstance(k, str) for k in av_kwargs):
            self._av_kwargs_textbox.setStyleSheet("background:red;")
            return

        def setter(av_kwargs):
            self.state["av_kwargs"] = av_kwargs
        self.try_set_state(
            self.get_updated_state(
                (lambda: self.state["av_kwargs"]),
                setter,
                av_kwargs,
            ),
            self._av_kwargs_textbox,
        )

    def init_av_kwargs(self, grid_layout, ref_span=0):
        """Display and allows to modify the av kwargs."""
        grid_layout.addWidget(QtWidgets.QLabel("PyAv parameters (json):"))
        self._av_kwargs_textbox = QtWidgets.QLineEdit()
        self._av_kwargs_textbox.setText(
            json.dumps(self.state["av_kwargs"], check_circular=False, indent=4, sort_keys=True)
        )
        self._av_kwargs_textbox.editingFinished.connect(self._validate_av_kwargs)
        grid_layout.addWidget(self._av_kwargs_textbox, ref_span, 1)
        ref_span += 1
        return ref_span

    def init_path(self, grid_layout, ref_span=0):
        """Display and allows to modify the filename."""
        grid_layout.addWidget(QtWidgets.QLabel("File Path:"), ref_span, 0)
        grid_layout.addWidget(QtWidgets.QLabel(self.state["filename"]), ref_span, 1)
        return ref_span + 1
