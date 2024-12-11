#!/usr/bin/env python3

"""Decode the streams of a multimedia file based on ffmpeg.

Decodes video and audio. Images are not well decoded here.
"""

from fractions import Fraction
import logging
import math
import numbers
import pathlib
import threading
import typing

import av
import numpy as np
import torch

from cutcutcodec.core.analysis.audio.properties.duration import get_duration_audio
from cutcutcodec.core.analysis.ffprobe import _estimate_rate_ffmpeg
from cutcutcodec.core.analysis.ffprobe import get_streams_type
from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.layout import Layout
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_audio import StreamAudio
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import (
    DecodeError, MissingInformation, MissingStreamError, OutOfTimeRange
)
from cutcutcodec.core.filter.video.pad import pad_keep_ratio
from cutcutcodec.utils import get_project_root


class ContainerInputFFMPEG(ContainerInput):
    """Allow to decode a multimedia file with ffmpeg.

    Attributes
    ----------
    av_kwargs : dict[str]
        The parameters passed to ``av.open``.
    filename : pathlib.Path
        The path to the physical file that contains the extracted video stream (readonly).

    Notes
    -----
    In order to avoid the folowing error :
        ``av.error.InvalidDataError: [Errno 1094995529] Invalid data found when processing input;
        last error log: [libdav1d] Error parsing OBU data``
    Which happens when reading a multi-stream file sparingly, The instances of
    ``av.container.InputContainer`` are new for each stream.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
    >>> with ContainerInputFFMPEG("cutcutcodec/examples/intro.webm") as container:
    ...     for stream in container.out_streams:
    ...         if stream.type == "video":
    ...             stream.snapshot(0, (stream.height, stream.width)).shape
    ...         elif stream.type == "audio":
    ...             torch.round(stream.snapshot(0, rate=2, samples=3), decimals=5)
    ...
    (720, 1280, 3)
    (360, 640, 3)
    FrameAudio(0, 2, 'stereo', [[     nan,  0.1804 , -0.34765],
                                [     nan, -0.07236,  0.07893]])
    FrameAudio(0, 2, 'mono', [[     nan,  0.06998, -0.24758]])
    >>>
    """

    def __init__(self, filename: typing.Union[str, bytes, pathlib.Path], **av_kwargs):
        """Initialise and create the class.

        Parameters
        ----------
        filename : pathlike
            Path to the file to be decoded.
        **av_kwargs : dict
            Directly transmitted to ``av.open``.

            * ``"format" (str)``: Specific format to use. Defaults to autodect.
            * ``"options" (dict)``: Options to pass to the container and all streams.
            * ``"container_options" (dict)``: Options to pass to the container.
            * ``"stream_options" (list)``: Options to pass to each stream.
            * ``"metadata_encoding" (str)``: Encoding to use when reading or writing file metadata.
                Defaults to "utf-8".
            * ``"metadata_errors" (str)``: Specifies how to handle encoding errors;
                behaves like str.encode parameter. Defaults to "strict".
            * ``"buffer_size" (int)``: Size of buffer for Python input/output operations in bytes.
                Honored only when file is a file-like object. Defaults to 32768 (32k).
            * ``"timeout" (float or tuple)``: How many seconds to wait for data before giving up,
                as a float, or a (open timeout, read timeout) tuple.

        Raises
        ------
        cutcutcodec.core.exceptions.DecodeError
            If it fail to extract any multimedia stream from the provided file.
        """
        filename = pathlib.Path(filename).expanduser().resolve()
        assert filename.is_file(), filename

        self._filename = filename
        self._av_kwargs = av_kwargs  # need for compilation
        self._av_kwargs["options"] = self._av_kwargs.get("options", {})
        self._av_kwargs["container_options"] = self._av_kwargs.get("container_options", {})

        try:
            streams_type = get_streams_type(filename)
        except MissingStreamError as err:
            raise DecodeError(f"failed to read the file {filename} with pyav") from err
        out_streams = [self._init_out_stream(s_t) for s_t in streams_type]
        super().__init__(out_streams)

    def __enter__(self):
        """Make the object compatible with a context manager."""
        return self

    def __exit__(self, *_):
        """Exit the context manager, close the stream watever happends."""
        self.close()

    def _getstate(self) -> dict:
        return {
            "filename": str(self.filename),
            "av_kwargs": self.av_kwargs,
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename", "av_kwargs"}
        assert state.keys() == keys, set(state)-keys
        ContainerInputFFMPEG.__init__(self, state["filename"], **state["av_kwargs"])

    def _init_out_stream(self, stream_type: str) -> Stream:
        if (
            stream_class := (
                {"audio": _StreamAudioFFMPEG, "video": _StreamVideoFFMPEG}.get(stream_type, None)
            )
        ) is None:
            raise ValueError(f"only 'audio' and 'video' stream is supported, not {stream_type}")
        return stream_class(self)

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls(get_project_root() / "examples" / "intro.webm")

    def close(self):
        """Close the file."""
        for stream in self.out_streams:
            stream.reset()

    @property
    def av_kwargs(self) -> dict[str]:
        """Return the parameters passed to ``av.open``."""
        return self._av_kwargs

    @property
    def filename(self) -> pathlib.Path:
        """Return the path to the physical file that contains the extracted video stream."""
        return self._filename


class _StreamFFMPEGBase(Stream):
    """Factorise share methods between audio and video."""

    is_time_continuous = False

    def __init__(self, node: ContainerInputFFMPEG):
        assert isinstance(node, ContainerInputFFMPEG), node.__class__.__name__
        super().__init__(node)

        self._av_container = None
        self._duration = None
        self._frame_iter = None
        self._prec_frame = self._next_frame = None
        self._rate = None  # optimise about 100 ms par call

    def _seek_backward(self, position: Fraction) -> None:
        """Move backwards in the file.

        This method guarantees to move before the required position.
        If this is not possible, we move to the very beginning of the file.
        After, we always have ``self.get_current_range()[0] <= position``.
        """
        if self.type == "audio":
            dec = Fraction(self.av_container.streams[self.index].frame_size, self.rate)
        elif self.type == "video":
            dec = 1 / self.rate
        else:
            dec = 0
        for pos in (position, position-10, 0):
            stream = self.av_container.streams[self.index]  # must be define in 'for' because reset
            try:
                self.av_container.seek(
                    max(0, math.floor((pos - 2*dec) / stream.time_base)),
                    backward=True,  # if there is not a keyframe at the given offset
                    stream=stream
                )
            except av.error.PermissionError:  # happens sometimes
                self.reset()
                break
            self._prec_frame = self._next_frame = None  # takes into account the new position

            # verification and rough adjustment
            try:
                if self.get_current_range()[0] <= position:
                    break
            except OutOfTimeRange:  # if this exception is throw, reset is just done
                continue
        else:
            self.reset()

    def _seek_forward(self, position: Fraction) -> None:
        """Move forwardwards in the file.

        The displacement, if some cases, can be very approximate.
        """
        stream = self.av_container.streams[self.index]
        if stream.type == "audio":
            dec = Fraction(stream.frame_size, self.rate)
        elif stream.type == "video":
            dec = 1 / self.rate
        else:
            dec = 0
        self.av_container.seek(
            max(0, math.floor((position - dec) / stream.time_base)),
            backward=True,  # if there is not a keyframe at the given offset
            stream=stream
        )
        self._prec_frame = self._next_frame = None  # takes into account the new position

    @property
    def av_container(self) -> av.container.Container:
        """Allow to read the file at the last moment."""
        if self._av_container is None:
            self._av_container = av.open(str(self.node.filename), "r", **self.node.av_kwargs)
            self._av_container.streams[self.index].thread_type = "AUTO"  # mit improve speed
        return self._av_container

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def frame_iter(self) -> typing.Iterable[av.audio.frame.AudioFrame]:
        """Allow to read the file at the last moment."""
        if self._frame_iter is None:
            self._frame_iter = iter(self.av_container.decode(self.av_container.streams[self.index]))
        return self._frame_iter

    @property
    def next_frame(self) -> typing.Union[None, av.audio.frame.AudioFrame]:
        """Return the next frame if exists, None else."""
        if self._next_frame is None:
            self._prec_frame = self.prec_frame  # iter if needed ("=" is for pylint W0104)
            try:
                self._next_frame = next(self.frame_iter)
            except (StopIteration, av.error.EOFError):
                self._next_frame = self._frame_iter = None
                if self._duration is None:  # facultative, it is just optimisation
                    t_start, t_end = frame_dates(self._prec_frame)
                    self._duration = t_start + Fraction(1, self.rate) if t_end is None else t_end
        return self._next_frame

    @property
    def prec_frame(self) -> av.audio.frame.AudioFrame:
        """Return the frame at the current position."""
        if self._prec_frame is None:
            try:
                self._prec_frame = next(self.frame_iter)
            except (StopIteration, av.error.EOFError) as err:
                self.reset()
                raise OutOfTimeRange("there is no frame left to read") from err
        return self._prec_frame

    @property
    def rate(self) -> Fraction:
        """Return the theorical image or sample frequency in the metadata."""
        if self._rate is None:
            self._rate = _estimate_rate_ffmpeg(self.node.filename, self.index)
        return self._rate

    def reset(self) -> None:
        """Close the file and delete all internal state."""
        if self._av_container is not None:
            self._prec_frame = self._next_frame = None
            self._frame_iter = None
            self._av_container.close()
            self._av_container = None


class _StreamAudioFFMPEG(StreamAudio, _StreamFFMPEGBase):
    """Stream Audio from a file.

    Attributes
    ----------
    duration : Fraction
        The exact duration of the stream (readonly).
        This date corresponds to the end of the last sample.
    rate : int
        The frequency in Hz of the samples (readonly).

    Notes
    -----
    Should use ``ffmpegio.audio.read(file, sample_fmt='dbl')``.
    """

    def __init__(self, node: ContainerInputFFMPEG):
        super().__init__(node)
        self._duration = None
        self._lock = threading.Lock()

    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # resample if needeed
        if samples != 1 and rate != self.rate:
            frame = self._snapshot(
                timestamp,
                rate=self.rate,
                samples=math.floor(samples*Fraction(self.rate, rate))
            )
            indexs = torch.arange(samples, dtype=torch.int64)
            indexs *= self.rate
            indexs //= rate
            frame = FrameAudio(timestamp, rate, frame.layout, frame[:, indexs])
            return frame

        # decode concerned frames
        frames_and_dates: list[list[np.ndarray, Fraction, Fraction]] = []  # frame, start_t, end_t
        end = timestamp + Fraction(samples, rate)  # apparition of last sample
        with self._lock:
            self.seek(timestamp)
            while True:
                try:
                    frame = self.prec_frame
                except OutOfTimeRange as err:
                    raise OutOfTimeRange(
                        f"stream start {self.beginning} and end {self.beginning + self.duration}, "
                        f"no stream at timestamp {timestamp} to {timestamp} + {samples}/{rate}"
                    ) from err
                if frame.is_corrupt:
                    logging.warning("the frame at %f seconds is corrupted", frame.time)
                    continue
                dates = frame_dates(frame)
                frames_and_dates.append(
                    [  # the reshape is usefull only in some cases for debug in ffmpeg 4
                        frame.to_ndarray().reshape(-1, frame.samples, order="F"),
                        dates[0]-timestamp,
                        dates[1]-timestamp,
                    ]
                )
                if end <= dates[1]:
                    break
                self._prec_frame, self._next_frame = self.next_frame, None  # iter in stream

        # correct the drift
        drift_max = self.av_container.streams[self.index].time_base
        drift_max = 2 if drift_max is None else math.ceil(drift_max*rate)
        frames_and_dates = _fix_drift_fill_crop(frames_and_dates, drift_max, rate, samples)

        # create the final frame
        return FrameAudio(
            timestamp,
            rate,
            self.layout,
            _convert_audio_samples(
                np.concatenate([f for f, _, _ in frames_and_dates], axis=1)
                if len(frames_and_dates) > 1 else frames_and_dates.pop()[0]
            ),
        )

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        """Return the exact duration in seconds.

        Examples
        --------
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/audio_5.1_narration.oga") as container:
        ...     (stream,) = container.out_streams
        ...     stream.duration
        ...
        Fraction(8, 1)
        >>>
        """
        if self._duration is not None:
            return self._duration
        # seek approximative
        rel_index = len(
            [
                None for i, s in enumerate(self.node.out_streams)
                if i < self.index and s.type == "audio"
            ]
        )
        with self._lock:
            self.seek(get_duration_audio(self.node.filename, rel_index, accurate=False) - 10)
            # decoding until reaching the last frame
            while self.next_frame is not None:
                self._prec_frame, self._next_frame = self.next_frame, None  # iter in stream
            # get the time of the last frame + the frame duration
            self._duration = frame_dates(self._prec_frame)[1]
        return self._duration

    def get_current_range(self) -> tuple[Fraction, Fraction]:
        """Return the time interval cover by the current frame."""
        if (next_frame := self.next_frame) is None:
            return frame_dates(self.prec_frame)
        return frame_dates(self.prec_frame)[0], frame_dates(next_frame)[0]

    @property
    def layout(self) -> Layout:
        """Return the signification of each channels in this audio stream.

        Examples
        --------
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/audio_5.1_narration.oga") as container:
        ...     (stream,) = container.out_streams
        ...     stream.layout
        ...
        Layout('5.1')
        >>>
        """
        return Layout(self.av_container.streams[self.index].layout.name)

    @property
    def rate(self) -> int:
        """Return the theorical image or sample frequency in the metadata."""
        return int(super().rate)

    def seek(self, position: Fraction) -> None:
        """Move into the file until reaching the frame at this position.

        If you are already well placed, this has no effect.
        Allows backward even a little bit, but only jump forward if the jump is big enough.

        Parameters
        ----------
        position : fraction.Fraction
            The target position such as ``self.prec_frame.time <= position < self.next_frame.time``.
            This position is expressed in seconds.

        Raises
        ------
        OutOfTimeRange
            If the required position is out of the definition range.

        Examples
        --------
        >>> from fractions import Fraction
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/audio_5.1_narration.oga") as container:
        ...     (stream,) = container.out_streams
        ...     stream.seek(Fraction(7))
        ...     stream.get_current_range()
        ...     stream.seek(Fraction(5))
        ...     stream.get_current_range()
        ...
        (Fraction(872, 125), Fraction(876, 125))
        (Fraction(624, 125), Fraction(628, 125))
        >>>
        """
        assert isinstance(position, Fraction), position.__class__.__name__

        # case need to seek
        if position > self.get_current_range()[1] + 10:  # forward if jump more 10 seconds
            self._seek_forward(position)  # very approximative
        if position < self.get_current_range()[0]:
            self._seek_backward(position)  # guaranteed to be before

        # fine adjustment
        while self.get_current_range()[1] <= position:
            self._prec_frame, self._next_frame = self.next_frame, None  # iter in stream


class _StreamVideoFFMPEG(StreamVideo, _StreamFFMPEGBase):
    """Stream Video from a file.

    Attributes
    ----------
    height : int
        The dimension i (vertical) of the encoded frames in pxl (readonly).
    duration : Fraction
        The exact duration of the complete stream (readonly).
        the time include the duration of the last frame.
    width : int
        The dimension j (horizontal) of the encoded frames in pxl (readonly).
    """

    is_space_continuous = False

    def __init__(self, node: ContainerInputFFMPEG):
        super().__init__(node)
        self._duration = None
        self._key_times = None
        self._lock = threading.Lock()

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # resize and keep proportion
        dw_sh, dh_sw = mask.shape[1] * self.height, mask.shape[0] * self.width
        if dw_sh == dh_sw:  # if the proportion is the same
            height, width = mask.shape
        elif dw_sh > dh_sw:  # need horizontal padding
            height, width = (mask.shape[0], round(dh_sw/self.height))  # keep height unchanged
        else:
            height, width = (round(dw_sh/self.width), mask.shape[1])  # keep width unchanged

        # decode the frame and convert into numpy array
        with self._lock:
            self.seek(timestamp)  # adjust position
            frame_av = self.prec_frame
            frame_np = frame_av.to_ndarray(
                width=width,  # reshape is alltimes required for non-squared pixels
                height=height,  # av is able to squeeze reshape if the shape is the same
                format="bgr24",
                dst_colorspace=av.video.reformatter.Colorspace.DEFAULT,
                interpolation=(
                    av.video.reformatter.Interpolation.AREA if (  # for shirking
                        height < self.av_container.streams[self.index].coded_height
                        or width < self.av_container.streams[self.index].coded_width
                    ) else av.video.reformatter.Interpolation.BICUBIC  # for enlarge
                ),
            )

        # final thread-safe operations
        frame_np = pad_keep_ratio(frame_np, mask.shape, copy=False)
        return FrameVideo(frame_dates(frame_av)[0], frame_np)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        """Return the exact duration in seconds.

        Examples
        --------
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/video.mp4") as container:
        ...     (stream,) = container.out_streams
        ...     stream.duration
        ...
        Fraction(16, 1)
        >>>
        """
        if self._duration is not None:
            return self._duration
        with self._lock:
            # jump if need
            key_times = self.get_key_times()
            key_time = key_times[-2] if len(key_times) >= 2 else Fraction(0)

            # print("avant seek", self.get_current_range())
            self.seek(key_time)  # sometimes self.reset() corrects the bug
            # decoding until reaching the last frame
            while self.next_frame is not None:
                self._prec_frame, self._next_frame = self.next_frame, None  # iter in stream
            # get the time of the last frame + the frame duration
            self._duration = frame_dates(self._prec_frame)[0] + 1/self.rate
        return self._duration

    def get_key_times(self) -> np.ndarray[Fraction]:
        """Allow to read the file at the last moment.

        Examples
        --------
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/video.mp4") as container:
        ...     (stream,) = container.out_streams
        ...     stream.get_key_times()
        ...
        array([Fraction(0, 1), Fraction(10, 1)], dtype=object)
        >>>
        """
        if self._key_times is None:
            try:
                self._key_times = np.fromiter(
                    (
                        frame_dates(frame)[0] for frame in _extract_key_frames(
                            self.av_container.streams[self.index]
                        )
                    ),
                    dtype=object,
                )
            except MissingInformation as err:
                raise MissingInformation("the timestamp is not known for all keyframes") from err
            if len(self._key_times) == 0:
                raise MissingStreamError(
                    f"can not decode any frames of {self.node.filename} stream {self.index}"
                )
        return self._key_times

    def get_current_range(self) -> tuple[Fraction, Fraction]:
        """Return the time interval cover by the current frame."""
        start_time = frame_dates(self.prec_frame)[0]
        if (next_frame := self.next_frame) is None:
            return start_time, start_time + 1/self.rate
        return start_time, frame_dates(next_frame)[0]

    @property
    def height(self) -> int:
        """Return the vertical size of the native frame in pxl."""
        if (ratio := Fraction(self.av_container.streams[self.index].sample_aspect_ratio or 1)) < 1:
            return int(self.av_container.streams[self.index].height / ratio)
        return self.av_container.streams[self.index].height

    def seek(self, position: Fraction) -> None:
        """Move into the file until reaching the frame at this accurate position.

        If you are already well placed, this has no effect.
        Allows backward even a little bit, but only jump forward if the jump is big enough.

        Parameters
        ----------
        position : fraction.Fraction
            The target position such as ``self.prec_frame.time <= position < self.next_frame.time``.
            This position is expressed in seconds.

        Raises
        ------
        OutOfTimeRange
            If the required position is out of the definition range.

        Examples
        --------
        >>> from fractions import Fraction
        >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("cutcutcodec/examples/video.mp4") as container:
        ...     (stream,) = container.out_streams
        ...     stream.seek(Fraction(15))
        ...     stream.get_current_range()
        ...     stream.seek(Fraction(5))
        ...     stream.get_current_range()
        ...
        (Fraction(15, 1), Fraction(376, 25))
        (Fraction(5, 1), Fraction(126, 25))
        >>>
        """
        assert isinstance(position, Fraction), position.__class__.__name__

        # case need to seek
        if position > self.get_current_range()[1] + 100/self.rate:  # if jump more than 100 frames
            self._seek_forward(position)  # very approximative
        if position < self.get_current_range()[0]:
            self._seek_backward(position)  # guaranteed to be before

        # fine adjustment
        while position >= self.get_current_range()[1]:
            self._prec_frame, self._next_frame = self.next_frame, None  # iter in stream

        # # check asked seek position is not bigger than the duration
        # if position > self.get_current_range()[0]:
        #     raise OutOfTimeRange(
        #         f"stream start {self.beginning} and end {self.beginning + self.duration}, "
        #         f"no frame at timestamp {position}"
        #     )

    @property
    def width(self) -> int:
        """Return the horizontal size of the native frame in pxl."""
        if (ratio := Fraction(self.av_container.streams[self.index].sample_aspect_ratio or 1)) > 1:
            return int(self.av_container.streams[self.index].width * ratio)
        return self.av_container.streams[self.index].width


def _convert_audio_samples(audio_samples: np.ndarray[numbers.Real]) -> torch.Tensor:
    """Convert sound samples into float between -1 and 1.

    Minimizes copying and reallocations.
    The values are not clamped.

    Examples
    --------
    >>> import numpy as np
    >>> from cutcutcodec.core.io.read_ffmpeg import _convert_audio_samples
    >>> _convert_audio_samples(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float64))
    tensor([-1.5000, -1.0000, -0.5000,  0.5000,  1.0000,  1.5000],
           dtype=torch.float64)
    >>> _convert_audio_samples(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float32))
    tensor([-1.5000, -1.0000, -0.5000,  0.5000,  1.0000,  1.5000])
    >>> _convert_audio_samples(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float16))
    tensor([-1.5000, -1.0000, -0.5000,  0.5000,  1.0000,  1.5000],
           dtype=torch.float16)
    >>> _convert_audio_samples(
    ...     np.array([-2147483648, -1073741824, 1073741824, 2147483647], dtype=np.int32)
    ... )
    tensor([-1.0000, -0.5000,  0.5000,  1.0000], dtype=torch.float64)
    >>> _convert_audio_samples(np.array([-32768, -16384, 16384, 32767], dtype=np.int16))
    tensor([-1.0000, -0.5000,  0.5000,  1.0000], dtype=torch.float64)
    >>> _convert_audio_samples(np.array([0, 64, 192, 255], dtype=np.uint8))
    tensor([-1.0000, -0.4980,  0.5059,  1.0000], dtype=torch.float64)
    >>>
    """
    assert isinstance(audio_samples, np.ndarray), audio_samples.__class__.__name__
    audio_samples = torch.from_numpy(audio_samples)
    if not audio_samples.dtype.is_floating_point:
        iinfo = torch.iinfo(audio_samples.dtype)
        audio_samples = audio_samples.to(torch.float64)
        audio_samples -= .5*float(iinfo.min + iinfo.max)
        audio_samples /= .5*float(iinfo.max - iinfo.min)
    return audio_samples


def _extract_key_frames(av_stream: av.video.stream.VideoStream):
    """Extract the list of key frames.

    Examples
    --------
    >>> import av
    >>> from cutcutcodec.core.io.read_ffmpeg import _extract_key_frames
    >>> with av.open("cutcutcodec/examples/video.mp4") as av_container:
    ...     key_frames = list(_extract_key_frames(av_container.streams.video[0]))
    ...
    >>> [f.time for f in key_frames]
    [0.0, 10.0]
    >>>
    """
    assert isinstance(av_stream, av.video.stream.VideoStream), av_stream.__class__.__name__
    av_stream.container.seek(0, backward=True, any_frame=False, stream=av_stream)
    av_stream.codec_context.skip_frame = "NONKEY"
    yield from av_stream.container.decode(av_stream)
    av_stream.container.seek(0, backward=True, any_frame=False, stream=av_stream)
    av_stream.codec_context.skip_frame = "DEFAULT"


def _fix_drift_fill_crop(
    frames_and_dates: list[list[np.ndarray, Fraction, Fraction]],
    drift_max: int,
    rate: int,
    samples: int,
) -> list[list[np.ndarray, Fraction, Fraction]]:
    """Slightly shift the audio frames, fill the gap and crop the end.

    After this function, it is possible to concatenate the frames.
    The gap are filled with the 'nan' value.

    Parameters
    ----------
    frames_and_dates : list[list[np.ndarray, Fraction, Fraction]]
        The frame data as a numpy array of shape (channels, samples).
        The frames are considered to be all of the same dtype and same
        number of channels.
        The relative date of start and end of each frames.
        The first date of the first sample has to be close to 0.
        All the frames are assumed to be in a monotonic order.
    drift_max : int
        The maximum authorized translation (number of samples).
    rate : int
        The samplerate.
    samples : int
        The final index. In the case where there is a hole at the beginning or at the very end,
        this makes it possible to translate the entirety of the frames by a maximum value of
        `drift_max`/2 in order to fill the hole.
        The last frame can be cropped to reach the exact number of requiered samples.
        The gaps can be filled to reach the exact number of requiered samples.

    Returns
    -------
    new_frames_and_dates
        Same as input but with somme correction and contiguous frames.

    Examples
    --------
    >>> from fractions import Fraction
    >>> from pprint import pprint
    >>> import numpy as np
    >>> from cutcutcodec.core.io.read_ffmpeg import _fix_drift_fill_crop
    >>> frames_and_dates = [
    ...     [np.zeros((2, 10)), Fraction(1), Fraction(6)],  # start after 0 -> padding
    ...     [np.ones((2, 10)), Fraction(5), Fraction(10)],  # light overlap -> shift
    ...     [np.zeros((2, 10)), Fraction(15), Fraction(20)],  # big gap -> padding
    ...     [np.ones((2, 10)), Fraction(21), Fraction(26)],  # light gap -> shift
    ...     [np.zeros((2, 10)), Fraction(23), Fraction(28)],  # big overlap -> crop
    ... ]
    >>> pprint(_fix_drift_fill_crop(frames_and_dates, drift_max=2, rate=2, samples=60))
    [(array([[nan, nan],
           [nan, nan]]), Fraction(0, 1), Fraction(1, 1)),
     [array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]),
      Fraction(1, 1),
      Fraction(6, 1)],
     [array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
           [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]]),
      Fraction(6, 1),
      Fraction(11, 1)],
     (array([[nan, nan, nan, nan, nan, nan, nan, nan],
           [nan, nan, nan, nan, nan, nan, nan, nan]]),
      Fraction(11, 1),
      Fraction(15, 1)),
     [array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]),
      Fraction(15, 1),
      Fraction(20, 1)],
     [array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
           [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]]),
      Fraction(20, 1),
      Fraction(25, 1)],
     [array([[0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0.]]),
      Fraction(25, 1),
      Fraction(28, 1)],
     (array([[nan, nan, nan, nan],
           [nan, nan, nan, nan]]),
      Fraction(28, 1),
      Fraction(30, 1))]
    >>>
    """
    dtype = frames_and_dates[0][0].dtype.type
    nbr_channels = frames_and_dates[0][0].shape[0]

    # drift each slices for perfect concatenation
    for index in range(1, len(frames_and_dates)):
        drift = frames_and_dates[index][1] - frames_and_dates[index-1][2]
        if rate * abs(drift) <= drift_max:
            frames_and_dates[index][1] -= drift
            frames_and_dates[index][2] -= drift

    # fill the gaps or crop the overlaps
    frames_and_dates.insert(0, [None, None, Fraction(0)])  # fake reference frame
    new_frames_and_dates = []
    for index in range(1, len(frames_and_dates)):
        drift = frames_and_dates[index][1] - frames_and_dates[index-1][2]
        if drift > 0:  # case padding
            logging.warning("audio frame drift of %f seconds detected", float(drift))
            nbr_samples = round(drift * rate)
            new_frames_and_dates.append((
                np.full((nbr_channels, nbr_samples), np.nan, dtype=dtype),
                frames_and_dates[index][1] - Fraction(nbr_samples, rate),
                frames_and_dates[index][1],
            ))
        elif drift < 0:  # case overlap
            logging.warning("audio frame overlap of %f seconds detected", float(-drift))
            nbr_samples = round(-drift * rate)
            frames_and_dates[index][0] = frames_and_dates[index][0][:, nbr_samples:]
            frames_and_dates[index][1] += Fraction(nbr_samples, rate)
        new_frames_and_dates.append(frames_and_dates[index])
    frames_and_dates = new_frames_and_dates

    # reach the exact number of samples
    nbr_missing_samples = samples - sum(f.shape[1] for f, _, _ in frames_and_dates)
    if nbr_missing_samples > 0:  # case padding at the last end
        frames_and_dates.append((
            np.full((nbr_channels, nbr_missing_samples), np.nan, dtype=dtype),
            frames_and_dates[-1][2],
            frames_and_dates[-1][2] + Fraction(nbr_missing_samples, rate),
        ))
    elif nbr_missing_samples < 0:  # case croping at the last end
        nbr_samples = frames_and_dates[-1][0].shape[1] + nbr_missing_samples
        frames_and_dates[-1][0] = frames_and_dates[-1][0][:, :nbr_samples]
        frames_and_dates[-1][2] += Fraction(nbr_missing_samples, rate)

    return frames_and_dates


def frame_dates(frame: av.frame.Frame) -> tuple[Fraction, typing.Union[None, Fraction]]:
    """Return the accurate time interval of the given frame.

    Parameters
    ----------
    frame : av.frame.Frame
        The audio or video frame witch we extract the timing information.

    Returns
    -------
    t_start : Fraction
        The display time of the frame. for audio frame, it corressponds to
        the time of the first sample.
    t_end : Fraction or None
        For audio frame only, the time to switch off the last sample. Return None for video frame.

    Examples
    --------
    >>> import av
    >>> from cutcutcodec.core.io.read_ffmpeg import frame_dates
    >>> with av.open("cutcutcodec/examples/video.mp4") as av_container:
    ...     frame_dates(next(av_container.decode(av_container.streams.video[0])))
    ...     frame_dates(next(av_container.decode(av_container.streams.video[0])))
    ...
    (Fraction(0, 1), None)
    (Fraction(1, 25), None)
    >>> with av.open("cutcutcodec/examples/audio_5.1_narration.oga") as av_container:
    ...     frame_dates(next(av_container.decode(av_container.streams.audio[0])))
    ...     frame_dates(next(av_container.decode(av_container.streams.audio[0])))
    ...
    (Fraction(0, 1), Fraction(4, 125))
    (Fraction(4, 125), Fraction(8, 125))
    >>>

    Notes
    -----
    For audio frame, include the duration of the last sample.
    For video frame, the duration of the frame is unknown.
    """
    assert isinstance(frame, av.frame.Frame), frame.__class__.__name__

    if (time_base := frame.time_base) is None:
        start_time = Fraction(frame.time)
    elif (pts := frame.pts) is not None:
        start_time = pts * time_base
    elif (dts := frame.dts) is not None:
        start_time = dts * time_base
    else:
        raise MissingInformation(f"unable to catch the time of the frame {frame}")
    if isinstance(frame, av.audio.frame.AudioFrame):
        stop_time = start_time + Fraction(frame.samples, frame.rate)
        return start_time, stop_time
    return start_time, None
