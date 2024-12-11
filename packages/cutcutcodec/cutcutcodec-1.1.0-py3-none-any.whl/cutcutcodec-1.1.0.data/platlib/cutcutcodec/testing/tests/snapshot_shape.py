#!/usr/bin/env python3

"""Test the video stream snapshot shape."""

import itertools

from cutcutcodec.core.filter.video.resize import FilterVideoResize
from cutcutcodec.core.generation.video.empty import GeneratorVideoEmpty
from cutcutcodec.testing.generation import extract_streams


def test_shape():
    """Extract snapshot in all video streams."""
    for stream in extract_streams():
        if stream.type != "video":
            continue
        if isinstance(stream.node, (GeneratorVideoEmpty, FilterVideoResize)):
            continue
        for height, width in itertools.product([1, 2, 3, 100, 101], [1, 2, 3, 100, 101]):
            frame = stream.snapshot(0, (height, width))
            assert frame.height == height, (frame, height, frame.height)
            assert frame.width == width, (frame, width, frame.width)
