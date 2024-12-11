#!/usr/bin/env python3

"""Smartly choose the framerate of a video stream."""

from fractions import Fraction
import math
import typing

from cutcutcodec.core.analysis.stream.time_backprop import time_backprop
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG


FPS_ESTIMATORS = {}  # to each node stream class, associate the func to find the optimal rate


def _add_estimator(node_cls: type) -> typing.Callable:
    def _add_func(func) -> typing.Callable:
        FPS_ESTIMATORS[node_cls] = func
        return func
    return _add_func


@_add_estimator(ContainerInputFFMPEG)
def _optimal_rate_container_input_ffmpeg(stream: StreamVideo, *_) -> Fraction:
    """Detect the rate of a ContainerInputFFMPEG stream.

    Examples
    --------
    >>> from cutcutcodec.core.analysis.stream.rate_video import optimal_rate_video
    >>> from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
    >>> (stream,) = ContainerInputFFMPEG("cutcutcodec/examples/video.mp4").out_streams
    >>> optimal_rate_video(stream)
    Fraction(25, 1)
    >>>
    """
    assert isinstance(stream.node, ContainerInputFFMPEG), stream.node.__class__.__name__
    return stream.rate


def optimal_rate_video(
    stream: StreamVideo,
    t_min: typing.Optional[Fraction] = None,
    t_max: typing.Optional[typing.Union[Fraction, float]] = None,
    choices: typing.Optional[set[Fraction]] = None,
) -> Fraction:
    """Find the optimal frame rate for a given video stream.

    Parameters
    ----------
    stream : cutcutcodec.core.classes.stream_video.StreamVideo
        The video stream that we want to find the optimal fps.
    t_min : float, optional
        The lower bound of the time slice estimation.
    t_max : float, optional
        The higher bound of the time slice estimation.
    choices : set[Fraction], optional
        The possible fps. If provide, returns the most appropriate fps of this set.

    Returns
    -------
    framerate : numbers.Real
        The framerate (maximum) that allows to minimize / cancel the loss of information,
        (minimum) and avoids an excess of frame that does not bring more information.
    """
    # verifications
    assert isinstance(stream, StreamVideo), stream.__class__.__name__
    assert t_min is None or isinstance(t_min, Fraction), t_min.__class__.__name__
    assert t_max is None or t_max == math.inf or isinstance(t_max, Fraction), t_max
    if choices is not None:
        assert isinstance(choices, set) and all(isinstance(r, Fraction) and r > 0 for r in choices)

    # optimisation
    if choices and len(choices) == 1:  # case not nescessary to do computing
        return choices.pop()

    # estimation of the best fps
    t_min, t_max = t_min or stream.beginning, t_max or stream.beginning + stream.duration
    if (estimator := FPS_ESTIMATORS.get(stream.node.__class__, None)) is not None:
        fps = estimator(stream, t_min, t_max)
    else:
        fps = max(
            (
                optimal_rate_video(s, *t)
                for s, *t in time_backprop(stream, t_min, t_max)
                if s.type == "video"
            ),
            default=0,
        )

    # select the most appropriate rate among the choices
    if not choices or not fps:
        return min(choices) if choices else fps
    for choice in sorted(choices):
        if fps <= choice:
            return choice
    return max(choices)
