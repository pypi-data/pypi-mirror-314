#!/usr/bin/env python3

"""Definition of the toolbar."""

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class MainToolBar(CutcutcodecWidget, QtWidgets.QToolBar):
    """Main window menu bar."""

    def __init__(self, parent, actions):
        super().__init__(parent)
        self._parent = parent

        self.addAction(actions["import"])
        self.addAction(actions["open"])
        self.addAction(actions["save"])

        self.addSeparator()

        self.addAction(actions["refresh"])
        self.addAction(actions["undo"])
        self.addAction(actions["redo"])

        self.addSeparator()

        self.addAction(actions["export"])
