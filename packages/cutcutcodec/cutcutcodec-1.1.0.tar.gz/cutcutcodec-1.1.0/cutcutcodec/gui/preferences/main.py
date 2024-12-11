#!/usr/bin/env python3

"""Preference management window."""

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.tools import WaitCursor
from cutcutcodec.gui.preferences.audio_settings import PreferencesAudio
from cutcutcodec.gui.preferences.video_settings import PreferencesVideo


class PreferencesTabs(CutcutcodecWidget, QtWidgets.QDialog):
    """Groups together the different preference management windows."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.widgets = []

        with WaitCursor(self.main_window):
            tabs = QtWidgets.QTabWidget(self)
            for i, stream in enumerate(self.app.tree().in_streams):
                if stream.type == "audio":
                    self.widgets.append(PreferencesAudio(self, i))
                elif stream.type == "video":
                    self.widgets.append(PreferencesVideo(self, i))
                else:
                    raise NotImplementedError(f"not yet supported {stream.type}")
                tabs.addTab(self.widgets[-1], f"Profile Stream {i} ({stream.type})")

            self.setWindowTitle("Preferences")
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(tabs)
            self.setLayout(layout)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        for sub_window in self.widgets:
            sub_window.refresh()
