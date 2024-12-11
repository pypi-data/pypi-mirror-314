#!/usr/bin/env python3

"""Generate a video noise signal."""

from fractions import Fraction
import hashlib
import math
import numbers
import struct
import typing

import numpy as np
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import OutOfTimeRange
from cutcutcodec.core.interfaces.seedable import Seedable


class GeneratorVideoNoise(ContainerInput, Seedable):
    """Generate a pure noise video signal.

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> stream = GeneratorVideoNoise(0).out_streams[0]
    >>> stream.snapshot(0, (13, 9))[..., 0]
    tensor([[127,  38, 184, 235, 108, 176, 146, 203,  68],
            [217, 228,  36,  60, 186,  75, 202, 203, 185],
            [228, 143,  82, 179, 157, 172, 151, 115, 208],
            [221, 219, 169, 189, 199, 214, 134,  31,  23],
            [177, 214,  12,  12,  86, 199,  62, 111, 143],
            [168,  24, 114, 190, 101,  49,  46,  13,  11],
            [217, 230, 254,  40, 216, 192, 196,  67, 127],
            [157, 214,  66,  65,  72, 153,  65, 129, 147],
            [ 24,  92, 187, 202, 171, 182,  40,  63, 240],
            [245, 219, 159, 178,  73,  59, 230, 141, 139],
            [197, 101, 129, 185,  46,  35,  80,   4, 156],
            [156, 145,  73,  60, 130, 234,  92, 195,  18],
            [ 25,  21, 156, 202, 142, 104, 225,  45,  57]], dtype=torch.uint8)
    >>>
    """

    def __init__(self, seed: typing.Optional[numbers.Real] = None):
        """Initialise and create the class.

        Parameters
        ----------
        seed : numbers.Real, optional
            Transmitted to ``cutcutcodec.core.interfaces.seedable.Seedable``.
        """
        Seedable.__init__(self, seed)
        super().__init__([_StreamVideoNoiseUniform(self)])

    def _getstate(self) -> dict:
        return self._getstate_seed()

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state.keys() == {"seed"}, set(state)
        self._setstate_seed(state)
        ContainerInput.__init__(self, [_StreamVideoNoiseUniform(self)])

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls(0)


class _StreamVideoNoiseUniform(StreamVideo):
    """Random video stream where each pixel follows a uniform law."""

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoNoise):
        assert isinstance(node, GeneratorVideoNoise), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")
        seed = int.from_bytes(
            hashlib.md5(
                struct.pack(
                    "dLL",
                    self.node.seed,
                    timestamp.numerator % (1 << 64),
                    timestamp.denominator % (1 << 64),
                )
            ).digest(),
            byteorder="big",
        ) % (1 << 64)  # solve RuntimeError: Overflow when unpacking long
        return torch.from_numpy(
            np.random.Generator(np.random.SFC64(seed=seed))  # np.random.default_rng(seed=seed)
            .random((*mask.shape, 3), dtype=np.float32)
        )
        # numpy 1.24.1 vs torch 2.0.0 is 11 times faster
        # this version is faster:
        # return torch.from_numpy(
        #     np.random.Generator(np.random.SFC64(seed=seed))  # np.random.default_rng(seed=seed)
        #     .integers(0, 256, (*mask.shape, 3), dtype=np.uint8)
        # )

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        return math.inf
