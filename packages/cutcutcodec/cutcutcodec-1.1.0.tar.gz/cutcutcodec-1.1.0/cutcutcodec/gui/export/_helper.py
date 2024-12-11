#!/usr/bin/env python3

"""Helps to avoid redundancy on simple functions."""

import abc
import re

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class ComboBox(CutcutcodecWidget, QtWidgets.QComboBox):
    """Main class for uniformization of QComboBox."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.currentTextChanged.connect(self.text_changed)

        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

    @abc.abstractmethod
    def _text_changed(self, name):
        """Apply the changes."""
        raise NotImplementedError

    def text_changed(self, element):
        """Return the action when a new element is selected."""
        if not element:  # for avoid catching self.clear()
            return
        pattern = r"(?P<name>[a-z0-9_\-]{2,})([\s:]+.*)?"
        name = re.fullmatch(pattern, element)["name"]
        self._text_changed(name)


class CoupleLabelWidget(CutcutcodecWidget, QtWidgets.QWidget):
    """Add a label a the left to a widget."""

    def __init__(self, parent, label_txt, widget_class):
        super().__init__(parent)
        self._parent = parent

        self.widget = widget_class(self)  # Instanciate a CutcutcodecWidget child.
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(QtWidgets.QLabel(label_txt, self), 0, 0)
        grid_layout.addWidget(self.widget, 0, 1)
        self.setLayout(grid_layout)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.widget.refresh()
