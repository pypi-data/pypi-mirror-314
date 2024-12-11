#!/usr/bin/env python3

"""Interactive widget for help to choose the export muxer settings."""

import pathlib

from qtpy import QtCore, QtWidgets

from cutcutcodec.core.classes.muxer import AllMuxers, Muxer
from cutcutcodec.core.compilation.export.compatibility import Compatibilities
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.export._helper import ComboBox
from cutcutcodec.gui.export.doc import DocViewer
from cutcutcodec.gui.tools import WaitCursor


class MuxerComboBox(ComboBox):
    """List the availables muxers."""

    def _text_changed(self, name: str):
        if name == "default":
            name = None
        if self.app.export_settings["muxer"] != name:
            with WaitCursor(self.parent.parent):
                self.app.export_settings["muxer"] = name
                print(f"update muxer: {self.app.export_settings['muxer']}")
                if name is not None:
                    suffix = sorted(Muxer(name).extensions)
                    suffix = suffix.pop(0) if len(suffix) >= 1 else ""
                else:
                    suffix = ""
                if self.app.export_settings["suffix"] != suffix:
                    self.app.export_settings["suffix"] = suffix
                    print(f"update export suffix: {self.app.export_settings['suffix']}")
                self.parent.parent.refresh()  # WindowsExportSettings

    def available_muxers(self) -> set[str]:
        """Set of muxers compatible with all the streams.

        The returned muxers are tested to ensure the compatibility with all the encoders.
        """
        muxers = sorted(AllMuxers().set)
        tree = self.app.tree()

        # process by elimination
        for stream, encoder, rate in zip(  # starts by audio because is faster than video
            tree.in_select("audio"),
            self.app.export_settings["encoders"]["audio"],
            self.app.export_settings["rates"]["audio"],
        ):
            if encoder is not None:
                encoders = [encoder]
            else:
                encoders = sorted(
                    self.parent.parent.encoders_widgets[tree.in_index(stream)]
                    .widgets["encoder_combo_box"]
                    .available_encoders()
                )
            comp = Compatibilities().check(  # we should to forward 'profile' as well
                encoders, muxers,
                layout=stream.layout.name,
                rate=rate,
            )
            muxers = [m for m, a in zip(muxers, (comp != "").any(axis=0)) if a]
        for stream, encoder, shape, rate, pix_fmt in zip(  # continue elimination with video
            tree.in_select("video"),
            self.app.export_settings["encoders"]["video"],
            self.app.export_settings["shapes"],
            self.app.export_settings["rates"]["video"],
            self.app.export_settings["pix_fmt"],
        ):
            if encoder is not None:
                encoders = [encoder]
            else:
                encoders = sorted(
                    self.parent.parent.encoders_widgets[tree.in_index(stream)]
                    .widgets["encoder_combo_box"]
                    .available_encoders()
                )
            comp = Compatibilities().check(
                encoders, muxers,
                shape=shape,
                rate=rate,
                pix_fmt=pix_fmt,
            )
            muxers = [m for m, a in zip(muxers, (comp != "").any(axis=0)) if a]
        return set(muxers)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.clear()
        self.addItem(self.app.export_settings["muxer"] or "default")
        for muxer in [None] + sorted(self.available_muxers()):
            if muxer == self.app.export_settings["muxer"]:
                continue
            self.addItem(muxer or "default")  # QtGui.QIcon.fromTheme("video-x-generic")


class FileNameSelector(CutcutcodecWidget, QtWidgets.QWidget):
    """File manager for select the filename."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self._textbox = QtWidgets.QLineEdit(self)
        self._textbox.editingFinished.connect(self._validate_path)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self._textbox, 0, 0)
        button = QtWidgets.QPushButton("Select", self)
        button.clicked.connect(self.filename_dialog)
        button.setAutoDefault(False)
        grid_layout.addWidget(button, 0, 1)
        self.setLayout(grid_layout)

    def _validate_path(self, new_path):
        """Try to validate the new path if it is valid."""
        try:
            self.update_path(new_path)
        except ValueError:
            self._textbox.setStyleSheet("background:red;")
        else:
            self._textbox.setStyleSheet("background:none;")

    def filename_dialog(self):
        """Open a window to choose a new file name."""
        new_path, _ = QtWidgets.QFileDialog.getSaveFileName(self)
        if new_path:
            try:
                self.update_path(new_path)
            except AssertionError as err:
                QtWidgets.QMessageBox.warning(
                    None, "Invalid filename", f"Unable to change the filename {new_path} : {err}"
                )

    def update_path(self, new_path):
        """Check that the new path is correct and set the new path in the settings."""
        with WaitCursor(self.parent.parent):
            assert isinstance(new_path, str), new_path.__class__.__name__
            new_path = pathlib.Path(new_path)
            if new_path.is_dir():
                raise ValueError(f"the path {new_path} can not be a directory")
            if not new_path.parent.is_dir():
                raise ValueError(f"the parent of {new_path} has to be a directory")
            if new_path.suffix and all(
                new_path.suffix != suf
                for mux in self.parent.muxer_combo_box.available_muxers()
                for suf in Muxer(mux).extensions
            ):
                raise ValueError(f"the suffix {new_path.suffix} not allow")

            modif = False

            if self.app.export_settings["parent"] != str(new_path.parent):
                modif = True
                self.app.export_settings["parent"] = str(new_path.parent)
                print(f"update directory: {self.app.export_settings['parent']}")
            if self.app.export_settings["stem"] != new_path.stem:
                modif = True
                self.app.export_settings["stem"] = new_path.stem
                print(f"update file stem: {self.app.export_settings['stem']}")
            if new_path.suffix != self.app.export_settings["suffix"]:
                modif = True
                self.app.export_settings["suffix"] = new_path.suffix
                print(f"update suffix: {self.app.export_settings['suffix']}")
                if new_path.suffix:
                    self.app.export_settings["muxer"] = Muxer(new_path.suffix).name
                    print(f"update muxer: {self.app.export_settings['muxer']}")

            if modif:
                self.parent.parent.refresh()  # WindowsExportSettings

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        new_text = str(
            (
                pathlib.Path(self.app.export_settings['parent'])
                / self.app.export_settings['stem']
            )
            .with_suffix(self.app.export_settings['suffix'])
        )
        self._textbox.setStyleSheet("background:none;")
        self._textbox.setText(new_text)


class ContainerSettings(CutcutcodecWidget, QtWidgets.QWidget):
    """Settings of the container file."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.filename_selector = FileNameSelector(self)
        self.muxer_combo_box = MuxerComboBox(self)
        self.muxer_doc_viewer = DocViewer(
            self,
            self.app.export_settings["muxer_settings"],
            lambda w: (
                "" if (muxer := w.app.export_settings["muxer"]) is None
                else Muxer(muxer).doc
            )
        )
        self.muxer_doc_viewer.hide()

        layout = QtWidgets.QGridLayout()
        self.init_title(layout)
        layout.addWidget(QtWidgets.QLabel("Path:", self), 1, 0)
        layout.addWidget(self.filename_selector, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Muxer:", self), 2, 0)
        layout.addWidget(self.muxer_combo_box, 2, 1)
        layout.addWidget(self.muxer_doc_viewer, 3, 0, 1, 2)
        self.setLayout(layout)

    def init_title(self, layout):
        """Return the section title."""
        title = QtWidgets.QLabel("Muxer Settings")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        layout.addWidget(title, 0, 0, 1, 2)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.filename_selector.refresh()
        self.muxer_combo_box.refresh()
        self.muxer_doc_viewer.refresh()
