#!/usr/bin/env python3

"""Accesses and displays the source code documentation for a node."""

import inspect
import logging

from pdoc.html_helpers import to_html
from qtpy import QtGui, QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase


class Documentation(EditBase):
    """Display the node documentation."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)

        layout = QtWidgets.QVBoxLayout()
        self.init_documentation(layout)
        self.setLayout(layout)

    def init_documentation(self, layout):
        """Extract the documentation and formats it for display."""
        font = QtGui.QFont("", -1)
        font.setFixedPitch(True)
        if not QtGui.QFontInfo(font).fixedPitch():
            logging.warning("no fixed pitch font found")

        main_doc = inspect.getdoc(self.get_class().__init__)
        main_doc = to_html(main_doc, latex_math=True)
        label_main = QtWidgets.QLabel(main_doc)
        label_main.setWordWrap(True)
        label_main.setFont(font)
        layout.addWidget(label_main)

        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)

        ex_doc = inspect.getdoc(self.get_class())
        ex_doc = to_html(ex_doc, latex_math=True)
        label_ex = QtWidgets.QLabel(ex_doc)
        label_ex.setWordWrap(True)
        label_ex.setFont(font)
        layout.addWidget(label_ex)
