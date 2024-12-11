#!/usr/bin/env python3

"""Check the consistency between the number of incoming and outgoing streams."""

import pytest

from cutcutcodec.core.classes.container import ContainerInput, ContainerOutput
from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.compilation.graph_to_tree import new_node
from cutcutcodec.core.generation.audio.empty import GeneratorAudioEmpty
from cutcutcodec.testing.generation import extract_cls_and_default


def test_empty():
    """Check that all filters can be emptied."""
    for cls, node in extract_cls_and_default():
        if not issubclass(cls, Filter) or issubclass(cls, (ContainerInput, ContainerOutput)):
            continue
        empty_filter = new_node(cls, [], node.getstate())
        assert empty_filter.in_streams == ()
        assert empty_filter.out_streams == (), cls


def test_raise_semi_empty():
    """Ensures that a filter cannot be half empty."""
    class _Filter(Filter):
        _getstate = None
        _setstate = None
        default = None

    stream = GeneratorAudioEmpty().out_streams[0]
    _Filter([], [])
    with pytest.raises(AssertionError):
        _Filter([stream], [])
    with pytest.raises(AssertionError):
        _Filter([], [stream])
    _Filter([stream], [stream])
    _Filter([stream], [stream, stream])
    _Filter([stream, stream], [stream])
    _Filter([stream, stream], [stream, stream])
