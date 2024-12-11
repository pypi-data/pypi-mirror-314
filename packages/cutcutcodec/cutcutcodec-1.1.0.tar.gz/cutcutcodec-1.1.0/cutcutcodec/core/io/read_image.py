#!/usr/bin/env python3

"""Read an image with opencv."""

from fractions import Fraction
import math
import pathlib
import typing

import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import DecodeError, OutOfTimeRange
from cutcutcodec.core.filter.video.resize import resize_keep_ratio


def read_image(filename: typing.Union[str, bytes, pathlib.Path]) -> torch.Tensor:
    """Read the image and make it compatible with Video Frame.

    Parameters
    ----------
    filename : pathlike
        The pathlike of the image file.

    Returns
    -------
    image : torch.Tensor
        The image in uint8 or float32 of shape (height, width, channels).

    Raises
    ------
    cutcutcodec.core.exceptions.DecodeError
        If it fails to read the image.
    """
    filename = pathlib.Path(filename).expanduser().resolve()
    assert filename.is_file(), filename

    if (img := cv2.imread(str(filename), cv2.IMREAD_UNCHANGED)) is None:
        raise DecodeError(f"failed to read the image {filename} with cv2")

    if img.ndim == 2:
        img = np.expand_dims(img, 2)

    if img.dtype != np.uint8 and np.issubdtype(img.dtype, np.integer):
        iinfo = np.iinfo(img.dtype)
        img = img.astype(np.float32)
        img -= float(iinfo.min)
        img *= 1.0 / float(iinfo.max - iinfo.min)
    elif img.dtype != np.float32 and np.issubdtype(img.dtype, np.floating):
        img = img.astype(np.float32)

    torch_img = torch.from_numpy(img)
    return torch_img


class ContainerInputImage(ContainerInput):
    """Decode an image.

    Attributes
    ----------
    filename : pathlib.Path
        The path to the physical file that contains the extracted image stream (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.io.read_image import ContainerInputImage
    >>> (stream,) = ContainerInputImage.default().out_streams
    >>> stream.snapshot(0, (12, 12))[..., 3]
    tensor([[  0,   0,   9, 113, 204, 247, 247, 203, 113,  10,   0,   0],
            [  0,  30, 208, 255, 255, 255, 255, 255, 255, 208,  30,   0],
            [  9, 208, 255, 255, 255, 255, 255, 255, 255, 255, 208,   9],
            [113, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 113],
            [204, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 203],
            [247, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 246],
            [247, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 246],
            [204, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 203],
            [113, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 113],
            [  9, 208, 255, 255, 255, 255, 255, 255, 255, 255, 208,   9],
            [  0,  30, 208, 255, 255, 255, 255, 255, 255, 208,  30,   0],
            [  0,   0,   9, 113, 203, 246, 246, 203, 113,   9,   0,   0]],
           dtype=torch.uint8)
    >>>
    """

    def __init__(self, filename: typing.Union[str, bytes, pathlib.Path]):
        """Initialise and create the class.

        Parameters
        ----------
        filename : pathlike
            Path to the file to be decoded.

        Raises
        ------
        cutcutcodec.core.exceptions.DecodeError
            If it fail to extract any multimedia stream from the provided file.
        """
        filename = pathlib.Path(filename).expanduser().resolve()
        assert filename.is_file(), filename
        self._filename = filename
        super().__init__([_StreamVideoImage(self)])

    def __enter__(self):
        """Make the object compatible with a context manager."""
        return self

    def __exit__(self, *_):
        """Exit the context manager."""

    def _getstate(self) -> dict:
        return {"filename": str(self.filename)}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename"}
        assert state.keys() == keys, set(state)-keys
        ContainerInputImage.__init__(self, state["filename"])

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls("cutcutcodec/examples/logo.png")

    @property
    def filename(self) -> pathlib.Path:
        """Return the path to the physical file that contains the extracted image stream."""
        return self._filename


class _StreamVideoImage(StreamVideo):
    """Read an image as a video stream.

    Parameters
    ----------
    height : int
        The dimension i (vertical) of the encoded frames in pxl (readonly).
    width : int
        The dimension j (horizontal) of the encoded frames in pxl (readonly).
    """

    is_space_continuous = False
    is_time_continuous = False

    def __init__(self, node: ContainerInputImage):
        assert isinstance(node, ContainerInputImage), node.__class__.__name__
        super().__init__(node)
        self._img = read_image(node.filename)
        self._height, self._width, *_ = self._img.shape
        self._resized_img = FrameVideo(0, self._img)  # not from_numpy for casting shape and type

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no image frame at timestamp {timestamp} (need >= 0)")

        # reshape if needed
        if self._resized_img.shape[:2] != mask.shape:
            self._resized_img = resize_keep_ratio(FrameVideo(0, self._img), mask.shape)

        return FrameVideo(timestamp, self._resized_img.clone())

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
