#!/usr/bin/env python3

"""Resize an image."""

from fractions import Fraction
import numbers
import typing

import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideoWrapper
from .pad import pad_keep_ratio


def _resize(image: np.ndarray, shape: tuple[int, int], copy: bool) -> np.ndarray:
    """Help ``resize``.

    Notes
    -----
    * No verifications are performed for performance reason.
    * The output tensor can be a reference to the provided tensor if copy is False.
    """
    if image.shape[:2] == shape:  # optional optimization
        return image.copy() if copy else image
    height, width = shape
    enlarge = height >= image.shape[0] or width >= image.shape[1]
    image = np.ascontiguousarray(image)  # cv2 needs it
    image = cv2.resize(  # 10 times faster than torchvision.transforms.v2.functional.resize
        image,
        dsize=(width, height),
        interpolation=(cv2.INTER_CUBIC if enlarge else cv2.INTER_AREA),  # for antialiasing
    )
    if enlarge and np.issubdtype(image.dtype, np.floating):
        image = np.clip(image, 0.0, 1.0, out=image)
    return image


def resize(
    image: typing.Union[FrameVideo, torch.Tensor, np.ndarray],
    shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
    copy: bool = True,
) -> typing.Union[FrameVideo, torch.Tensor, np.ndarray]:
    """Reshape the image, can introduce a deformation.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        The image to be resized, of shape (height, width, channels).
        It has to match with the video image specifications.
    shape : int and int
        The pixel dimensions of the returned image.
        The convention adopted is the numpy convention (height, width).
    copy : boolean, default=True
        If True, ensure that the returned tensor doesn't share the data of the input tensor.

    Returns
    -------
    resized_image
        The resized image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize
    >>> ref = FrameVideo(0, torch.empty(480, 720, 3, dtype=torch.uint8))
    >>> resize(ref, (720, 1080)).shape  # upscaling
    (720, 1080, 3)
    >>> resize(ref, (480, 360)).shape  # downscaling
    (480, 360, 3)
    >>>
    """
    # case cast homogeneous
    if isinstance(image, FrameVideo):
        return FrameVideo(image.time, resize(torch.Tensor(image), shape, copy=copy))
    if isinstance(image, torch.Tensor):
        return torch.as_tensor(
            resize(image.numpy(force=True), shape, copy=copy), device=image.device
        )

    # verif case np.ndarray
    assert isinstance(image, np.ndarray), image.__class__.__name__
    assert image.ndim == 3, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert image.shape[2] in {1, 2, 3, 4}, image.shape
    assert image.dtype.type in {np.uint8, np.float32}
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
    shape = (int(shape[0]), int(shape[1]))
    assert isinstance(copy, bool), copy.__class__.__name__

    # resize
    return _resize(image, shape, copy=copy)


def resize_keep_ratio(
    image: typing.Union[FrameVideo, torch.Tensor, np.ndarray],
    shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
    copy: bool = True,
) -> typing.Union[FrameVideo, torch.Tensor, np.ndarray]:
    """Reshape the image, keep the spact ratio and pad with transparent pixels.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    shape : int and int
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    copy : boolean, default=True
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.

    Returns
    -------
    resized_image
        The resized (and padded) image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize_keep_ratio
    >>> ref = FrameVideo(0, torch.full((4, 8, 1), 128, dtype=torch.uint8))
    >>>
    >>> # upscale
    >>> resize_keep_ratio(ref, (8, 12))[..., 1]  # alpha layer
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]],
           dtype=torch.uint8)
    >>> resize_keep_ratio(ref, (8, 12)).convert(1)[..., 0]  # as gray
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]],
           dtype=torch.uint8)
    >>>
    >>> # downscale
    >>> resize_keep_ratio(ref, (4, 4))[..., 1]  # alpha layer
    tensor([[  0,   0,   0,   0],
            [255, 255, 255, 255],
            [255, 255, 255, 255],
            [  0,   0,   0,   0]], dtype=torch.uint8)
    >>> resize_keep_ratio(ref, (4, 4)).convert(1)[..., 0]  # as gray
    tensor([[  0,   0,   0,   0],
            [128, 128, 128, 128],
            [128, 128, 128, 128],
            [  0,   0,   0,   0]], dtype=torch.uint8)
    >>>
    >>> # mix
    >>> resize_keep_ratio(ref, (6, 6))[..., 1]  # alpha layer
    tensor([[  0,   0,   0,   0,   0,   0],
            [255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255],
            [  0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> resize_keep_ratio(ref, (6, 6)).convert(1)[..., 0]  # as gray
    tensor([[  0,   0,   0,   0,   0,   0],
            [128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128],
            [128, 128, 128, 128, 128, 128],
            [  0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>>
    """
    # minimalist verifications
    assert isinstance(image, (FrameVideo, torch.Tensor, np.ndarray)), image.__class__.__name__
    assert image.ndim >= 2, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape

    # find the shape for keeping proportion
    dw_sh, dh_sw = shape[1]*image.shape[0], shape[0]*image.shape[1]
    if dw_sh < dh_sw:  # need vertical padding
        height, width = (round(dw_sh/image.shape[1]), shape[1])  # keep width unchanged
    elif dw_sh > dh_sw:  # need horizontal padding
        height, width = (shape[0], round(dh_sw/image.shape[0]))  # keep height unchanged
    else:  # if the proportion is the same
        return resize(image, shape, copy=copy)

    # resize and pad
    image = resize(image, (height, width), copy=copy)
    image = pad_keep_ratio(image, shape, copy=False)
    return image


class FilterVideoResize(Filter):
    """Frozen the shape of the input stream.

    Attributes
    ----------
    keep_ratio : boolean
        True if the aspect ratio is keep, False otherwise (readonly).
    shape : tuple[int, int]
        The pixel dimensions of the incoming frames (readonly).
        The convention adopted is the numpy convention (height, width).

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> from cutcutcodec.core.filter.video.resize import FilterVideoResize
    >>> (stream_in,) = GeneratorVideoNoise(0).out_streams
    >>>
    >>> # keep ratio
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 8), keep_ratio=True).out_streams
    >>> stream_out.snapshot(0, (8, 12)).convert(1)[..., 0]
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
            [148, 126, 108, 109,  98,  91,  58,  25,  36, 107, 178, 214],
            [144, 135, 135, 157, 158, 139, 119,  68,  68, 160, 189, 176],
            [127, 130, 155, 203, 188, 149, 146, 119, 117, 167, 175, 161],
            [102, 107, 137, 193, 118,  29,  47, 119, 149,  61, 122, 218],
            [111, 100, 115, 176, 124,  64, 110, 144, 136,  81, 141, 222],
            [132,  97, 100, 164, 159, 154, 211, 167, 106, 145, 183, 202],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]],
           dtype=torch.uint8)
    >>> stream_out.snapshot(0, (4, 4)).convert(1)[..., 0]
    tensor([[  0,   0,   0,   0],
            [134, 144,  81, 173],
            [110, 130, 134, 152],
            [  0,   0,   0,   0]], dtype=torch.uint8)
    >>> stream_out.snapshot(0, (6, 6)).convert(1)[..., 0]
    tensor([[  0,   0,   0,   0,   0,   0],
            [137, 129, 117,  69,  98, 182],
            [121, 162, 122, 109, 123, 169],
            [115, 138, 125, 157, 124, 183],
            [  0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>>
    >>> # deformation
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 8), keep_ratio=False).out_streams
    >>> stream_out.snapshot(0, (8, 12))[..., 0]
    tensor([[143,  61,  31, 148, 246, 241, 129, 133, 177, 154, 176, 207],
            [111,  84,  94, 178, 209, 171, 102, 134, 177, 129, 160, 210],
            [ 57, 120, 197, 227, 148,  55,  56, 136, 178,  88, 134, 215],
            [ 82, 162, 246, 252, 134,  20,  37, 132, 181,  92, 130, 203],
            [173, 188, 214, 239, 174,  84,  54, 122, 185, 138, 149, 180],
            [209, 180, 171, 219, 208, 158, 117, 141, 181, 174, 174, 175],
            [171, 141, 138, 201, 219, 204, 193, 177, 172, 182, 189, 192],
            [149, 117, 118, 189, 226, 233, 239, 199, 166, 187, 199, 202]],
           dtype=torch.uint8)
    >>> stream_out.snapshot(0, (4, 4))[..., 0]
    tensor([[ 69, 235, 133, 172],
            [141, 131, 136, 128],
            [190, 195, 127, 162],
            [124, 223, 192, 196]], dtype=torch.uint8)
    >>> stream_out.snapshot(0, (6, 6))[..., 0]
    tensor([[114,  84, 255, 109, 165, 195],
            [ 90, 180, 142,  94, 142, 189],
            [104, 255,  60,  79, 134, 178],
            [188, 226, 139,  79, 169, 169],
            [182, 181, 200, 152, 179, 182],
            [140, 152, 226, 222, 174, 200]], dtype=torch.uint8)
    >>>
    """

    def __init__(
        self,
        in_streams: typing.Iterable[Stream],
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
        keep_ratio: bool = False,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        shape : tuple[int, int]
            The pixel dimensions of the incoming frames.
            The convention adopted is the numpy convention (height, width).
        keep_ratio : boolean, default=False
            If True, the returned frame is padded to keep the proportion of the incoming frame.
        """
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, len(shape)
        assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
        assert isinstance(keep_ratio, bool), keep_ratio.__class__.__name__
        self._shape = (int(shape[0]), int(shape[1]))
        self._keep_ratio = keep_ratio

        super().__init__(in_streams, in_streams)
        super().__init__(
            in_streams, [_StreamVideoResize(self, index) for index in range(len(in_streams))]
        )

    def _getstate(self) -> dict:
        return {
            "keep_ratio": self.keep_ratio,
            "shape": list(self.shape),
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state.keys() == {"keep_ratio", "shape"}, set(state)
        FilterVideoResize.__init__(self, in_streams, state["shape"], keep_ratio=state["keep_ratio"])

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls([], (720, 1080))

    @property
    def keep_ratio(self) -> bool:
        """Return True if the aspect ratio is keep, False otherwise."""
        return self._keep_ratio

    @property
    def shape(self) -> tuple[int, int]:
        """Return The pixel dimensions of the incoming frames."""
        return self._shape


class _StreamVideoResize(StreamVideoWrapper):
    """Translate a video stream from a certain delay."""

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        in_mask = torch.full(self.node.shape, True, dtype=bool)
        src = self.stream._snapshot(timestamp, in_mask)  # pylint: disable=W0212
        dst = (
            resize_keep_ratio(src, mask.shape)
            if self.node.keep_ratio else
            resize(src, mask.shape)
        )
        return dst
