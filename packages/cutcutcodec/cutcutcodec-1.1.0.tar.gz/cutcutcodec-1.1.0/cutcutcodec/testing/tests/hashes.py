#!/usr/bin/env python3

"""Ensures that the hashes are consistent."""

import itertools

from cutcutcodec.core.classes.container import ContainerOutput
from cutcutcodec.core.opti.cache.hashes.graph import compute_graph_items_hash
from cutcutcodec.core.compilation.tree_to_graph import tree_to_graph
from cutcutcodec.testing.generation import extract_streams


def test_invariance_and_differences():
    """Ensures that the function is repeatable and that it can detect differences."""
    all_graphs = [
        tree_to_graph(ContainerOutput([stream]))
        for stream in extract_streams()
    ]
    hashes = [compute_graph_items_hash(graph) for graph in all_graphs]
    for graph, signature in zip(all_graphs, hashes):
        assert compute_graph_items_hash(graph) == signature
    for hash_1, hash_2 in itertools.combinations(hashes, 2):
        assert hash_1 != hash_2
