#!/usr/bin/env python3

"""Description of a node for the flow chart."""

from qtpynodeeditor.enums import PortType
from qtpynodeeditor.node_data import NodeDataModel, NodeDataType

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.node import Node


# verify=False solves "ValueError: Cannot leave data_type unspecified"
class AssemblyGraphNode(NodeDataModel, verify=False):  # type: ignore [call-arg]
    """General assembly graph node widget."""

    caption_visible = True
    port_caption_visible = False
    data_type = None  # solve w0223 'data_type' is abstract

    @property
    def caption(self) -> str:
        """Allow to display the correct name."""
        return self.name


def meta_node_creator(node: Node) -> type:
    """Complete the class attributes of a node present in the graph."""
    data_type = {
        PortType.input: {i: NodeDataType(s.type, None) for i, s in enumerate(node.in_streams)},
        PortType.output: {i: NodeDataType(s.type, None) for i, s in enumerate(node.out_streams)},
    }
    if not isinstance(node, ContainerInput):
        data_type[PortType.input][len(node.in_streams)] = NodeDataType("stream", "free")
    return type(
        f"{node.__class__.__name__}Widget",
        (AssemblyGraphNode,),
        {
            "name": node.__class__.__name__,
            "num_ports": {
                PortType.input: len(data_type[PortType.input]),
                PortType.output: len(data_type[PortType.output]),
            },
            "data_type": data_type,
        },
    )
