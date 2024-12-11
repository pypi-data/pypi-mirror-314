#!/usr/bin/env python3

"""Properties of a ``cutcutcodec.core.filter.basic.cut.FilterCut``."""

from fractions import Fraction

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase


class EditFilterCut(EditBase):
    """Allow to view and modify the properties of a filter of type ``FilterCut``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)

        self.limit_textboxs = self.limit_labels = None

        self.grid_layout = QtWidgets.QGridLayout()
        self.init_limit(self.grid_layout)
        self.setLayout(self.grid_layout)

    def init_limit(self, grid_layout, ref_span=0):
        """Display and allows to modify the limits."""
        class _Val:

            def __init__(self, limit_index, window):
                self.limit_index = limit_index
                self.window = window

            def __call__(self, text):
                return self.window.update_limit(text, self.limit_index)

            def __repr__(self):  # for remove pylint R0903
                return f"verification limit {self.limit_index}"
        limits = self.state["limits"] + [""]
        self.limit_labels = [QtWidgets.QLabel(f"Limit {i} (second)") for i in range(len(limits))]
        self.limit_textboxs = [None for _ in limits]
        for i, limit in enumerate(limits):
            self.limit_textboxs[i] = QtWidgets.QLineEdit()
            self.limit_textboxs[i].setText(str(limit))
            self.limit_textboxs[i].textEdited.connect(_Val(i, self))
            grid_layout.addWidget(self.limit_labels[i], ref_span, 0)
            grid_layout.addWidget(self.limit_textboxs[i], ref_span, 1)
            ref_span += 1
        return ref_span

    def update_limit(self, text, limit_index):
        """Check that the limit is correct and update all the limits."""
        changed = False
        if not text and limit_index >= 1 and limit_index + 1 == len(self.state["limits"]):
            changed = True
            new_limits = self.state["limits"][:limit_index]
        else:
            try:
                limit = Fraction(text)
            except (ValueError, ZeroDivisionError):
                self.limit_textboxs[limit_index].setStyleSheet("background:red;")
                return
            new_limits = self.state["limits"].copy()
            if limit_index < len(new_limits):
                new_limits[limit_index] = str(limit)
            else:
                changed = True
                new_limits.append(str(limit))
            limits = list(map(Fraction, new_limits))
            if sorted(limits) != limits or len(set(limits)) != len(limits):
                self.limit_textboxs[limit_index].setStyleSheet("background:red;")
                return

        def setter(limits):
            self.state["limits"] = limits

        self.try_set_state(
            self.get_updated_state((lambda: self.state["limits"]), setter, new_limits)
        )
        if changed:  # redraw the limits fields
            for widget in self.limit_textboxs + self.limit_labels:
                if widget is not None:
                    widget.deleteLater()
            self.init_limit(self.grid_layout)
