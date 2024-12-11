#!/usr/bin/env python3

"""Smartly choose the shape of a video stream."""

from fractions import Fraction
import math
import typing

from cutcutcodec.core.analysis.stream.time_backprop import time_backprop
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.filter.video.resize import FilterVideoResize
from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
from cutcutcodec.core.io.read_image import ContainerInputImage
from cutcutcodec.core.io.read_svg import ContainerInputSVG


SHAPE_ESTIMATORS = {}  # to each node stream class, associate the func to find the optimal rate


def _add_estimator(node_cls: type) -> typing.Callable:
    def _add_func(func) -> typing.Callable:
        SHAPE_ESTIMATORS[node_cls] = func
        return func
    return _add_func


@_add_estimator(FilterVideoResize)
def _optimal_shape_filter_video_resize(stream: StreamVideo, *_) -> tuple[int, int]:
    """Detect the best shape of a FilterVideoReshape.

    Examples
    --------
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.filter.video.resize import FilterVideoResize
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> (stream,) = FilterVideoResize(GeneratorVideoNoise(0).out_streams, (360, 640)).out_streams
    >>> optimal_shape_video(stream)
    (360, 640)
    >>>
    """
    assert isinstance(stream.node, FilterVideoResize), stream.node.__class__.__name__
    return stream.node.shape


@_add_estimator(ContainerInputFFMPEG)
def _optimal_shape_container_input_ffmpeg(stream: StreamVideo, *_) -> tuple[int, int]:
    """Detect the shape of a ContainerInputFFMPEG.

    Examples
    --------
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
    >>> (stream,) = ContainerInputFFMPEG("cutcutcodec/examples/video.mp4").out_streams
    >>> optimal_shape_video(stream)
    (360, 640)
    >>>
    """
    assert isinstance(stream.node, ContainerInputFFMPEG), stream.node.__class__.__name__
    return (stream.height, stream.width)


@_add_estimator(ContainerInputImage)
def _optimal_shape_container_input_image(stream: StreamVideo, *_) -> tuple[int, int]:
    """Detect the shape of a ContainerInputFFMPEG.

    Examples
    --------
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.io.read_image import ContainerInputImage
    >>> (stream,) = ContainerInputImage("cutcutcodec/examples/logo.png").out_streams
    >>> optimal_shape_video(stream)
    (64, 64)
    >>>
    """
    assert isinstance(stream.node, ContainerInputImage), stream.node.__class__.__name__
    return (stream.height, stream.width)


@_add_estimator(ContainerInputSVG)
def _optimal_shape_container_input_svg(stream: StreamVideo, *_) -> tuple[int, int]:
    """Detect the shape of a ContainerInputFFMPEG.

    Examples
    --------
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.io.read_svg import ContainerInputSVG
    >>> (stream,) = ContainerInputSVG("cutcutcodec/examples/logo.svg").out_streams
    >>> optimal_shape_video(stream)
    (64, 64)
    >>>
    """
    assert isinstance(stream.node, ContainerInputSVG), stream.node.__class__.__name__
    return (stream.height, stream.width)


def optimal_shape_video(
    stream: StreamVideo,
    t_min: typing.Optional[Fraction] = None,
    t_max: typing.Optional[typing.Union[Fraction, float]] = None,
    choices: typing.Optional[set[tuple[int, int]]] = None,
) -> typing.Union[tuple[int, int], None]:
    """Find the optimal frame shape for a given video stream.

    Parameters
    ----------
    stream : cutcutcodec.core.classes.stream_video.StreamVideo
        The video stream that we want to find the optimal fps.
    t_min : float, optional
        The lower bound of the time slice estimation.
    t_max : float, optional
        The higher bound of the time slice estimation.
    choices : set[tuple[int, int]], optional
        The possible shape. If provide, returns the most appropriate shape of this set.
        The convention adopted is the numpy convention (height, width) in pixels.

    Returns
    -------
    shape : tuple[int, int]
        The shape that limit the reshape informations and the information loss.
    """
    # verifications
    assert isinstance(stream, StreamVideo), stream.__class__.__name__
    assert t_min is None or isinstance(t_min, Fraction), t_min.__class__.__name__
    assert t_max is None or t_max == math.inf or isinstance(t_max, Fraction), t_max
    if choices is not None:
        assert isinstance(choices, set), choices.__class__.__name__
        assert all(isinstance(s, tuple) for s in choices), choices
        assert all(len(s) == 2 for s in choices), choices
        assert all(isinstance(s[0], int) and isinstance(s[1], int) for s in choices), choices
        assert all(min(s) >= 1 for s in choices), choices

    def shape_key(shape):
        """Favorise little surface and square surface."""
        height, width = shape
        area = height * width
        deformation = 2*math.sqrt(area) / (height + width)  # 1 -> square, 0 -> flat
        return area - deformation

    # optimisation
    if choices and len(choices) == 1:  # case not nescessary to do computing
        return choices.pop()

    # estimation of the best shape
    t_min, t_max = t_min or stream.beginning, t_max or stream.beginning + stream.duration
    if (estimator := SHAPE_ESTIMATORS.get(stream.node.__class__, None)) is not None:
        shape = estimator(stream, t_min, t_max)
    else:
        shapes = (
            optimal_shape_video(s, *t) for s, *t in time_backprop(stream, t_min, t_max)
            if s.type == "video"
        )
        shapes = [s for s in shapes if s is not None]
        shape = (max(s[0] for s in shapes), max(s[1] for s in shapes)) if shapes else None

    # select the most appropriate rate among the choices
    if not choices or shape is None:
        return min(choices, key=shape_key) if choices else shape
    choices = sorted(choices, key=shape_key)
    for choice in choices:
        if shape[0] <= choice[0] and shape[1] <= choice[1]:
            return choice
    return choices[-1]
