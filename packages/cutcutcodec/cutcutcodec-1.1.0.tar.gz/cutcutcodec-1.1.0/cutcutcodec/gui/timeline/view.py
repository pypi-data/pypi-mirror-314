#!/usr/bin/env python3

"""Allow drawing the tracks in the timeline."""

from fractions import Fraction
import math

from qtpy import QtCore
import pyqtgraph

from cutcutcodec.gui.base import CutcutcodecWidget
# from cutcutcodec.gui.timeline.track import Track


class TimeAxisItem(pyqtgraph.AxisItem):
    """Internal timestamp for x-axis."""

    def tickStrings(self, values, scale, spacing):
        """Overload the weak default version to provide timestamp."""
        if spacing >= 1e-1:
            return [f"{int(value) // 60:02d}:{value % 60:04.1f}" for value in values]
        return [f"{int(value) // 60:02d}:{value % 60:06.3f}" for value in values]

    def generateSVG(self):
        """Avoid pylint warning."""
        raise NotImplementedError


class View(CutcutcodecWidget, pyqtgraph.widgets.PlotWidget.PlotWidget):
    """Canva with tracks and time rules.

    self.viewRange() -> [[xmin, xmax], [ymin, ymax]]
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.setLimits(xMin=0, minYRange=1, maxYRange=1)
        self.invertY(True)
        self.setAxisItems({"top": TimeAxisItem(orientation="top")})
        self.showAxis("left", False)
        self.showAxis("bottom", False)
        self.sigRangeChanged.connect(View.event_range_changed)

        # self.track = Track(self, self.app.tree())

        self.cursor = pyqtgraph.graphicsItems.InfiniteLine.InfiniteLine(angle=90, movable=True)
        self.cursor.addMarker("<|>", 0, 20)
        self.cursor.sigDragged.connect(self.event_position_changed)  # sigPositionChangeFinished

        # self.scene().addItem(self.track)
        self.addItem(self.cursor)

        # self.showGrid(x=True, y=True)
        # p = self.plot([5, 14, 14, 5, 5], [0, 0, 0.2, 0.2, 0])
        # print(p)

        # self.setYRange(0, 10)

    def event_position_changed(self, cursor):
        """Help when called when the cursor is moved."""
        timestamp = Fraction(cursor.x())
        self.main_window.sub_windows["video_preview"].frame_extractor.set_position(timestamp)

    def event_range_changed(self, box):
        """Help when called when the range is changed."""
        (t_min, t_max), _ = box
        # for track in self.tracks:
        #     track.update_range(t_min, t_max)
        self.parent.slider.update_range(t_min, t_max)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        duration = (
            max((s.beginning+s.duration for s in self.app.tree().in_streams), default=math.inf)
        )
        if duration == math.inf:
            self.setLimits(xMax=None)
        else:
            self.setLimits(xMax=duration)  # duration + 10%

        # if (new_tree := self.app.tree()) != self.track.node:
        #     self.track.update_node(new_tree)
        self.update()

    @QtCore.Slot(Fraction)
    def update_pos(self, timestamp):
        """Set the cursor at the write position."""
        self.cursor.setPos(timestamp)

    def update_range(self, t_min: Fraction, t_max: Fraction):
        """Update the position from slice."""
        self.setXRange(t_min, t_max, padding=0)  # pylint: disable=E1124
