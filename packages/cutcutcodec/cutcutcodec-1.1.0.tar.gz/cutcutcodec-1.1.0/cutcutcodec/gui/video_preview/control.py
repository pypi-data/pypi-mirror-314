#!/usr/bin/env python3

"""The control bar to manage video preview."""

from fractions import Fraction
import math

from qtpy import QtGui, QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class ControlBar(CutcutcodecWidget, QtWidgets.QToolBar):
    """Contains the buttons for the control of the video preview."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.act_start_pause = (
            QtGui.QAction(QtGui.QIcon.fromTheme("media-playback-start"), "start", self)
        )
        self.act_start_pause.triggered.connect(self.set_start_pause)
        self.act_start_pause.setShortcut("space")
        self.addAction(self.act_start_pause)

        self.addSeparator()

        act_seek_backward = (
            QtGui.QAction(QtGui.QIcon.fromTheme("media-skip-backward"), "backward big", self)
        )
        act_seek_backward.triggered.connect(lambda: self.jump(-10))
        self.addAction(act_seek_backward)

        act_backward = QtGui.QAction(QtGui.QIcon.fromTheme("media-seek-backward"), "backward", self)
        act_backward.triggered.connect(lambda: self.jump(-1))
        act_backward.setShortcut("Left")
        self.addAction(act_backward)

        act_pause = QtGui.QAction(QtGui.QIcon.fromTheme("media-playback-stop"), "stop", self)
        act_pause.triggered.connect(self.set_stop)
        self.addAction(act_pause)

        act_forward = QtGui.QAction(QtGui.QIcon.fromTheme("media-seek-forward"), "forward", self)
        act_forward.triggered.connect(lambda: self.jump(1))
        act_forward.setShortcut("Right")
        self.addAction(act_forward)

        act_seek_forward = (
            QtGui.QAction(QtGui.QIcon.fromTheme("media-skip-forward"), "forward big", self)
        )
        act_seek_forward.triggered.connect(lambda: self.jump(10))
        self.addAction(act_seek_forward)

        self.addSeparator()

        act_zoom_fit = QtGui.QAction(QtGui.QIcon.fromTheme("zoom-fit-best"), "zoom fit best", self)
        act_zoom_fit.triggered.connect(self.parent.set_zoom_fit)
        self.addAction(act_zoom_fit)

        act_zoom_original = QtGui.QAction(
            QtGui.QIcon.fromTheme("zoom-original"), "zoom original", self
        )
        act_zoom_original.triggered.connect(self.parent.set_zoom_original)
        self.addAction(act_zoom_original)

    def jump(self, step: int):
        """Take a step backward or forward."""
        curr_pos = self.parent.frame_extractor.dynamic_scheduler.position
        curr_pos = Fraction(0) if curr_pos is None else curr_pos[0]
        if self.parent.frame_extractor.dynamic_scheduler.state["running"]:
            s_a = self.parent.frame_extractor.dynamic_scheduler.get_stream_audio()
            s_v = self.parent.frame_extractor.dynamic_scheduler.get_stream_video()
            durations = []
            if s_a is not None:
                durations.append(s_a.duration)
            if s_v is not None:
                durations.append(s_v.duration)
            if (duration := max(durations, default=math.inf)) == math.inf:
                delta = Fraction(6)
            else:
                delta = duration / 100
        else:
            delta = 1 / self.parent.frame_extractor.dynamic_scheduler.state["fps"]
        self.parent.frame_extractor.set_position(curr_pos + step*delta)

    def set_start_pause(self):
        """Switches between start and pause mode."""
        if self.parent.frame_extractor.dynamic_scheduler.state["running"]:
            self.parent.frame_extractor.set_pause()
        else:
            self.parent.frame_extractor.set_start()

    def set_stop(self):
        """Alias to ``cutcutcodec.gui.video_preview.frame_extractor.FrameExtractor.set_stop``."""
        self.parent.frame_extractor.set_stop()
