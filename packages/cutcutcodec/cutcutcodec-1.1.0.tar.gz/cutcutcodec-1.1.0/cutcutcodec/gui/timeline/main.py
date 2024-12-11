#!/usr/bin/env python3

"""Allow video and audio cronological previews and editing."""

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.timeline.slider import Slider
from cutcutcodec.gui.timeline.view import View


class Timeline(CutcutcodecWidget, QtWidgets.QWidget):
    """Time slider and tracks."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.slider = Slider(self)
        self.view = View(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.slider.refresh()
        self.view.refresh()
