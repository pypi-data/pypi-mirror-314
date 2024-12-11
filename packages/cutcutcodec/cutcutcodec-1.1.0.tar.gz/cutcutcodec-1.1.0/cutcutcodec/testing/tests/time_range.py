#!/usr/bin/env python3

"""Check that the start times and durations of the streams are consistent."""

from fractions import Fraction
import math

import pytest

from cutcutcodec.core.exceptions import OutOfTimeRange
from cutcutcodec.testing.generation import extract_streams


def test_time_range_audio():
    """Ensures that audio snapshots only exist in the interval [start, end[."""
    for stream in extract_streams():
        if stream.type != "audio":
            continue
        t_min = stream.beginning
        t_max = t_min + stream.duration
        assert t_max >= t_min
        with pytest.raises(OutOfTimeRange):  # f"t={t_min-1}, stream={stream}"
            stream.snapshot(t_min - 1)
        if t_max < math.inf:
            with pytest.raises(OutOfTimeRange):  # f"t={t_max+1}, stream={stream}"
                stream.snapshot(t_max + 1)
            with pytest.raises(OutOfTimeRange):  # f"t={t_max}, stream={stream}"
                stream.snapshot(t_max)
        if t_max != t_min:
            if t_max < math.inf:
                rate = 1 + math.ceil(Fraction(3, (t_max-t_min)))
                stream.snapshot(t_min, rate, 3)
                stream.snapshot(t_max-Fraction(3, rate), rate, 3)


def test_time_range_video():
    """Ensures that video snapshots only exist in the interval [start, end[."""
    for stream in extract_streams():
        if stream.type != "video":
            continue
        t_min = stream.beginning
        t_max = t_min + stream.duration
        assert t_max >= t_min
        with pytest.raises(OutOfTimeRange):  # f"t={t_min-1}, stream={stream}"
            stream.snapshot(t_min - 1, (1, 1))
        if t_max < math.inf:
            with pytest.raises(OutOfTimeRange):  # f"t={t_max+1}, stream={stream}"
                stream.snapshot(t_max + 1, (1, 1))
            with pytest.raises(OutOfTimeRange):  # f"t={t_max}, stream={stream}"
                stream.snapshot(t_max, (1, 1))
        if t_max != t_min:
            stream.snapshot(t_min, (1, 1))  # close start insterval
            if t_max < math.inf:
                stream.snapshot((t_min + t_max)/2, (1, 1))
                stream.snapshot(t_max - Fraction(1, 100_000), (1, 1))
