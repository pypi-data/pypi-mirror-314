#!/usr/bin/env python3

"""The widget that contains all the elements to pick from to add them to the timeline."""

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.entry.filters import Filters, FiltersAudio, FiltersVideo
from cutcutcodec.gui.entry.generators import Generators, GeneratorsAudio, GeneratorsVideo


class EntryTabs(CutcutcodecWidget, QtWidgets.QWidget):
    """Contains the different selection windows."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        # declaration
        self.generators = Generators(self)
        self.generators_audio = GeneratorsAudio(self)
        self.generators_video = GeneratorsVideo(self)
        self.filters = Filters(self)
        self.filters_audio = FiltersAudio(self)
        self.filters_video = FiltersVideo(self)

        # location
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.generators, "All Generators")
        tabs.addTab(self.generators_audio, "Audio Generators")
        tabs.addTab(self.generators_video, "Video Generators")
        tabs.addTab(self.filters, "All Filters")
        tabs.addTab(self.filters_audio, "Audio Filters")
        tabs.addTab(self.filters_video, "Video Filters")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.generators.refresh()
        self.generators_audio.refresh()
        self.generators_video.refresh()
        self.filters.refresh()
        self.filters_audio.refresh()
        self.filters_video.refresh()
