#!/usr/bin/env python3

"""Compile and decompile all elements."""

from cutcutcodec.core.classes.container import ContainerOutput
from cutcutcodec.core.compilation.graph_to_ast import graph_to_ast
from cutcutcodec.core.compilation.graph_to_json import graph_to_json
from cutcutcodec.core.compilation.graph_to_tree import graph_to_tree
from cutcutcodec.core.compilation.json_to_graph import json_to_graph
from cutcutcodec.core.compilation.tree_to_graph import tree_to_graph
from cutcutcodec.testing.generation import extract_streams


def test_all_types_tree2graph2tree2graph():
    """Compile and decompile all types of streams from tree."""
    for stream in extract_streams():
        graph1 = tree_to_graph(ContainerOutput([stream]))
        graph2 = tree_to_graph(graph_to_tree(graph1))
        assert graph1.edges == graph2.edges
        assert graph1.nodes("class") == graph2.nodes("class")
        assert graph1.nodes("state") == graph2.nodes("state")


def test_all_types_tree2graph2ast2tree():
    """Compile and decompile all types of streams from ast."""
    for stream in extract_streams():
        tree1 = ContainerOutput([stream])
        mod_code = compile(graph_to_ast(tree_to_graph(tree1)), filename="", mode="exec")
        context = {}
        # load the references in context, not in locals()
        exec(mod_code, context, context)  # pylint: disable=W0122
        tree2 = context["get_complete_tree"]()
        assert tree1 == tree2


def test_all_types_tree2graph2json2graph():
    """Compile and decompile all types of streams from json."""
    for stream in extract_streams():
        graph1 = tree_to_graph(ContainerOutput([stream]))
        graph2 = json_to_graph(graph_to_json(graph1))
        assert graph1.edges == graph2.edges
        assert graph1.nodes("class") == graph2.nodes("class")
        assert graph1.nodes("state") == graph2.nodes("state")
