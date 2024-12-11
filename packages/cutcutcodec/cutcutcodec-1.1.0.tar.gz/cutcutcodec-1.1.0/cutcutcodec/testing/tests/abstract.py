#!/usr/bin/env python3

"""Ensures that the methods and attributes of abstract classes are well defined."""

from fractions import Fraction
import math

import pytest

from cutcutcodec.core.classes.node import Node
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.testing.generation import extract_streams


def test_node_default():
    """Make sure the ``default`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None

    class _NodeOk(_Node):
        default = None

    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Node",
    ):
        _Node([], [])  # pylint: disable=E0110
    _NodeOk([], [])


def test_node_getstate():
    """Make sure the ``getstate`` method is abstract."""

    class _Node(Node):
        _setstate = None
        default = None

    class _NodeOk(_Node):
        _getstate = None

    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Node",
    ):
        _Node([], [])  # pylint: disable=E0110
    _NodeOk([], [])


def test_node_setstate():
    """Make sure the ``getstate`` method is abstract."""

    class _Node(Node):
        _getstate = None
        default = None

    class _NodeOk(_Node):
        _setstate = None

    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Node",
    ):
        _Node([], [])  # pylint: disable=E0110
    _NodeOk([], [])


def test_stream_beginning():
    """Make sure the ``duration`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None
        default = None

    class _Stream(Stream):
        duration = None
        is_space_continuous = None
        is_time_continuous = None
        type = None

    class _StreamOk(_Stream):
        beginning = None

    node = _Node([], [])
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Stream",
    ):
        _Stream(node)  # pylint: disable=E0110
    _StreamOk(node)

    for stream in extract_streams():
        assert isinstance(stream.beginning, Fraction)


def test_stream_duration():
    """Make sure the ``duration`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None
        default = None

    class _Stream(Stream):
        beginning = None
        is_space_continuous = None
        is_time_continuous = None
        type = None

    class _StreamOk(_Stream):
        duration = None

    node = _Node([], [])
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Stream",
    ):
        _Stream(node)  # pylint: disable=E0110
    _StreamOk(node)

    for stream in extract_streams():
        duration = stream.duration
        assert isinstance(duration, Fraction) or duration == math.inf
        assert duration >= 0


def test_stream_space_continuous():
    """Make sure the ``is_space_continuous`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None
        default = None

    class _Stream(StreamVideo):
        beginning = None
        duration = None
        is_time_continuous = None
        type = None

    class _StreamOk(_Stream):
        is_space_continuous = None

    node = _Node([], [])
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Stream",
    ):
        _Stream(node)  # pylint: disable=E0110
    _StreamOk(node)

    for stream in (s for s in extract_streams() if isinstance(s, StreamVideo)):
        assert isinstance(stream.is_space_continuous, bool)


def test_stream_time_continuous():
    """Make sure the ``is_time_continuous`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None
        default = None

    class _Stream(Stream):
        beginning = None
        duration = None
        is_space_continuous = None
        type = None

    class _StreamOk(_Stream):
        is_time_continuous = None

    node = _Node([], [])
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Stream",
    ):
        _Stream(node)  # pylint: disable=E0110
    _StreamOk(node)

    for stream in extract_streams():
        assert isinstance(stream.is_time_continuous, bool)


def test_stream_type():
    """Make sure the ``type`` method is abstract."""

    class _Node(Node):
        _getstate = None
        _setstate = None
        default = None

    class _Stream(Stream):
        beginning = None
        duration = None
        is_space_continuous = None
        is_time_continuous = None

    class _StreamOk(_Stream):
        type = None

    node = _Node([], [])
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class _Stream",
    ):
        _Stream(node)  # pylint: disable=E0110
    _StreamOk(node)

    for stream in extract_streams():
        assert isinstance(stream.type, str)
        assert stream.type in {"audio", "subtitle", "video"}
