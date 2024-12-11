#!/usr/bin/env python3

"""The widget that contains all the elements for the video edition."""

from qtpy import QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.flowchart.main import FlowChart
from cutcutcodec.gui.timeline.main import Timeline


class EditionTabs(CutcutcodecWidget, QtWidgets.QWidget):
    """Contains the different selection windows."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        # declaration
        self.timeline = Timeline(self)
        self.flowchart = FlowChart(self)

        # location
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.timeline, "Timeline")
        tabs.addTab(self.flowchart, "Flow Chart")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.timeline.refresh()
        self.flowchart.refresh()
