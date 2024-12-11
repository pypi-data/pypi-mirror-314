#!/usr/bin/env python3

"""Defines the structure of an abstract audio stream."""

from fractions import Fraction
import abc
import numbers
import typing

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.layout import Layout
from cutcutcodec.core.classes.stream import Stream, StreamWrapper


class StreamAudio(Stream):
    """Representation of any audio stream.

    Attributes
    ----------
    layout : cutcutcodec.core.classes.layout.Layout
        The signification of each channels (readonly).
        The number of channels is ``len(self.layout.channels)``.
    """

    @abc.abstractmethod
    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def layout(self) -> Layout:
        """Return the signification of each channels."""
        raise NotImplementedError

    def snapshot(
        self,
        timestamp: numbers.Real,
        rate: typing.Optional[numbers.Integral] = None,
        samples: numbers.Integral = 1,
    ) -> FrameAudio:
        """Extract the closest values to the requested date.

        Parameters
        ----------
        timestamp : numbers.Real
            The absolute time expressed in seconds, not relative to the beginning of the audio.
            Is the instant of the first sample of the returned frame.
            For avoid the inacuracies of round, it is recomended to use fractional number.
        rate : numbers.Integral, optional
            If samples == 1, this argument is ignored. Otherwise is the samplerate of the frame.
            If provide and samples != 1, allows to deduce the timestamps of the non 0 samples.
            If non provide and samples != 1, try to call the `rate` attribute of the stream.
        samples : numbers.Integral, default=1
            The number of audio samples per channels to catch.

        Returns
        -------
        samples : FrameAudio
            Audio samples corresponding to the times provided.
            This vector is of shape (nbr_channels, *timestamp_shape).
            The values are between -1 and 1.

        Raises
        ------
        cutcutcodec.core.exception.OutOfTimeRange
            If we try to get a frame out of the definition range.
            The valid range is [self.beginning, self.beginning+self.duration].
            The range taken is [timestamp, timestamp + samples/rate[.
        AttributeError
            If the `rate` attribute has to be defined but is not provides or deductable.
        """
        # verifications on input
        assert isinstance(samples, numbers.Integral), samples.__class__.__name__
        samples = int(samples)
        assert samples > 0, samples
        if rate is None:
            if samples != 1:
                if (rate := getattr(self, "rate", None)) is None:
                    raise ValueError("rate attribute has to be provide")
            else:
                rate = 1  # ignore default unused stupid value
        assert isinstance(rate, numbers.Integral), rate.__class__.__name__
        rate = int(rate)
        assert rate > 0, rate
        assert isinstance(timestamp, numbers.Real), timestamp.__class__.__name__
        timestamp = Fraction(timestamp)

        # extract samples
        frame = self._snapshot(timestamp, rate, samples)

        # result verification
        assert isinstance(frame, FrameAudio), frame.__class__.__name__
        return frame

    @property
    def type(self) -> str:
        """Implement ``cutcutcodec.core.classes.stream.Stream.type``."""
        return "audio"


class StreamAudioWrapper(StreamWrapper, StreamAudio):
    """Allow to dynamically transfer the methods of an instanced audio stream.

    This can be very useful for implementing filters.
    """

    def __init__(self, node: Filter, index: numbers.Integral):
        """Initialise and create the class.

        Parameters
        ----------
        node : cutcutcodec.core.classes.filter.Filter
            The parent node, transmitted to ``cutcutcodec.core.classes.stream.Stream``.
        index : number.Integral
            The index of the audio stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        assert isinstance(node, Filter), node.__class__.__name__
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        assert isinstance(node.in_streams[index], StreamAudio), "the stream must be audio type"
        super().__init__(node, index)

    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        return self.stream._snapshot(timestamp, rate, samples)  # pylint: disable=W0212

    @property
    def layout(self) -> Layout:
        """Return the signification of each channels."""
        return self.stream.layout
