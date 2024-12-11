#!/usr/bin/env python3

"""Allow to select the parameters of a video stream."""

from fractions import Fraction
import re

from qtpy import QtWidgets

from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
from cutcutcodec.core.compilation.export.rate import suggest_video_rate
from cutcutcodec.gui.base import CutcutcodecWidget


CLASSICAL_FPS = {
    Fraction(15): "animation",
    Fraction(24000, 1001): "old cinema",
    Fraction(24): "old cinema",
    Fraction(25): "old television",
    Fraction(30000, 1001): "standard",
    Fraction(30): "cinema",
    Fraction(50): "interlaced television",
    Fraction(60000, 1001): "modern television",
    Fraction(60): "computer screen",
    Fraction(120): "human perception threshold",
    Fraction(240): "slow-motion",
    Fraction(300): "slow-motion",
}
CLASSICAL_SHAPES = {  # numpy convention (height, width)
    (240, 320): "QVGA",
    (240, 426): "240p",
    (360, 480): "",
    (360, 640): "360p",
    (480, 320): "HVGA",
    (480, 640): "VGA",
    (480, 854): "480p",
    (576, 768): "PAL",
    (600, 800): "SVGA",
    (720, 960): "",
    (720, 1280): "720p HD High Definition",
    (768, 1024): "XGA",
    (900, 1200): "",
    (960, 1280): "",
    (1050, 1400): "SXGA",
    (1080, 1920): "1080p FHD Full HD",
    (1200, 1600): "UXGA",
    (1440, 1920): "",
    (1440, 2560): "1440p QHD Quad HD",
    (1536, 2048): "QXGA",
    (1707, 2276): "",
    (1920, 2560): "",
    (2160, 3840): "4K UHD Ultra HD",
    (4320, 7680): "8K Full Ultra HD",
}


def _format_shape(shape: tuple[int, int]) -> str:
    height, width = shape
    ratio = Fraction(width, height).limit_denominator(20)
    text = f"{width}x{height} {ratio.numerator}:{ratio.denominator}"
    if CLASSICAL_SHAPES.get(shape, ""):
        text = f"{text} ({CLASSICAL_SHAPES[shape]})"
    return text


class PreferencesVideo(CutcutcodecWidget, QtWidgets.QWidget):
    """Allow to select the frame rate and the resolution of a video stream."""

    def __init__(self, parent, index_abs):
        super().__init__(parent)
        self._parent = parent

        self.widgets = {"fpstext": None, "fpscomb": None, "shapetext": None, "shapecomb": None}

        tree = self.app.tree()
        self.stream = tree.in_streams[index_abs]
        self.index_rel = None
        for i, stream in enumerate(tree.in_select("video")):
            if stream is self.stream:
                self.index_rel = i
        assert self.index_rel is not None, "the output container has been modified in background"

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_fps(grid_layout)
        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        grid_layout.addWidget(separador, ref_span, 0, 1, 2)
        self.init_shape(grid_layout, ref_span=ref_span+1)
        self.setLayout(grid_layout)
        self.refresh()

    def _select_fps(self, text: str):
        """From combo box."""
        # decode the fps Fraction or None
        if "automatic" in text:
            fps = None
        elif text == "manual":
            fps = self.best_fps
        else:
            fps = Fraction(max(re.findall(r"\d+/?\d*", text), key=len))

        # update only if it changed
        if (curr_fps := self.app.export_settings["rates"]["video"][self.index_rel]) is not None:
            curr_fps = Fraction(curr_fps)
        if fps != curr_fps:
            self.app.export_settings["rates"]["video"][self.index_rel] = (
                None if fps is None else str(fps)
            )
            print(f"update fps (stream video {self.index_rel}) to {fps}")
            self.main_window.refresh()

    def _select_shape(self, text: str):
        """From combo box."""
        # decode the shape (tuple[int, int] or None)
        if "automatic" in text:
            shape = None
        elif text == "manual":
            shape = (
                self.app.export_settings["shapes"][self.index_rel]
                or optimal_shape_video(self.stream)
                or (720, 1080)
            )
        else:
            shape = tuple(map(int, re.findall(r"\d+", text)))[1::-1]
            if len(shape) != 2 or shape[0] <= 0 or shape[1] <= 0:
                self.widgets["shapetext"].setStyleSheet("background:red;")
                return

        # update only if it changed
        if shape != self.app.export_settings["shapes"][self.index_rel]:
            self.app.export_settings["shapes"][self.index_rel] = shape
            print(f"update shape (stream video {self.index_rel}) to {shape}")
            self.main_window.refresh()

    def _validate_fps(self):
        """Check that the frame rate is a correct fraction."""
        text = self.widgets["fpstext"].text()
        if re.fullmatch(r"\s*", text):
            self._select_fps("automatic")
            return
        try:
            fps = Fraction(text).limit_denominator(1001)
        except (ValueError, ZeroDivisionError):
            self.widgets["fpstext"].setStyleSheet("background:red;")
            return
        if fps <= 0:
            self.widgets["fpstext"].setStyleSheet("background:red;")
            return
        self._select_fps(str(fps))

    def _validate_shape(self):
        """Check that the shape is correct."""
        text = self.widgets["shapetext"].text()
        if re.fullmatch(r"\s*", text):
            self._select_shape("automatic")
            return
        self._select_shape(text)

    @property
    def best_fps(self) -> Fraction:
        """Return the most appropriated frame rate for the current configuration.

        If the fps is specified by the user, it returns the given fps.
        Otherwise it ask to ``cutcutcodec.core.compilation.export.rate.suggest_video_rate``
        for the best estimation.
        """
        if (fps := self.app.export_settings["rates"]["video"][self.index_rel]) is not None:
            return Fraction(fps)
        return suggest_video_rate(self.stream)

    def init_fps(self, grid_layout, ref_span=0):
        """Display and allows to modify the framerate."""
        grid_layout.addWidget(QtWidgets.QLabel("Frame Rate (fps):"), ref_span, 0)
        self.widgets["fpstext"] = QtWidgets.QLineEdit()
        self.widgets["fpstext"].editingFinished.connect(self._validate_fps)
        grid_layout.addWidget(self.widgets["fpstext"], ref_span, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Selection:"), ref_span+1, 0)
        self.widgets["fpscomb"] = QtWidgets.QComboBox()
        self.widgets["fpscomb"].textActivated.connect(self._select_fps)
        grid_layout.addWidget(self.widgets["fpscomb"], ref_span+1, 1)
        return ref_span + 2

    def init_shape(self, grid_layout, ref_span=0):
        """Display and allows to modify the shape of the frames."""
        grid_layout.addWidget(QtWidgets.QLabel("Resolution (width x height):"), ref_span, 0)
        self.widgets["shapetext"] = QtWidgets.QLineEdit()
        self.widgets["shapetext"].editingFinished.connect(self._validate_shape)
        grid_layout.addWidget(self.widgets["shapetext"], ref_span, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Selection:"), ref_span+1, 0)
        self.widgets["shapecomb"] = QtWidgets.QComboBox()
        self.widgets["shapecomb"].textActivated.connect(self._select_shape)
        grid_layout.addWidget(self.widgets["shapecomb"], ref_span+1, 1)
        return ref_span + 2

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.refresh_fps()
        self.refresh_shape()

    def refresh_fps(self):
        """Refresh the data related to the fps."""
        def format_fps(fps: Fraction) -> str:
            if fps.denominator == 1:
                text = str(fps.numerator)
            else:
                text = f"{float(fps):.2f} = {fps}"
            if CLASSICAL_FPS.get(fps, ""):
                text = f"{text} ({CLASSICAL_FPS[fps]})"
            return text

        # update combobox items
        self.widgets["fpscomb"].clear()
        self.widgets["fpscomb"].addItem("automatic")
        self.widgets["fpscomb"].addItem("manual")
        self.widgets["fpscomb"].addItems(map(format_fps, sorted(CLASSICAL_FPS)))

        # select the right combobox item
        if (fps := self.app.export_settings["rates"]["video"][self.index_rel]) is None:
            self.widgets["fpscomb"].setCurrentText("automatic")
        else:
            fps = Fraction(fps)
            if fps in CLASSICAL_FPS:
                self.widgets["fpscomb"].setCurrentText(format_fps(fps))
            else:
                self.widgets["fpscomb"].setCurrentText("manual")

        # update textbox item
        self.widgets["fpstext"].setPlaceholderText(str(suggest_video_rate(self.stream)))
        if (fps := self.app.export_settings["rates"]["video"][self.index_rel]) is not None:
            self.widgets["fpstext"].setText(fps)
        else:
            self.widgets["fpstext"].setText("")
        self.widgets["fpstext"].setStyleSheet("background:none;")

    def refresh_shape(self):
        """Refresh the data related to the shape."""
        # update combobox items
        self.widgets["shapecomb"].clear()
        self.widgets["shapecomb"].addItem("automatic")
        self.widgets["shapecomb"].addItem("manual")
        self.widgets["shapecomb"].addItems(map(_format_shape, sorted(CLASSICAL_SHAPES)))

        # select the right combobox item
        if (shape := self.app.export_settings["shapes"][self.index_rel]) is None:
            self.widgets["shapecomb"].setCurrentText("automatic")
        elif shape in CLASSICAL_SHAPES:
            self.widgets["shapecomb"].setCurrentText(_format_shape(shape))
        else:
            self.widgets["shapecomb"].setCurrentText("manual")

        # update textbox item
        shape = optimal_shape_video(self.stream) or (720, 1080)
        self.widgets["shapetext"].setPlaceholderText("x".join(map(str, shape[::-1])))  # h*w to w*h
        if (shape := self.app.export_settings["shapes"][self.index_rel]) is not None:
            self.widgets["shapetext"].setText("x".join(map(str, shape[::-1])))  # h*w to w*h
        else:
            self.widgets["shapetext"].setText("")
        self.widgets["shapetext"].setStyleSheet("background:none;")
