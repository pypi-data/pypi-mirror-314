#!/usr/bin/env python3

"""Properties that are common to all nodes."""

from qtpy import QtWidgets

from cutcutcodec.core.classes.container import ContainerInput, ContainerOutput
from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.gui.edit_node_state.base import EditBase


class General(EditBase):
    """Display the node documentation."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_type(grid_layout)
        ref_span = self.init_ancestors(grid_layout, ref_span)
        self.init_streams(grid_layout, ref_span)
        self.setLayout(grid_layout)

    def init_streams(self, grid_layout, ref_span=0):
        """Give some informations about streams."""
        in_streams = sorted(
            self.app.graph.in_edges(self.node_name, data=False, keys=True),
            key=lambda src_dst_key: int(src_dst_key[2].split("->")[1])
        )
        out_streams = sorted(
            self.app.graph.out_edges(self.node_name, data=False, keys=True),
            key=lambda src_dst_key: int(src_dst_key[2].split("->")[0])
        )
        for streams, label in zip((in_streams, out_streams), ("Incoming", "Output")):
            if streams:
                grid_layout.addWidget(QtWidgets.QLabel(f"{label} Streams:"), ref_span, 0)
                for i, (src, dst, key) in enumerate(streams):
                    key = key.split('->')
                    grid_layout.addWidget(
                        QtWidgets.QLabel(
                            f"{src} (stream {key[0]}) -> {dst} (stream {key[1]})"
                        ),
                        ref_span+i,
                        1,
                    )
                ref_span += len(in_streams)
        return ref_span

    def init_ancestors(self, grid_layout, ref_span=0):
        """Return the inheritance of classes from the main type."""
        ancestors = " <-- ".join(c.__name__ for c in self.get_class().__mro__[-2::-1])
        grid_layout.addWidget(QtWidgets.QLabel("Ancestors:"), ref_span, 0)
        grid_layout.addWidget(QtWidgets.QLabel(ancestors), ref_span, 1)
        ref_span += 1
        return ref_span

    def init_type(self, grid_layout, ref_span=0):
        """Return the generique type of node."""
        if issubclass(self.get_class(), ContainerInput):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Input"), ref_span, 1)
            ref_span += 1
        elif issubclass(self.get_class(), ContainerOutput):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Output"), ref_span, 1)
            ref_span += 1
        elif issubclass(self.get_class(), Filter):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Filter"), ref_span, 1)
            ref_span += 1
        return ref_span
