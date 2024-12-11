#!/usr/bin/env python3

"""Allow video and audio previews, but also allows interaction with editing some nodes."""

from fractions import Fraction

from qtpy import QtCore, QtGui, QtWidgets
import numpy as np

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.video_preview.control import ControlBar
from cutcutcodec.gui.video_preview.frame_extractor import FrameExtractor


class VideoPreview(CutcutcodecWidget, QtWidgets.QWidget):
    """Canva with video frames in the background, and objects in the foreground."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        # ``self.__del__`` does not work
        self.destroyed.connect(lambda: self.__del__())  # pylint: disable=W0108

        # creation of main elements
        self.state = {"zoom": True, "frame": np.array(())}
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate
        )
        self.view.resizeEvent = self.resizeEvent
        self.bg_img = self.scene.addPixmap(QtGui.QPixmap())  # the background displayed frame
        self.control_bar = ControlBar(self)
        self.frame_extractor = FrameExtractor(self)
        self.frame_extractor.setTerminationEnabled(True)
        self.frame_extractor.error.connect(self.__del__)
        self.frame_extractor.update_pos.connect(self.update_pos)
        self.frame_extractor.update_frame.connect(self.update_frame)
        self.frame_extractor.start()

        # location
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.control_bar)
        self.setLayout(layout)

    @QtCore.Slot(object)
    def __del__(self, err=None):
        """Kill threads to avoid segfault."""
        if err is not None:
            raise err
        self.frame_extractor.__del__()

    def resizeEvent(self, _):
        """Help when called each times the view shape is changing."""
        if self.state["frame"].size != 0:
            self.update_frame(self.state["frame"])

    def set_zoom_fit(self):
        """Allow to adapt the size of the video to the size of the viewer."""
        self.state["zoom"] = True
        self.update_frame(self.state["frame"])

    def set_zoom_original(self):
        """Allow to adapt the size of the video to the size of the frame."""
        self.state["zoom"] = False
        self.update_frame(self.state["frame"])

    @QtCore.Slot(np.ndarray)
    def update_frame(self, frame: np.ndarray):
        """Redraw the new background frame image."""
        assert isinstance(frame, np.ndarray), frame.__class__.__name__
        self.state["frame"] = frame
        if frame.size == 0:  # if no frame provided
            self.bg_img.setPixmap(QtGui.QPixmap())  # erase the actual background
            return

        # convert image
        assert frame.ndim == 3, frame.shape
        height, width, channels = frame.shape
        assert height >= 1 and width >= 1, (height, width)
        assert frame.dtype == np.uint8, frame.dtype
        if channels == 1:
            img_qt = QtGui.QImage(
                frame.data, width, height, width, QtGui.QImage.Format.Format_Grayscale8
            )
        elif channels == 3:
            img_qt = QtGui.QImage(
                frame.data, width, height, 3*width, QtGui.QImage.Format.Format_BGR888
            )
        else:
            raise ValueError(f"only 1 gray or 3 BGR channels image supprorted, not {channels}")

        # rescale image
        if self.state["zoom"]:
            width, height = self.view.width()-2, self.view.height()-2
            img_qt = img_qt.scaled(
                width,
                height,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,  # no stretching
                QtCore.Qt.TransformationMode.SmoothTransformation,  # bilinear filtering
            )

        # draw image
        self.scene.setSceneRect(0, 0, img_qt.width(), img_qt.height())  # to center the image
        self.bg_img.setPixmap(QtGui.QPixmap.fromImage(img_qt))

    @QtCore.Slot(Fraction)
    def update_pos(self, timestamp):
        """Set the cursor at the write position."""
        self.main_window.sub_windows["edition_tabs"].timeline.view.update_pos(timestamp)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.control_bar.refresh()
        self.frame_extractor.refresh()
