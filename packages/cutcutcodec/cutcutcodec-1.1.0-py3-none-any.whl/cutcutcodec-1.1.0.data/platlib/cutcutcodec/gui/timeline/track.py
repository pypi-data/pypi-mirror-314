#!/usr/bin/env python3

"""A single track in the timeline."""

import math

from qtpy import QtCore, QtGui, QtWidgets
from qtpynodeeditor.style import NodeStyle

from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.core.classes.node import Node


class Track(CutcutcodecWidget, QtWidgets.QGraphicsItem):
    """Representation of the stream of a node."""

    def __init__(self, parent, node: Node):
        super().__init__()
        self._parent = parent
        self.node = node

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemDoesntPropagateOpacityToChildren, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemContainsChildrenInShape, True)  # for optimisation
        # self.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges, True)

        self.is_hovered = False

    def boundingRect(self) -> QtCore.QRectF:
        """Return the complete bounding rect of the node."""
        beginning = self.node.in_streams[0].beginning
        duration = self.node.in_streams[0].duration
        (t_min, t_max), _ = self.parent.viewRange()
        x_min, x_max = self.parent.sceneRect().left(), self.parent.sceneRect().right()
        ratio = (x_max-x_min) / (t_max-t_min)
        left = x_min + ratio * (beginning-t_min)
        width = x_min + ratio * duration
        if width == math.inf:
            width = max(x_max-x_min, x_max-left)
        boundary = QtCore.QRectF(left, 30, width, 70)
        return boundary

    def hoverEnterEvent(self, event):
        """When the mouse comes in the rectangle."""
        self.is_hovered = True
        event.accept()
        self.update()

    def hoverLeaveEvent(self, event):
        """When the mouse leave the rectangle."""
        self.is_hovered = False
        event.accept()
        self.update()

    def paint(self, painter: QtGui.QPainter, *_):
        """Draw the track."""
        boundary = self.boundingRect()

        # draw the main rectangle
        color = (
            NodeStyle().selected_boundary_color
            if self.isSelected()
            else NodeStyle().normal_boundary_color
        )
        style = NodeStyle().hovered_pen_width if self.is_hovered else NodeStyle().pen_width
        pen = QtGui.QPen(color, style)
        painter.setPen(pen)
        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(0.0, 0.0), QtCore.QPointF(2.0, boundary.height())
        )
        for at_, color in NodeStyle().gradient_colors:
            gradient.setColorAt(at_, color)
        painter.setBrush(gradient)
        radius = 3.0
        painter.drawRoundedRect(boundary, radius, radius)

        # draw the node name
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(NodeStyle().font_color)
        painter.drawText(boundary, "container output")
        font.setBold(False)
        painter.setFont(font)

    def update_node(self, new_node: Node):
        """Recompute the complete new tree from the given node."""
        self.node = new_node
        # for item in self.childItems():
        #     print(item, "todelete")
        # for stream in self.node.in_streams:
        #     child_track = Track(self.parent, stream.node_main)
        #     child_track.setParentItem(self)
        #     self.scene().addItem(child_track)
