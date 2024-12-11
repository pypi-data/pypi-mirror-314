#!/usr/bin/env python3

"""Interface between windows and data."""

import pathlib
import threading
import typing

import networkx

from cutcutcodec.core.classes.container import ContainerOutput
from cutcutcodec.core.classes.node import Node
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.compilation.graph_to_json import graph_to_json
from cutcutcodec.core.compilation.graph_to_tree import graph_to_tree, update_trees
from cutcutcodec.core.compilation.json_to_graph import json_to_graph
from cutcutcodec.core.compilation.tree_to_graph import tree_to_graph
from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise


class App:
    """Contains the shared data.

    Attributes
    ----------
    export_settings : dict[str]
        The exportation parameters for ffmpeg.
    graph : networkx.MultiDiGraph
        The assembly graph, the main element that contains all the operations to be performed.
    """

    def __init__(self):
        self._persistant = {}  # all for the state.
        self._compile_lock = threading.Lock()
        self._graph = tree_to_graph(
            ContainerOutput(
                [
                    GeneratorAudioNoise().out_streams[0],
                    GeneratorVideoNoise().out_streams[0],
                ]
            )
        )
        self.global_vars = {}

    def __getstate__(self) -> dict:
        """Allow to help serialization and saving."""
        return {
            "export_settings": self.export_settings,
            "graph": graph_to_json(self.graph),
        }

    def __setstate__(self, state: dict):
        """Allow deserialization."""
        assert isinstance(state, dict), state.__class__.__name__

        self._persistant["export_settings"] = state.get("export_settings", {})
        if (graph := state.get("graph", None)) is not None:
            graph = json_to_graph(graph)
        self.graph = graph

    @property
    def export_settings(self) -> dict[str]:
        """Return the exporation parameters for writting.

        Notes
        -----
        * Modifications are inplace.
        """
        export_settings = self._persistant.get("export_settings", {})
        export_settings["parent"] = export_settings.get("parent", str(pathlib.Path.cwd()))
        if "stem" not in export_settings:
            export_settings["stem"] = "cutcutcodec_project"
            while (pathlib.Path(export_settings["parent"]) / export_settings["stem"]).exists():
                export_settings["stem"] += "_bis"
        export_settings["suffix"] = export_settings.get("suffix", "")
        export_settings["muxer"] = export_settings.get("muxer", None)
        export_settings["muxer_settings"] = export_settings.get("muxer_settings", {})

        tree = self.tree()

        # codecs
        export_settings["codecs"] = export_settings.get("codecs", {"audio": [], "video": []})
        export_settings["codecs"]["audio"].extend([None for _ in tree.in_select("audio")])
        export_settings["codecs"]["video"].extend([None for _ in tree.in_select("video")])
        export_settings["codecs"]["audio"] = (
            export_settings["codecs"]["audio"][:len(tree.in_select("audio"))]
        )
        export_settings["codecs"]["video"] = (
            export_settings["codecs"]["video"][:len(tree.in_select("video"))]
        )

        # encoders
        export_settings["encoders"] = export_settings.get("encoders", {"audio": [], "video": []})
        export_settings["encoders"]["audio"].extend([None for _ in tree.in_select("audio")])
        export_settings["encoders"]["video"].extend([None for _ in tree.in_select("video")])
        export_settings["encoders"]["audio"] = (
            export_settings["encoders"]["audio"][:len(tree.in_select("audio"))]
        )
        export_settings["encoders"]["video"] = (
            export_settings["encoders"]["video"][:len(tree.in_select("video"))]
        )

        # encoders_settings
        export_settings["encoders_settings"] = (
            export_settings.get("encoders_settings", {"audio": [], "video": []})
        )
        export_settings["encoders_settings"]["audio"].extend([{} for _ in tree.in_select("audio")])
        export_settings["encoders_settings"]["video"].extend([{} for _ in tree.in_select("video")])
        export_settings["encoders_settings"]["audio"] = (
            export_settings["encoders_settings"]["audio"][:len(tree.in_select("audio"))]
        )
        export_settings["encoders_settings"]["video"] = (
            export_settings["encoders_settings"]["video"][:len(tree.in_select("video"))]
        )

        # fps, samplerate, shapes, bitrate and pix_fmt
        export_settings["rates"] = export_settings.get("rates", {"audio": [], "video": []})
        export_settings["rates"]["audio"].extend([None for _ in tree.in_select("audio")])
        export_settings["rates"]["video"].extend([None for _ in tree.in_select("video")])
        export_settings["rates"]["audio"] = (  # type int or None
            export_settings["rates"]["audio"][:len(tree.in_select("audio"))]
        )
        export_settings["rates"]["video"] = (  # type str or None
            export_settings["rates"]["video"][:len(tree.in_select("video"))]
        )
        export_settings["shapes"] = export_settings.get("shapes", [])  # tuple[int, int] or None
        export_settings["shapes"].extend([None for _ in tree.in_select("video")])
        export_settings["shapes"] = export_settings["shapes"][:len(tree.in_select("video"))]
        export_settings["shapes"] = (  # because json convert tuple into list
            [s if s is None else tuple(s) for s in export_settings["shapes"]]
        )
        export_settings["bitrate"] = export_settings.get("bitrate", {"audio": [], "video": []})
        export_settings["bitrate"]["audio"].extend([None for _ in tree.in_select("audio")])
        export_settings["bitrate"]["video"].extend([None for _ in tree.in_select("video")])
        export_settings["bitrate"]["audio"] = (
            export_settings["bitrate"]["audio"][:len(tree.in_select("audio"))]
        )
        export_settings["bitrate"]["video"] = (
            export_settings["bitrate"]["video"][:len(tree.in_select("video"))]
        )
        export_settings["pix_fmt"] = export_settings.get("pix_fmt", [])  # type str or None
        export_settings["pix_fmt"].extend([None for _ in tree.in_select("video")])
        export_settings["pix_fmt"] = export_settings["pix_fmt"][:len(tree.in_select("video"))]

        # optimization enable
        export_settings["optimize"] = export_settings.get("optimize", False)
        export_settings["excecute"] = export_settings.get("excecute", True)

        self._persistant["export_settings"] = export_settings  # for inplace edition, not setter

        return export_settings

    def get_save_file(self) -> typing.Union[None, pathlib.Path]:
        """Return the path for the saving file, None if it is not define."""
        return self._persistant.get("save_file", None)

    @property
    def graph(self) -> networkx.MultiDiGraph:
        """Return the assembly graph."""
        return self._graph

    @graph.setter
    def graph(self, graph: networkx.MultiDiGraph):
        """Perform verification."""
        assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__
        with self._compile_lock:
            self._graph = graph

    def redo(self):
        """Allow to move forward in the steps."""
        print("redo")

    def set_save_file(self, file: typing.Union[None, str, pathlib.Path]):
        """Update the path of the file for saving project."""
        if file is None:
            self._persistant["save_file"] = None
        assert isinstance(file, (str, pathlib.Path)), file.__class__.__name__
        file = pathlib.Path(file)
        self._persistant["save_file"] = file  # str for jsonisable

    def tree(self) -> ContainerOutput:
        """Return the node associated with the complete graph.

        Returns
        -------
        container_output : cutcutcodec.core.classes.container.ContainerOutput
            The terminal node of the assembly graph.
        """
        with self._compile_lock:
            container_output = graph_to_tree(self.graph)
        return container_output

    def tree_edge(self, edge: tuple[str, str, str]) -> Stream:
        """Return the updated tree of this edge.

        Parameters
        ----------
        edge : tuple[str, str, str]
            The name of the edge in the graph (src_node, dst_node, key).

        Returns
        -------
        Stream
            The dynamic tree corresponding to this edge.

        Notes
        -----
        All the ``tree`` attributes are updated to the current state of the assembly graph.
        """
        assert isinstance(edge, tuple), edge.__class__.__name__
        assert len(edge) == 3, edge
        for name in edge:
            assert isinstance(name, str), name.__class__.__name__
        with self._compile_lock:
            assert self.graph.has_edge(*edge), (edge, self.graph.edges)
            update_trees(self.graph)
            src, dst, key = edge
            tree = self.graph.edges[src, dst, key]["cache"][1]["tree"]
        return tree

    def tree_node(self, node: str) -> Node:
        """Return the updated tree of this node.

        Parameters
        ----------
        node : str
            The name of the node in the graph.

        Returns
        -------
        cutcutcodec.core.classes.node.Node
            The dynamic tree corresponding to this node.

        Notes
        -----
        All the ``tree`` attributes are updated to the current state of the assembly graph.
        """
        assert isinstance(node, str), node.__class__.__name__
        with self._compile_lock:
            assert node in self.graph
            update_trees(self.graph)
            tree = self.graph.nodes[node]["cache"][1]["tree"]
        return tree

    def undo(self):
        """Return to the previous step."""
        print("undo")
