#!/usr/bin/env python3

"""Allow to generate colors from mathematical functions."""

import numbers
import re
import typing

from sympy.core.basic import Basic

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.filter.video.equation import FilterVideoEquation


class GeneratorVideoEquation(FilterVideoEquation, ContainerInput):
    """Generate a video stream whose channels are defened by any equations.

    It is a particular case of ``cutcutcodec.core.filter.equation.FilterVideoEquation``.

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.equation import GeneratorVideoEquation
    >>> (stream,) = GeneratorVideoEquation(
    ...     "atan(pi*j)/pi + 1/2",  # dark blue on the left and bright on the right
    ...     "sin(2pi(i-t))**2",  # horizontal descending green waves
    ...     "exp(-(i**2+j**2)/(2*(1e-3+.1*t)))",  # red spot in the center that grows
    ... ).out_streams
    >>> stream.node.colors
    [atan(pi*j)/pi + 1/2, sin(2*pi*(i - t))**2, exp((-i**2 - j**2)/((2*(0.1*t + 0.001))))]
    >>> stream.snapshot(0, (13, 9))[..., 0]  # blue at t=0
    tensor([[ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230]], dtype=torch.uint8)
    >>> stream.snapshot(0, (13, 9))[..., 1]  # green at t=0
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> stream.snapshot(0, (13, 9))[..., 2]  # red at t=0
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0, 255,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> stream.snapshot(1, (13, 9))[..., 2]  # red at t=1
    tensor([[  0,   0,   1,   1,   2,   1,   1,   0,   0],
            [  0,   1,   2,   6,   8,   6,   2,   1,   0],
            [  0,   2,   8,  21,  28,  21,   8,   2,   0],
            [  1,   5,  21,  54,  74,  54,  21,   5,   1],
            [  1,   9,  43, 108, 147, 108,  43,   9,   1],
            [  2,  14,  64, 163, 222, 163,  64,  14,   2],
            [  2,  16,  74, 187, 255, 187,  74,  16,   2],
            [  2,  14,  64, 163, 222, 163,  64,  14,   2],
            [  1,   9,  43, 108, 147, 108,  43,   9,   1],
            [  1,   5,  21,  54,  74,  54,  21,   5,   1],
            [  0,   2,   8,  21,  28,  21,   8,   2,   0],
            [  0,   1,   2,   6,   8,   6,   2,   1,   0],
            [  0,   0,   1,   1,   2,   1,   1,   0,   0]], dtype=torch.uint8)
    >>>
    """

    def __init__(self, *colors: typing.Union[Basic, numbers.Real, str]):
        """Initialise and create the class.

        Parameters
        ----------
        *colors : str or sympy.Basic
            Transmitted to the
            ``cutcutcodec.core.filter.video.equation.FilterVideoEquation`` initialisator.
            But the only available vars are `t`, `i` and `j`.
        """
        FilterVideoEquation.__init__(self, [], *colors)
        ContainerInput.__init__(self, self.out_streams)
        if excess := (
            {s for s in self._free_symbs if re.fullmatch(r"i|j|t", str(s)) is None}
        ):
            raise ValueError(f"only i, j, and t symbols are allowed, not {excess}")

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls(0)
