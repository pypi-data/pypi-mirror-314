#!/usr/bin/env python3

"""Processing of ffmpeg documentation."""

import logging
import re
import typing

from qtpy import QtGui, QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class DocViewer(CutcutcodecWidget, QtWidgets.QWidget):
    """Allow to show and hide a documentation."""

    def __init__(self, parent, dict_settings: dict[str, str], doc_getter: typing.Callable):
        super().__init__(parent)
        self._parent = parent
        self.dict_settings = dict_settings
        self.doc_getter = doc_getter

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self._doc_label = QtWidgets.QLabel(scroll_area)
        font = QtGui.QFont("", -1)
        font.setFixedPitch(True)
        if not QtGui.QFontInfo(font).fixedPitch():
            logging.warning("no fixed pitch font found")
        self._doc_label.setFont(font)
        scroll_area.setWidget(self._doc_label)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Documentation:", self), 0, 0)
        layout.addWidget(scroll_area, 0, 1)

        layout.addWidget(QtWidgets.QLabel("Custom Settings:"), 1, 0)
        self._params_textbox = QtWidgets.QLineEdit(self)
        self._params_textbox.editingFinished.connect(self.validate)
        layout.addWidget(self._params_textbox, 1, 1)

        self.setLayout(layout)

    def refresh(self):
        """Update the doc content and displaying."""
        doc_content = self.doc_getter(self)
        self._doc_label.setText(doc_content)
        self._params_textbox.setText(" ".join(f"-{k} {v}" for k, v in self.dict_settings.items()))
        if doc_content:
            self.show()
        else:
            self.hide()

    def validate(self, text):
        """Update and checks the specific settings."""
        if re.fullmatch(r"\s*", text):  # empty string
            self.dict_settings.clear()
            self._params_textbox.setStyleSheet("background:none;")
            return
        if not re.fullmatch(r"(?:-[a-zA-Z][a-zA-Z0-9_:-]*\s+.*?\w\s+)+", text+" "):  # no conform
            self._params_textbox.setStyleSheet("background:red;")
            return

        self.dict_settings.clear()
        for match in re.finditer(r"-(?P<label>[a-zA-Z][a-zA-Z0-9_:-]*)\s+(?P<set>.*?\w+)", text):
            self.dict_settings[match["label"]] = match["set"]
        print(f"update settings: {self.dict_settings}")
        self._params_textbox.setStyleSheet("background:none;")
