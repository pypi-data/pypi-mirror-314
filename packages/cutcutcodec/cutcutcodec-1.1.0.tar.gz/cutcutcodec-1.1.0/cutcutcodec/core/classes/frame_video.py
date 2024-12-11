#!/usr/bin/env python3

"""Defines the structure a video frame."""

from fractions import Fraction
import numbers
import re
import typing

import numpy as np
import torch

from cutcutcodec.core.classes.frame import Frame
from cutcutcodec.core.filter.mix.video_cast import to_gray, to_gray_alpha, to_bgr, to_bgr_alpha


class FrameVideo(Frame):
    """An image with time information for video context.

    Behaves like a torch tensor of shape (height, width, channels).
    The shape is consistent with pyav and cv2.
    The dtype is automaticaly cast into torch.uint8.

    Parameters
    ----------
    channels : int
        The numbers of layers (readonly):

            * 1 -> grayscale
            * 2 -> grayscale, alpha
            * 3 -> blue, green, red
            * 4 -> blue, green, red, alpha
    height : int
        The dimension i (vertical) of the image in pxl (readonly).
    time : Fraction
        The time of the frame inside the video stream in second (readonly).
    width : int
        The dimension j (horizontal) of the image in pxl (readonly).
    """

    def __new__(  # pylint: disable=W0222
        cls,
        time: typing.Union[Fraction, numbers.Real, str],
        data: typing.Union[torch.Tensor, np.ndarray, typing.Container],
        **kwargs,
    ):
        """Construct a video frame and normalize the type.

        Parameters
        ----------
        time : Fraction
            The time of the frame inside the video stream in second
        data : arraylike
            Transmitted to ``cutcutcodec.core.classes.frame.Frame`` initialisator.
        **kwargs : dict
            Transmitted to ``cutcutcodec.core.classes.frame.Frame`` initialisator.
        """
        # create frame
        frame = super().__new__(cls, data, context=time, **kwargs)

        # cast shape
        if frame.ndim == 2:  # give flexibility for grayscale images
            frame = frame.unsqueeze(2)

        # verifications
        frame.check_state()
        return frame

    def __repr__(self) -> str:
        """Compact and complete display of an evaluable version of the video frame.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo("2/4", torch.zeros((480, 720, 3), dtype=torch.uint8))  # doctest: +ELLIPSIS
        FrameVideo('1/2', [[[0, 0, 0],
                            ...
                            [0, 0, 0]]])
        >>>
        """
        time_str = f"'{self.time}'" if int(self.time) != self.time else f"{self.time}"
        header = f"{self.__class__.__name__}({time_str}, "
        tensor_str = np.array2string(
            self.numpy(force=True), separator=", ", prefix=header, suffix=" "
        )
        if (infos := re.findall(r"\w+=[a-zA-Z0-9_\-.\"']+", torch.Tensor.__repr__(self))):
            infos = [inf for inf in infos if inf != "dtype=torch.uint8"]
        if infos:
            infos = "\n" + " "*len(header) + (",\n" + " "*len(header)).join(infos)
            return f"{header}{tensor_str},{infos})"
        return f"{header}{tensor_str})"

    @property
    def channels(self) -> int:
        """Return the numbers of layers.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, torch.empty(480, 720, 3)).channels
        3
        >>>
        """
        return self.shape[2]

    def check_state(self) -> None:
        """Apply verifications.

        Raises
        ------
        AssertionError
            If something wrong in this frame.
        """
        context = getattr(self, "context", None)
        assert context is not None
        assert isinstance(context, (Fraction, numbers.Real, str)), context.__class__.__name__
        setattr(self, "context", Fraction(context))
        assert self.ndim == 3, self.shape
        assert self.shape[0] > 0, self.shape
        assert self.shape[1] > 0, self.shape
        assert self.shape[2] in {1, 2, 3, 4}, self.shape
        assert self.dtype in {torch.uint8, torch.float32}, self.dtype

    def convert(self, channels: int) -> Frame:
        """Change the numbers of channels of the frame.

        Returns
        -------
        frame : cutcutcodec.core.classes.frame_video.FrameVideo
            The new frame, be carfull, undergroud data can be shared.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> _ = torch.manual_seed(0)
        >>> ref_gray = FrameVideo(0, torch.randint(0, 256, (480, 720, 1), dtype=torch.uint8))
        >>> ref_gray_alpha = FrameVideo(0, torch.randint(0, 256, (480, 720, 2), dtype=torch.uint8))
        >>> ref_bgr = FrameVideo(0, torch.randint(0, 256, (480, 720, 3), dtype=torch.uint8))
        >>> ref_bgr_alpha = FrameVideo(0, torch.randint(0, 256, (480, 720, 4), dtype=torch.uint8))
        >>>
        >>> # case 1 -> 2, 3, 4
        >>> gray_alpha = ref_gray.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.equal(gray_alpha[..., 0], ref_gray[..., 0])
        True
        >>> torch.eq(gray_alpha[..., 1], 255).all()
        tensor(True)
        >>> bgr = ref_gray.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0], ref_gray[..., 0])
        True
        >>> torch.equal(bgr[..., 1], ref_gray[..., 0])
        True
        >>> torch.equal(bgr[..., 2], ref_gray[..., 0])
        True
        >>> bgr_alpha = ref_gray.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_gray[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_gray[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_gray[..., 0])
        True
        >>> torch.eq(bgr_alpha[..., 3], 255).all()
        tensor(True)
        >>>
        >>> # case 2 -> 1, 3, 4
        >>> gray = ref_gray_alpha.convert(1)
        >>> gray.channels
        1
        >>> torch.equal(gray[..., 0],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> bgr = ref_gray_alpha.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 1],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 2],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> bgr_alpha = ref_gray_alpha.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 3], ref_gray_alpha[..., 1])
        True
        >>>
        >>> # case 3 -> 1, 2, 4
        >>> gray = ref_bgr.convert(1)
        >>> gray.channels
        1
        >>> gray_alpha = ref_bgr.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.eq(gray_alpha[..., 1], 255).all()
        tensor(True)
        >>> bgr_alpha = ref_bgr.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_bgr[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_bgr[..., 1])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_bgr[..., 2])
        True
        >>> torch.eq(bgr_alpha[..., 3], 255).all()
        tensor(True)
        >>>
        >>> # case 4 -> 1, 2, 3
        >>> gray = ref_bgr_alpha.convert(1)
        >>> gray.channels
        1
        >>> gray_alpha = ref_bgr_alpha.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.equal(gray_alpha[..., 1], ref_bgr_alpha[..., 3])
        True
        >>> bgr = ref_bgr_alpha.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 1],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 1]))
        True
        >>> torch.equal(bgr[..., 2],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 2]))
        True
        >>>
        """
        assert isinstance(channels, int), channels.__class__.__name__
        assert 1 <= channels <= 4, f"channels can only be 1, 2, 3, or 4, not {channels}"
        converter = {1: to_gray, 2: to_gray_alpha, 3: to_bgr, 4: to_bgr_alpha}[channels]
        return self.__class__(self.time, converter(self))

    @property
    def height(self) -> int:
        """Return the dimension i (vertical) of the image in pxl.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, torch.empty(480, 720, 3)).height
        480
        >>>
        """
        return self.shape[0]

    @property
    def time(self) -> Fraction:
        """Return the time of the frame inside the video stream in second.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, torch.empty(480, 720, 3)).time
        Fraction(0, 1)
        >>>
        """
        return self.context

    def to_numpy_bgr(self, contiguous=False) -> np.ndarray[np.uint8]:
        """Return the 3 channels uint8 numpy frame representation.

        Parameters
        ----------
        contiguous : boolean, default=False
            If True, guaranti that the returned numpy array is c-contiguous.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>>
        >>> # from float32
        >>> frame = FrameVideo(0, torch.zeros(480, 720, 3)).to_numpy_bgr()  # classical bgr
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, torch.zeros(480, 720, 3)).to_numpy_bgr()  # grayscale
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, torch.zeros(480, 720, 3)).to_numpy_bgr()  # alpha channel
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>>
        >>> # from uint8
        >>> frame = FrameVideo(0, torch.empty(480, 720, 3, dtype=torch.uint8)).to_numpy_bgr()
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, torch.empty(480, 720, 3, dtype=torch.uint8)).to_numpy_bgr()
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, torch.empty(480, 720, 3, dtype=torch.uint8)).to_numpy_bgr()
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>>
        """
        assert isinstance(contiguous, bool), contiguous.__class__.__name__
        frame_np = self.convert(3).numpy(force=True)
        if frame_np.dtype == np.float32:
            frame_np = frame_np.copy()
            frame_np *= 255.0
            frame_np += 0.5  # to transform floor in round
            frame_np = frame_np.astype(np.uint8)  # floor
        if contiguous:
            return np.ascontiguousarray(frame_np)
        return frame_np

    @property
    def width(self) -> int:
        """Return the dimension j (horizontal) of the image in pxl.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, torch.empty(480, 720, 3)).width
        720
        >>>
        """
        return self.shape[1]
