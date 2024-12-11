#!/usr/bin/env python3

"""Defines the actions."""

from qtpy import QtGui


def create_actions(parent) -> dict[str, QtGui.QAction]:
    """Create all the actions.

    Returns
    -------
    actions : dict
        To each action name, associate the action PyQt ``QtGui.QAction``.
    """
    actions = {}

    actions["export"] = QtGui.QAction("Export", parent)
    actions["export"].setIcon(QtGui.QIcon.fromTheme("media-record"))
    actions["export"].setShortcut("Ctrl+E")
    actions["export"].triggered.connect(parent.export)

    actions["import"] = QtGui.QAction("Import Files", parent)
    actions["import"].setIcon(QtGui.QIcon.fromTheme("list-add"))
    actions["import"].setShortcut("Ctrl+I")
    actions["import"].triggered.connect(parent.import_files)

    actions["open"] = QtGui.QAction("Open", parent)
    actions["open"].setIcon(QtGui.QIcon.fromTheme("document-open"))
    actions["open"].setShortcut(QtGui.QKeySequence.StandardKey.Open)
    # lambda is require even the argument file is provide with a stupid value
    actions["open"].triggered.connect(lambda: parent.open())  # pylint: disable=W0108

    actions["redo"] = QtGui.QAction("Redo", parent)
    actions["redo"].setIcon(QtGui.QIcon.fromTheme("edit-redo"))
    actions["redo"].setShortcut(QtGui.QKeySequence.StandardKey.Redo)
    actions["redo"].triggered.connect(parent.app.redo)

    actions["refresh"] = QtGui.QAction("Refresh", parent)
    actions["refresh"].setIcon(QtGui.QIcon.fromTheme("view-refresh"))
    actions["refresh"].setShortcut(QtGui.QKeySequence.StandardKey.Refresh)
    actions["refresh"].triggered.connect(parent.refresh)

    actions["save"] = QtGui.QAction("Save", parent)
    actions["save"].setIcon(QtGui.QIcon.fromTheme("document-save"))
    actions["save"].setShortcut(QtGui.QKeySequence.StandardKey.Save)
    actions["save"].triggered.connect(parent.save)

    actions["save_as"] = QtGui.QAction("Save as", parent)
    actions["save_as"].setIcon(QtGui.QIcon.fromTheme("document-save-as"))
    actions["save_as"].setShortcut(QtGui.QKeySequence.StandardKey.SaveAs)
    actions["save_as"].triggered.connect(parent.save_as)

    actions["undo"] = QtGui.QAction("Undo", parent)
    actions["undo"].setIcon(QtGui.QIcon.fromTheme("edit-undo"))
    actions["undo"].setShortcut(QtGui.QKeySequence.StandardKey.Undo)
    actions["undo"].triggered.connect(parent.app.undo)

    actions["preferences"] = QtGui.QAction("Preferences", parent)
    actions["preferences"].setIcon(QtGui.QIcon.fromTheme("document-properties"))
    actions["preferences"].setShortcut(QtGui.QKeySequence.StandardKey.Preferences)
    actions["preferences"].triggered.connect(parent.preferences)

    return actions
