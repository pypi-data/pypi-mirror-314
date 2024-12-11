#!/usr/bin/env python3

"""Selects a time slice of an audio stream."""

from fractions import Fraction
import math
import numbers
import typing

from cutcutcodec.core.classes.meta_filter import MetaFilter
from cutcutcodec.core.classes.node import Node
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.compilation.parse import parse_to_number
from cutcutcodec.core.filter.audio.cut import FilterAudioCut
from cutcutcodec.core.filter.audio.identity import FilterAudioIdentity
from cutcutcodec.core.filter.subclip import FilterSubclip


class FilterAudioSubclip(FilterSubclip, MetaFilter):
    """Extract a segment from an audio stream.

    It is a particular case of ``cutcutcodec.core.filter.audio.cut.FilterAudioCut``.
    Allows to start a flow after the beginning and or finish it before the end.

    Examples
    --------
    >>> from cutcutcodec.core.filter.audio.subclip import FilterAudioSubclip
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>>
    >>> (s_a,) = GeneratorAudioNoise(0).out_streams
    >>> (s_b,) = GeneratorAudioNoise(0).out_streams
    >>> s_subclip_a, s_subclip_b = FilterAudioSubclip([s_a, s_b], 10, 20).out_streams
    >>>
    >>> s_subclip_a.beginning
    Fraction(10, 1)
    >>> s_subclip_a.duration
    Fraction(20, 1)
    >>> s_subclip_b.beginning
    Fraction(10, 1)
    >>> s_subclip_b.duration
    Fraction(20, 1)
    >>>
    """

    def __init__(
        self,
        in_streams: typing.Iterable[Stream],
        delay: numbers.Real = Fraction(0),
        duration_max: numbers.Real = math.inf,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        delay: numbers.Real, default=0
            Transmitted to ``cutcutcodec.core.filter.subclip.FilterSubClip``.
        duration_max : numbers.Real, default=inf
            Transmitted to ``cutcutcodec.core.filter.subclip.FilterSubClip``.
        """
        FilterSubclip.__init__(self, delay, duration_max)
        MetaFilter.__init__(self, in_streams)

    def _compile(self, in_streams: tuple[Stream]) -> Node:
        if self.delay:
            if math.isfinite(self.duration_max):
                sub_streams = FilterAudioCut(
                    in_streams, self.delay, self.delay+self.duration_max
                ).out_streams[len(in_streams):2*len(in_streams)]
            else:
                sub_streams = FilterAudioCut(in_streams, self.delay).out_streams[len(in_streams):]
        else:
            if math.isfinite(self.duration_max):
                sub_streams = FilterAudioCut(
                    in_streams, self.delay+self.duration_max
                ).out_streams[:len(in_streams)]
            else:
                sub_streams = in_streams
        return FilterAudioIdentity(sub_streams)

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state.keys() == {"delay", "duration_max"}, set(state)
        FilterAudioSubclip.__init__(
            self, in_streams, Fraction(state["delay"]), parse_to_number(state["duration_max"])
        )

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls([], 0, math.inf)
