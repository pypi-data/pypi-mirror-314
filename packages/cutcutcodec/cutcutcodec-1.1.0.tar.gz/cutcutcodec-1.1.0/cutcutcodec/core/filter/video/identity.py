#!/usr/bin/env python3

"""A video filter that doing nothing."""

import typing

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.stream import Stream


class FilterVideoIdentity(Filter):
    """Allow to convert a set of streams into a filter.

    Examples
    --------
    >>> from cutcutcodec.core.filter.video.identity import FilterVideoIdentity
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>>
    >>> (s_base_video,) = GeneratorVideoNoise(0).out_streams
    >>> identity = FilterVideoIdentity([s_base_video])
    >>>
    >>> s_base_video is identity.out_streams[0]
    True
    >>>
    """

    def __init__(self, in_streams: typing.Iterable[Stream]):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            All the streams to keep intact.
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        """
        super().__init__(in_streams, in_streams)

    def _getstate(self) -> dict:
        return {}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state == {}
        FilterVideoIdentity.__init__(self, in_streams)

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls([])
