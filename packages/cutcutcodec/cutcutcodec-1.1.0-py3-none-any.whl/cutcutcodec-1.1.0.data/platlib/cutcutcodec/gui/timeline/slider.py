#!/usr/bin/env python3

"""Allow for simple navigation through time."""

from fractions import Fraction
import math

from qtpy import QtCore, QtGui, QtWidgets

from cutcutcodec.gui.base import CutcutcodecWidget


class QRangeSlider(QtWidgets.QSlider):
    """Like QtWidgets.QSlider with 2 buttons.

    Based on https://stackoverflow.com/questions/67028200/pyqt5-qslider-two-positions.
    """

    sliderMoved = QtCore.Signal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._low, self._high = self.minimum(), self.maximum()

        self.pressed_control = QtWidgets.QStyle.SubControl.SC_None
        self.hover_control = QtWidgets.QStyle.SubControl.SC_None
        self.click_offset = 0
        self.active_slider = 0  # 0 for the low, 1 for the high, -1 for both

    def _pick(self, point):
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return point.x()
        return point.y()

    def _pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QtWidgets.QApplication.style()

        g_r = style.subControlRect(
            style.ComplexControl.CC_Slider, opt, style.SubControl.SC_SliderGroove, self
        )
        s_r = style.subControlRect(
            style.ComplexControl.CC_Slider, opt, style.SubControl.SC_SliderHandle, self
        )

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            slider_length = s_r.width()
            slider_min = g_r.x()
            slider_max = g_r.right() - slider_length + 1
        else:
            slider_length = s_r.height()
            slider_min = g_r.y()
            slider_max = g_r.bottom() - slider_length + 1

        return style.sliderValueFromPosition(
            self.minimum(), self.maximum(), pos-slider_min, slider_max-slider_min, opt.upsideDown
        )

    def low(self):
        """Return the low position."""
        return self._low

    def setLow(self, low: int):
        """Update the low position."""
        self._low = low
        self.update()

    def high(self):
        """Return the high position."""
        return self._high

    def setHigh(self, high: int):
        """Update the hight position."""
        self._high = high
        self.update()

    def paintEvent(self, _):
        """Draw the slider.

        Based on http://qt.gitorious.org/qt/qt/blobs/master/src/gui/widgets/qslider.cpp.
        """
        painter = QtGui.QPainter(self)
        style = QtWidgets.QApplication.style()

        # draw groove
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        opt.siderValue = 0
        opt.sliderPosition = 0
        opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderGroove
        style.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self)
        groove = style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderGroove,
            self,
        )

        # drawSpan
        self.initStyleOption(opt)
        opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderGroove
        opt.siderValue = 0
        opt.sliderPosition = self._low
        low_rect = style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderHandle,
            self,
        )
        opt.sliderPosition = self._high
        high_rect = style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderHandle,
            self,
        )

        low_pos = self._pick(low_rect.center())
        high_pos = self._pick(high_rect.center())
        min_pos = min(low_pos, high_pos)
        max_pos = max(low_pos, high_pos)

        cursor = QtCore.QRect(low_rect.center(), high_rect.center()).center()
        if opt.orientation == QtCore.Qt.Orientation.Horizontal:
            span_rect = QtCore.QRect(
                QtCore.QPoint(min_pos, cursor.y()-2), QtCore.QPoint(max_pos, cursor.y()+1)
            )
        else:
            span_rect = QtCore.QRect(
                QtCore.QPoint(cursor.x()-2, min_pos), QtCore.QPoint(cursor.x()+1, max_pos)
            )

        if opt.orientation == QtCore.Qt.Orientation.Horizontal:
            groove.adjust(0, 0, -1, 0)
        else:
            groove.adjust(0, 0, 0, -1)

        highlight = self.palette().color(QtGui.QPalette.ColorRole.Highlight)
        painter.setBrush(QtGui.QBrush(highlight))
        painter.setPen(QtGui.QPen(highlight, 0))
        painter.drawRect(span_rect.intersected(groove))

        for value in (self._low, self._high):
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider so it doesn't get drawn
            # on top of the existing ones every time
            opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderHandle

            # if self.tickPosition() != QtWidgets.QSlider.TickPosition.NoTicks:
            #     opt.subControls |= QtWidgets.QStyle.SubControl.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
            else:
                opt.activeSubControls = self.hover_control

            opt.sliderPosition = value
            opt.sliderValue = value
            style.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self)

    def mousePressEvent(self, event):
        """When the mouse is pressed on the slider."""
        event.accept()

        style = QtWidgets.QApplication.style()
        button = event.button()

        # In a normal slider control, when the user clicks on a point in the
        # slider's total range, but not on the slider part of the control the
        # control would jump the slider value to where the user clicked.
        # For this control, clicks which are not direct hits will slide both
        # slider parts

        if button:
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            self.active_slider = -1

            if self._low + self._high > self.minimum() + self.maximum():
                i_value = ((0, self._low), (1, self._high))
            else:
                i_value = ((1, self._high), (0, self._low))
            for i, value in i_value:
                opt.sliderPosition = value
                hit = style.hitTestComplexControl(
                    style.ComplexControl.CC_Slider, opt, event.pos(), self
                )
                if hit == style.SubControl.SC_SliderHandle:
                    self.active_slider = i
                    self.pressed_control = hit

                    self.triggerAction(self.SliderAction.SliderMove)
                    self.setRepeatAction(self.SliderAction.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider < 0:
                self.pressed_control = QtWidgets.QStyle.SubControl.SC_SliderHandle
                self.click_offset = self._pixelPosToRangeValue(self._pick(event.pos()))
                self.triggerAction(self.SliderAction.SliderMove)
                self.setRepeatAction(self.SliderAction.SliderNoAction)
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        """When the curseor is mooved."""
        if self.pressed_control != QtWidgets.QStyle.SubControl.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        new_pos = self._pixelPosToRangeValue(self._pick(event.pos()))
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)

        if self.active_slider < 0:
            offset = new_pos - self.click_offset
            self._high += offset
            self._low += offset
            if self._low < self.minimum():
                diff = self.minimum() - self._low
                self._low += diff
                self._high += diff
            if self._high > self.maximum():
                diff = self.maximum() - self._high
                self._low += diff
                self._high += diff
        elif self.active_slider == 0:
            if new_pos >= self._high:
                new_pos = self._high - 1
            self._low = new_pos
        else:
            if new_pos <= self._low:
                new_pos = self._low + 1
            self._high = new_pos

        self.click_offset = new_pos

        self.update()

        self.sliderMoved.emit(self._low, self._high)


class Slider(CutcutcodecWidget, QRangeSlider):
    """Return the slider for adapt the view."""

    def __init__(self, parent):
        self._parent = parent
        super().__init__(QtCore.Qt.Orientation.Horizontal, parent)

        self.sliderMoved.connect(self.slider_moved)

        self.setMinimum(0)
        self.setMaximum(3600*1000)
        self.setLow(0)
        self.setHigh(600*1000)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        duration = (
            max((s.beginning+s.duration for s in self.app.tree().in_streams), default=math.inf)
        )
        if duration == math.inf:
            self.setMaximum(3600*1000)  # 1h
        else:
            self.setMaximum(round(1000*duration))

        if self.low() >= self.maximum():
            self.setLow(0)
        if self.high() > self.maximum():
            self.setHigh(self.maximum())

    def slider_moved(self, low, high):
        """Help when called when the slider is moved by user."""
        self.parent.view.update_range(Fraction(low, 1000), Fraction(high, 1000))

    def update_range(self, t_min, t_max):
        """Help when called when the timeline is moved by user."""
        low, high = round(1000*t_min), round(1000*t_max)
        self.setLow(low)
        self.setHigh(high)
