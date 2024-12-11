#!/usr/bin/env python3

"""Allow to view and edit the assembly graph with a ``block`` view."""

import logging
import pathlib
import typing

from qtpy import QtCore, QtWidgets
from qtpynodeeditor.connection_graphics_object import ConnectionGraphicsObject
from qtpynodeeditor.enums import PortType
from qtpynodeeditor.node_data import NodeDataModel, NodeDataType
from qtpynodeeditor.node_graphics_object import NodeGraphicsObject
from qtpynodeeditor.type_converter import TypeConverter
import qtpynodeeditor

from cutcutcodec.core.compilation.tree_to_graph import new_node
from cutcutcodec.core.edit.operation.add import add_edge, add_node
from cutcutcodec.core.edit.operation.remove import remove_elements
from cutcutcodec.core.exceptions import DecodeError
from cutcutcodec.core.io import read
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.edit_node_state.main import EditNodeWindow
from cutcutcodec.gui.flowchart.edge_properties import edge_properties
from cutcutcodec.gui.flowchart.node import meta_node_creator


class FlowScene(CutcutcodecWidget, qtpynodeeditor.FlowScene):
    """Able more acurate control on certain actions."""

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent
        self.qtnode_to_name = {}  # to each graphic node, associate the node name

    def create_complete_node(
        self, data_model: NodeDataModel, name: str
    ) -> qtpynodeeditor.node.Node:
        """Add a graphical node to the scene.

        Parameters
        ----------
        data_model : NodeDataModel
            The description class of the node.
        name : str
            The name of the node in the app tree.
        """
        assert isinstance(name, str), name.__class__.__name__
        assert name in self.app.graph
        data_model.name = name
        self.registry.register_model(data_model, category="")
        node = super().create_node(data_model)
        self.qtnode_to_name[node] = name
        return node

    def create_connection(
        self,
        port_a: qtpynodeeditor.port.Port,
        port_b: typing.Optional[qtpynodeeditor.port.Port] = None,
        *, converter: typing.Optional[qtpynodeeditor.type_converter.TypeConverter] = None,
        check_cycles=True
    ) -> qtpynodeeditor.connection.Connection:
        """Add the tool tip to the complete connection."""
        connection = super().create_connection(
            port_a, port_b, converter=converter, check_cycles=check_cycles
        )
        if not connection.is_complete:
            return connection

        dst_ind, src_ind = connection.ports
        src_ind, dst_ind = src_ind.index, dst_ind.index
        node_src = self.qtnode_to_name[connection.output_node]
        node_dst = self.qtnode_to_name[connection.input_node]
        edge_name = (node_src, node_dst, f"{src_ind}->{dst_ind}")

        for item in self.items():
            if isinstance(item, qtpynodeeditor.connection_graphics_object.ConnectionGraphicsObject):
                if item.connection is connection:
                    item.setToolTip(edge_properties(self, edge_name))
                    break
        else:
            raise RuntimeError(f"connection {connection} not found in the scene")

        return connection

    def remove_node(self, node: qtpynodeeditor.node.Node):
        """Keep updated the node traduction table."""
        del self.qtnode_to_name[node]
        super().remove_node(node)


class FlowView(CutcutcodecWidget, qtpynodeeditor.FlowView):
    """Change the default menu, manage drag and drop an element deletion."""

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent=parent)
        self._parent = parent
        self.setAcceptDrops(True)

    def generate_context_menu(self, pos: QtCore.QPoint):
        """Skip the menu creation."""
        menu = QtWidgets.QMenu()
        return menu

    def delete_selected(self):
        """Delete the selected elements."""
        elements = []
        for item in self._scene.selectedItems():
            if isinstance(item, ConnectionGraphicsObject):
                dst, src = item.connection.ports
                edge_name = (
                    self.scene.qtnode_to_name[item.connection.output_node],
                    self.scene.qtnode_to_name[item.connection.input_node],
                    f"{src.index}->{dst.index}",
                )
                elements.append(edge_name)
            if isinstance(item, NodeGraphicsObject):
                elements.append(self.scene.qtnode_to_name[item.node])

        backup_graph = self.app.graph.copy()
        trans = remove_elements(self.app.graph, elements)
        try:
            self.app.tree()
        except AssertionError as err:
            self.app.graph = backup_graph
            QtWidgets.QMessageBox.warning(
                None, "Deletion not permitted", f"Unable to delete {elements} : {err}"
            )
        else:
            for element, action in trans.items():
                if action is None:
                    print(f"delete {element}")
                else:
                    print(f"rename {element} to {action}")
            self.main_window.refresh()

    def dragEnterEvent(self, event):
        """Drag and drop selection."""
        if not event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            # case drag from file manager
            if not event.mimeData().hasFormat("text/plain") or not event.mimeData().hasUrls():
                logging.error("drag-and-drop failed (no text)")
                event.ignore()
                return
            for url in event.mimeData().urls():
                url_str = url.toString()
                if not url_str.startswith("file:"):
                    logging.error("drag-and-drop failed (not file %s)", url_str)
                    continue
                path = pathlib.Path(url_str[5:])
                if not path.is_file():
                    logging.error("drag-and-drop failed (not file exists %s)", path)
                    continue
                if self.app.global_vars.get("drag_an_drop", None) is not None:
                    logging.error("drag-and-drop ignore %s (only one file accepted)", path)
                    continue
                try:
                    container_input = read(path)
                except DecodeError as err:
                    logging.error("drag-and-drop failed (%s)", err)
                    continue
                self.app.global_vars["drag_an_drop"] = new_node(self.app.graph, container_input)
                break

        if self.app.global_vars.get("drag_an_drop", None) is None:
            event.ignore()
            return
        event.accept()

    def dropEvent(self, _):
        """Drag and drop management."""
        # creation of the new node in the main graph
        node_name, attrs = self.app.global_vars["drag_an_drop"]
        self.app.global_vars["drag_an_drop"] = None
        add_node(self.app.graph, node_name, attrs)
        print(f"create {node_name}")

        # very light graphical update, beter than self.parent.refresh()
        node_cls_widget = meta_node_creator(self.app.tree_node(node_name))
        self.scene.create_complete_node(node_cls_widget, node_name)

    def dragMoveEvent(self, event):
        """Need to be defined for calling ``dropEvent``."""


class FlowChart(CutcutcodecWidget, QtWidgets.QWidget):
    """Nodes graph viewer."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        registry = qtpynodeeditor.DataModelRegistry()
        audio_converter = TypeConverter(
            NodeDataType("audio", None), NodeDataType("stream", "free"), lambda d: d
        )
        registry.register_type_converter(
            NodeDataType("audio", None), NodeDataType("stream", "free"), audio_converter
        )
        video_converter = TypeConverter(
            NodeDataType("video", None), NodeDataType("stream", "free"), lambda d: d
        )
        registry.register_type_converter(
            NodeDataType("video", None), NodeDataType("stream", "free"), video_converter
        )

        self.scene = FlowScene(parent=self, registry=registry)
        self.scene.style_collection.connection.use_data_defined_colors = True
        self.scene.connection_created.connect(self.connection_created)
        self.scene.node_double_clicked.connect(self.node_double_clicked)
        self.scene.node_moved.connect(self.node_moved)
        self.view = FlowView(self.scene, parent=self)

        self.edge_prop_win = {}  # the popup edge properties window

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def connection_created(self, connection: qtpynodeeditor.connection.Connection):
        """Help when called when a connection has just been created."""
        dst_ind, src_ind = connection.ports
        src_ind, dst_ind = src_ind.index, dst_ind.index
        node_src = self.scene.qtnode_to_name[connection.output_node]
        node_dst = self.scene.qtnode_to_name[connection.input_node]
        edge_name = (node_src, node_dst, f"{src_ind}->{dst_ind}")
        if edge_name not in self.app.graph.edges:
            backup_graph = self.app.graph.copy()
            add_edge(self.app.graph, node_src, node_dst, src_ind)
            try:
                self.app.tree()
            except AssertionError as err:
                self.app.graph = backup_graph
                self.scene.delete_connection(connection)
                QtWidgets.QMessageBox.warning(
                    None, "Creation not permitted", f"Unable to create {edge_name} : {err}"
                )
            else:
                print(f"create {edge_name}")
                self.main_window.refresh()

    def node_double_clicked(self, qtnode: qtpynodeeditor.node.Node):
        """Open the node edition window."""
        name = self.scene.qtnode_to_name[qtnode]
        graph_win = EditNodeWindow(self, name)
        graph_win.exec()

    def node_moved(self, node: qtpynodeeditor.node.Node):
        """Record the new position of the node."""
        position = [node.position.x(), node.position.y()]
        prop = self.app.graph.nodes[self.scene.qtnode_to_name[node]]
        prop["display"] = prop.get("display", {})
        prop["display"]["position"] = position

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        # remove all the widgets on the scene
        self.scene.clear_scene()

        # the nodes
        for node_name in self.app.graph.nodes:
            node_cls_widget = meta_node_creator(self.app.tree_node(node_name))
            node = self.scene.create_complete_node(node_cls_widget, node_name)
            prop = self.app.graph.nodes(data=True)[self.scene.qtnode_to_name[node]]
            try:
                node.position = prop["display"]["position"]
            except KeyError:
                pass

        # the edges
        name_to_qtnode = {n: q for q, n in self.scene.qtnode_to_name.items()}
        for src, dst, key in self.app.graph.edges:
            src_ind, dst_ind = key.split("->")
            src_ind, dst_ind = int(src_ind), int(dst_ind)
            self.scene.create_connection(
                name_to_qtnode[src][PortType.output][src_ind],
                name_to_qtnode[dst][PortType.input][dst_ind],
            )
