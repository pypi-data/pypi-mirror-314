#!/usr/bin/env python3

"""Generate the frame in background for the requierd timestamp.

Allows to send audio and video frames in order to have a preview of the current editing.
"""

from fractions import Fraction
import functools
import queue
import threading
import time
import typing

from qtpy import QtCore, QtGui
import numpy as np

from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
from cutcutcodec.core.classes.frame import Frame
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream_audio import StreamAudio
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.compilation.export.rate import suggest_audio_rate
from cutcutcodec.core.compilation.export.rate import suggest_video_rate
from cutcutcodec.core.exceptions import MissingStreamError, OutOfTimeRange
from cutcutcodec.core.io.scheduler import scheduler
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.video_preview.audio_player import AudioPlayer


def _catch_none(func):
    """Call in loop while until res is not None."""
    @functools.wraps(func)
    def func_no_none(*args, **kwargs):
        res = None
        while res is None:
            res = func(*args, **kwargs)
        return res
    return func_no_none


class DynamicSheduler:
    """Yield in real time the frame updated with the current parameters."""

    def __init__(self, frame_extractor):
        self.frame_extractor = frame_extractor
        self.lock = threading.Lock()
        self.position = None
        self.priority_frames = queue.Queue()
        self.scheduler = None
        self.state = {
            "running": False,
            "rate": 48000,
            "fps": Fraction(30000, 1001),
            "shape": (1080, 720),
        }

    @_catch_none
    def __next__(self) -> typing.Union[None, Frame]:
        """Wait and return the next frame at the right moment (real time)."""
        while True:
            if not self.state["running"]:  # if need pause
                return self.priority_frames.get()
            try:
                return self.priority_frames.get_nowait()
            except queue.Empty:
                pass
            if self.scheduler is None:
                self.update_scheduler()
            with self.lock:
                try:
                    _, frame = next(self.scheduler)
                except (StopIteration, TypeError, MissingStreamError):
                    # if we reach the end of the stream
                    # or if self.scheduler set to None in background,
                    # or if the user try forward after the end of the stream
                    self.frame_extractor.set_pause()
                    continue
                self.position = self.position or (frame.time, time.time())
                date_theo = self.position[1] + frame.time - self.position[0]
                if (sleep_time := date_theo - time.time()) > 0:
                    time.sleep(sleep_time)  # overrun -> real time
                elif sleep_time < -0.01:  # if big underun (>10ms), assume delay not catchable
                    date_theo -= sleep_time  # reset counter for next frame, (= time.time())
                self.position = (frame.time, date_theo)
            return frame

    def __iter__(self):
        """Make the object compatible with the for loop."""
        return self

    def get_stream_audio(self) -> typing.Union[None, StreamAudio]:
        """Return as possible the first audio stream."""
        for stream in self.frame_extractor.app.tree().in_streams:
            if stream.type == "audio":
                return stream
        return None

    def get_stream_video(self) -> typing.Union[None, StreamVideo]:
        """Return as possible the first video stream."""
        for stream in self.frame_extractor.app.tree().in_streams:
            if stream.type == "video":
                return stream
        return None

    def update_scheduler(self):
        """Get an updated version of ``cutcutcodec.core.io.scheduler.scheduler`` iterator."""
        streams, rates = [], []
        if (stream := self.get_stream_video()) is not None:
            streams.append(stream)
            rates.append(self.state["fps"])
        if (stream := self.get_stream_audio()) is not None:
            streams.append(stream)
            rates.append(self.state["rate"])
        if not streams:
            raise MissingStreamError("no audio or video stream founded in output")
        start_time = Fraction(0) if self.position is None else self.position[0]
        scheduler_ = (
            iter(scheduler(streams, rates, start_time=start_time, shape=self.state["shape"]))
        )
        with self.lock:
            self.position = None
            self.scheduler = scheduler_
            self.priority_frames.put(None)  # relunch


class FrameExtractor(CutcutcodecWidget, QtCore.QThread):
    """Non-blocking thread allowing to quietly extract frames in the background."""

    update_frame = QtCore.Signal(np.ndarray)
    update_pos = QtCore.Signal(Fraction)
    error = QtCore.Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._stop = False
        self.dynamic_scheduler = DynamicSheduler(self)
        self.audio_player = AudioPlayer(daemon=True)
        self.audio_player.start()

    def __del__(self):
        """Stop the thread automaticaly when the object is deleted."""
        self._stop = True
        self.audio_player.stop()  # this is blocking
        self.wait(1000)  # timeout in ms
        if not self.isFinished():
            self.terminate()
            self.wait(1000)  # timeout in ms

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        # update fps, samplerate and shape
        if stream := self.dynamic_scheduler.get_stream_audio():
            rate = self.app.export_settings["rates"]["audio"]
            rate = rate[0] if rate else suggest_audio_rate(stream)
            if rate is None:
                rate = suggest_audio_rate(stream)
            self.dynamic_scheduler.state["rate"] = rate
        if stream := self.dynamic_scheduler.get_stream_video():
            fps = self.app.export_settings["rates"]["video"]
            fps = fps[0] if fps else suggest_video_rate(stream)
            if fps is None:
                fps = suggest_video_rate(stream)
            else:
                fps = Fraction(fps)
            self.dynamic_scheduler.state["fps"] = fps
            shape = self.app.export_settings["shapes"]
            shape = shape[0] if shape else (720, 1080)
            if shape is None:
                shape = optimal_shape_video(stream) or (720, 1080)
            self.dynamic_scheduler.state["shape"] = shape

        # refresh the frame at the current position
        curr_pos = self.dynamic_scheduler.position
        curr_pos = Fraction(0) if curr_pos is None else curr_pos[0]
        self.set_position(curr_pos)  # allways reset the scheduler

    def run(self):
        """Extract frames in background until death."""
        try:
            while not self._stop:
                for frame in self.dynamic_scheduler:
                    self.update_pos.emit(frame.time)
                    if self._stop:
                        break
                    if isinstance(frame, FrameVideo):
                        self.update_frame.emit(frame.to_numpy_bgr(contiguous=True))
                    elif isinstance(frame, FrameAudio):
                        self.audio_player.update_frame(frame)
                    else:
                        raise NotImplementedError("only audio and video frame are supported")
        except Exception as err:  # pylint: disable=W0718
            threading.Thread(target=self.error.emit, args=(err,), daemon=True).start()

    @QtCore.Slot()
    def set_pause(self):
        """Stop reading and updates icon."""
        if not self.dynamic_scheduler.state["running"]:  # if it is already in pause
            return  # do nothing
        self.parent.control_bar.act_start_pause.setIcon(
            QtGui.QIcon.fromTheme("media-playback-start")
        )
        self.parent.control_bar.act_start_pause.setText("start")
        self.dynamic_scheduler.state["running"] = False

    @QtCore.Slot(Fraction)
    def set_position(self, pos: Fraction):
        """Seek the preview to the given position."""
        assert isinstance(pos, Fraction), pos.__class__.__name__

        # set the new position
        delta = self.dynamic_scheduler.state["fps"]
        if rest := pos % (1/delta):
            pos += 1/delta - rest  # pos = k*(1/fps), k integer
        with self.dynamic_scheduler.lock:
            self.dynamic_scheduler.scheduler = None
            self.dynamic_scheduler.position = [pos, time.time()]

        # extrat one frame at the given position
        if (stream := self.dynamic_scheduler.get_stream_video()) is not None:
            try:
                frame = stream.snapshot(pos, self.dynamic_scheduler.state["shape"])
            except OutOfTimeRange:
                pass
            else:
                self.dynamic_scheduler.priority_frames.put(frame)
        if (stream := self.dynamic_scheduler.get_stream_audio()) is not None:
            rate = self.dynamic_scheduler.state["rate"]
            try:
                frame = stream.snapshot(pos, rate, max(1, rate//10))  # 100 ms
            except OutOfTimeRange:
                pass
            else:
                self.dynamic_scheduler.priority_frames.put(frame)

    @QtCore.Slot()
    def set_start(self):
        """Stop reading and updates icon."""
        if self.dynamic_scheduler.state["running"]:  # if it is already playing
            return  # do nothing
        self.parent.control_bar.act_start_pause.setIcon(
            QtGui.QIcon.fromTheme("media-playback-pause")
        )
        self.parent.control_bar.act_start_pause.setText("pause")
        self.dynamic_scheduler.state["running"] = True
        self.dynamic_scheduler.priority_frames.put(None)  # relunch

    @QtCore.Slot()
    def set_stop(self):
        """Pause and return to the beginning."""
        self.set_pause()
        self.set_position(Fraction(0))
