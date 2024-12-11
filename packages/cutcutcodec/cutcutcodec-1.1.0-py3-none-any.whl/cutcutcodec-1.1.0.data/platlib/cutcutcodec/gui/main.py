#!/usr/bin/env python3

"""Entry point of the graphic interface."""

import json
import logging
import multiprocessing
import pathlib
import typing

from qtpy import QtCore, QtWidgets

from cutcutcodec.core.analysis.ffprobe import get_streams_type
from cutcutcodec.core.compilation.tree_to_graph import new_node
from cutcutcodec.core.edit.operation.add import add_node
from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
from cutcutcodec.gui.actions import create_actions
from cutcutcodec.gui.app.app import App
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.edition_tabs import EditionTabs
from cutcutcodec.gui.entry_tabs import EntryTabs
from cutcutcodec.gui.export.main import WindowsExportSettings
from cutcutcodec.gui.menu import fill_menu
from cutcutcodec.gui.preferences.main import PreferencesTabs
from cutcutcodec.gui.toolbar import MainToolBar
from cutcutcodec.gui.tools import WaitCursor
from cutcutcodec.gui.video_preview.main import VideoPreview


class MainWindow(CutcutcodecWidget, QtWidgets.QMainWindow):
    """Return the main window for video editing interface."""

    def __init__(self, output: multiprocessing.Queue):
        super().__init__()
        self._parent = None

        self.output = output
        self._app = App()

        self.actions = create_actions(self)

        # declaration
        self.setWindowTitle("cutcutcodec")
        self.sub_windows = {
            "toolbar": MainToolBar(self, self.actions),
            "entry_tabs": EntryTabs(self),
            "video_preview": VideoPreview(self),
            "edition_tabs": EditionTabs(self),
        }
        fill_menu(self.menuBar(), self.actions)

        # location
        self.addToolBar(self.sub_windows["toolbar"])
        h_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        h_splitter.addWidget(self.sub_windows["entry_tabs"])
        h_splitter.addWidget(self.sub_windows["video_preview"])
        v_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical, self)
        v_splitter.addWidget(h_splitter)
        v_splitter.addWidget(self.sub_windows["edition_tabs"])
        self.setCentralWidget(v_splitter)

    @property
    def app(self):
        """Allow to rewrite this method of the parent class."""
        return self._app

    def closeEvent(self, event):
        """Take precautions before properly releasing resources."""
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle("Unregistered changes")
        box.setText("Do you want to save before closing?")
        box.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Save | QtWidgets.QMessageBox.StandardButton.Discard
        )
        box.setIcon(QtWidgets.QMessageBox.Icon.Question)
        button = box.exec()
        if button == QtWidgets.QMessageBox.StandardButton.Save:
            self.save()
        event.accept()

    def crash(self, msg):
        """Display a critical error message."""
        QtWidgets.QMessageBox.critical(None, "Application crashed", msg)

    def export(self):
        """Brings up the export window."""
        self.sub_windows["export"] = WindowsExportSettings(self)
        self.sub_windows["export"].exec()
        del self.sub_windows["export"]

    def import_files(self):
        """Append files to the project."""
        new_files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Import Multimedia Files")
        for file in new_files:
            if not get_streams_type(file, ignore_errors=True):
                logging.error("failed to import %s (not multimedia stream found)", file)
                continue
            node_name, attrs = new_node(self.app.graph, ContainerInputFFMPEG.default())
            attrs["state"]["filename"] = file
            add_node(self.app.graph, node_name, attrs)
            print(f"create {node_name}")
        self.refresh()

    def open(self, file: typing.Union[None, str, pathlib.Path] = None):
        """Load a new project file.

        Parameters
        ----------
        file : pathlike, optional
            The name or path of the file. If not provide, a dialog file explorator windows pop.
        """
        if file is None:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open", filter="*.json")
            if not file:
                return
        assert isinstance(file, (str, pathlib.Path)), file.__class__.__name__
        with open(file, "r", encoding="utf8") as raw:
            state = json.load(raw)
        self.app.__setstate__(state)
        self.app.set_save_file(file)
        self.refresh()

    def preferences(self):
        """Display the preferences window."""
        self.sub_windows["preferences"] = PreferencesTabs(self)
        self.sub_windows["preferences"].exec()
        del self.sub_windows["preferences"]

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        with WaitCursor(self):
            for sub_window in self.sub_windows.values():
                sub_window.refresh()

    def save(self):
        """Save all the state in a file, nn        ."""
        if self.app.get_save_file() is None:
            self.save_as()
            return
        with open(self.app.get_save_file(), "w", encoding="utf8") as file:
            json.dump(self.app.__getstate__(), file, check_circular=False, indent=4, sort_keys=True)

    def save_as(self):
        """Set a new recording file and invoque save."""
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Project", filter="*.json")
        if not file:
            return
        file = pathlib.Path(file)
        file = file.with_suffix(".json")
        self.app.set_save_file(file)
        self.save()
