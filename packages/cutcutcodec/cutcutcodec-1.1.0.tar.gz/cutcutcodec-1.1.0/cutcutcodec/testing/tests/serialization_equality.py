#!/usr/bin/env python3

"""Ensures that objects serialize correctly and remain equivalent.

* Checks that the classes that inherit from ``cutcutcodec.core.classes.node.Node`` are pickable.
* Checks that classes inheriting from ``cutcutcodec.core.classes.stream.Stream``
    can serialize and attach to there node.
* Checks that the deserialized objects are equal to there initial version.
"""

import itertools
import json

import pickle
import typing

from cutcutcodec.core.classes.node import Node
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.testing.generation import extract_default, extract_streams


def single_check(obj: typing.Union[Node, Stream]):
    """Perform serialization and equality tests on a single object."""
    assert isinstance(obj, (Node, Stream)), obj.__class__.__name__
    # every node and stream must be equal to itself
    assert obj == obj  # pylint: disable=R0124
    obj_bis = pickle.loads(pickle.dumps(obj))  # must be serializable with the native pickle module
    assert obj_bis is not obj
    assert obj_bis == obj  # serializing and deserializing should not change much
    if isinstance(obj, Node):
        state = obj.getstate()
        assert isinstance(state, dict)  # state need to be dict
        assert all(isinstance(k, str) for k in state)  # all keys need to be str
        assert json.loads(json.dumps(state)) == state  # node state needs to be jsonisable


def inequality_check(objs: typing.Iterable[typing.Union[Node, Stream]]):
    """Check that all the objects provided are different."""
    for obj_1, obj_2 in itertools.combinations(objs, 2):
        assert obj_1 != obj_2


def test_node_are_differents():
    """Ensure that all nodes are differents."""
    inequality_check(extract_default())


def test_streams_serialization():
    """Perform checks on streams independently."""
    for stream in extract_streams():
        single_check(stream)
