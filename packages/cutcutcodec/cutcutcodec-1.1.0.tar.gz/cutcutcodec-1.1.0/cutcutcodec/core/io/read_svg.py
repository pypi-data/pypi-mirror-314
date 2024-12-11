#!/usr/bin/env python3

"""Decode the svg vectorial images based on `cairosvg` lib."""

from fractions import Fraction
import math
import pathlib
import typing
import xml

import cairosvg
import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import DecodeError
from cutcutcodec.core.exceptions import OutOfTimeRange


class ContainerInputSVG(ContainerInput):
    """Decode an svg image to a matricial image of any dimension.

    Attributes
    ----------
    filename : pathlib.Path
        The path to the physical file that contains the svg data (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.io.read_svg import ContainerInputSVG
    >>> (stream,) = ContainerInputSVG.default().out_streams
    >>> stream.snapshot(0, (12, 12))[..., 3]
    tensor([[  0,   0,   7, 110, 200, 244, 244, 200, 109,   7,   0,   0],
            [  0,  27, 208, 255, 255, 255, 255, 255, 255, 207,  27,   0],
            [  7, 208, 255, 255, 255, 255, 255, 255, 255, 255, 207,   7],
            [110, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 108],
            [201, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 199],
            [243, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 243],
            [243, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 241],
            [201, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 199],
            [109, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 108],
            [  7, 207, 255, 255, 255, 255, 255, 255, 255, 255, 207,   6],
            [  0,  27, 207, 255, 255, 255, 255, 255, 255, 207,  27,   0],
            [  0,   0,   6, 108, 199, 243, 243, 198, 108,   6,   0,   0]],
           dtype=torch.uint8)
    >>>
    """

    def __init__(self, filename: typing.Union[str, bytes, pathlib.Path], *, unsafe=False):
        """Initialise and create the class.

        Parameters
        ----------
        filename : pathlike
            Path to the file to be decoded.
        unsafe : bool
            Transmitted to ``cairosvg.svg2png``.

        Raises
        ------
        cutcutcodec.core.exceptions.DecodeError
            If it fail to extract any multimedia stream from the provided file.
        """
        filename = pathlib.Path(filename).expanduser().resolve()
        assert filename.is_file(), filename
        assert isinstance(unsafe, bool), unsafe.__class__.__name__
        self._filename = filename
        self.unsafe = unsafe
        super().__init__([_StreamVideoSVG(self)])

    def __enter__(self):
        """Make the object compatible with a context manager."""
        return self

    def __exit__(self, *_):
        """Exit the context manager."""

    def _getstate(self) -> dict:
        return {
            "filename": str(self.filename),
            "unsafe": self.unsafe,
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename", "unsafe"}
        assert state.keys() == keys, set(state)-keys
        ContainerInputSVG.__init__(self, state["filename"], unsafe=state["unsafe"])

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls("cutcutcodec/examples/logo.svg")

    @property
    def filename(self) -> pathlib.Path:
        """Return the path to the physical file that contains the svg data."""
        return self._filename


class _StreamVideoSVG(StreamVideo):
    """Read SVG as a video stream.

    Parameters
    ----------
    height : int
        The preconised dimension i (vertical) of the picture in pxl (readonly).
    width : int
        The preconised dimension j (horizontal) of the picture in pxl (readonly).
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: ContainerInputSVG):
        assert isinstance(node, ContainerInputSVG), node.__class__.__name__
        super().__init__(node)
        with open(node.filename, "rb") as raw:
            self._bytestring = raw.read()
        try:
            pngdata = cairosvg.svg2png(self._bytestring, unsafe=self.node.unsafe)
        except xml.etree.ElementTree.ParseError as err:
            raise DecodeError(f"failed to read the svg file {node.filename} with cairosvg") from err
        img = torch.from_numpy(cv2.imdecode(np.frombuffer(pngdata, np.uint8), cv2.IMREAD_UNCHANGED))
        self._height, self._width, _ = img.shape
        self._shape_and_img = ((self._height, self._width), img)

    def _get_img(self, shape: tuple[int, int]) -> torch.Tensor:
        """Cache the image."""
        if self._shape_and_img[0] != shape:
            self._shape_and_img = (
                shape,
                torch.from_numpy(
                    cv2.imdecode(
                        np.frombuffer(
                            cairosvg.svg2png(
                                self._bytestring,
                                unsafe=self.node.unsafe,
                                output_height=shape[0],
                                output_width=shape[1],
                            ),
                            np.uint8,
                        ),
                        cv2.IMREAD_UNCHANGED,
                    ),
                ),
            )
        return self._shape_and_img[1]

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no svg frame at timestamp {timestamp} (need >= 0)")
        return FrameVideo(timestamp, self._get_img(mask.shape).clone())

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        return math.inf

    @property
    def height(self) -> int:
        """Return the preconised dimension i (vertical) of the picture in pxl."""
        return self._height

    @property
    def width(self) -> int:
        """Return the preconised dimension j (horizontal) of the picture in pxl."""
        return self._width
