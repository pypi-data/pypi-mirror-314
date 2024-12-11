#!/usr/bin/env python3

"""Allow to avoid redundancy in the node editing windows.

Defines several accessors that allow to lighten the code of child classes.
This is also where methods common to several classes are implemented to avoid data redundancy.
"""

import math
import numbers
import re
import typing

from qtpy import QtWidgets

from cutcutcodec.core.classes.layout import AllLayouts, Layout
from cutcutcodec.core.compilation.parse import parse_to_number
from cutcutcodec.core.compilation.parse import parse_to_sympy
from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.preferences.video_settings import CLASSICAL_SHAPES, _format_shape


class AudioLayoutable:
    """Allow to select an audio layout."""

    def __init__(self, edit: EditBase, enable_default=True):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "layout" in edit.state, sorted(edit.state)
        assert isinstance(enable_default, bool), enable_default.__class__.__name__
        self.edit = edit
        self.edit.ref.append(self)
        self.combobox = QtWidgets.QComboBox(edit)
        self.enable_default = enable_default

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to select the layout field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel("Audio layout:", self.edit), ref_span, 0)
        self.combobox.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.combobox.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

        if self.enable_default:
            self.combobox.addItem("default")
        layouts = AllLayouts().layouts
        defaults = (
            {Layout(nb_channels).name for nb_channels in set(map(len, layouts.values()))}
        )
        for layout in sorted(layouts, key=lambda p: (len(layouts[p]), (p not in defaults), p)):
            if layout in defaults:
                item = (
                    f'{len(layouts[layout])} channels default "{layout}" '
                    f"({'+'.join(layouts[layout])})"
                )
            else:
                item = (
                    f'{len(layouts[layout])} channels "{layout}" ({"+".join(layouts[layout])})'
                )
            self.combobox.addItem(item)
            if self.edit.state["layout"] == layout:
                self.combobox.setCurrentText(item)
        self.combobox.currentTextChanged.connect(self.validate)

        grid_layout.addWidget(self.combobox, ref_span, 1)
        return ref_span + 1

    def validate(self, text):
        """Check and updates the audio layout."""
        old_layout = self.edit.state["layout"]
        new_layout = None if text == "default" else re.search(r'".+"', text).group()[1:-1]
        if new_layout != old_layout:
            if "signals" in self.edit.state:
                signals = self.edit.state["signals"]
                layout = Layout(new_layout or len(signals))
                signals = (
                    signals + ["0"]*(len(layout.channels)-len(signals))
                )[:len(layout.channels)]
                self.edit.try_set_state(
                    self.edit.get_updated_state_dict({"layout": new_layout, "signals": signals})
                )
            else:
                self.edit.try_set_state(self.edit.get_updated_state_dict({"layout": new_layout}))
            if hasattr(self.edit, "reset"):
                self.edit.reset()


class Booleanable:
    """Allow to manage a boolean field."""

    def __init__(self, edit: EditBase, var: str, label: str):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert var in edit.state, (var, sorted(edit.state))
        assert isinstance(label, str), label.__class__.__name__
        self.edit = edit
        self.var = var
        self.label = label
        self.edit.ref.append(self)
        self.checkbox = QtWidgets.QCheckBox(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify the seed field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel(self.label, self.edit), ref_span, 0)
        self.checkbox.stateChanged.connect(self.validate)
        self.checkbox.setChecked(self.edit.state[self.var])
        grid_layout.addWidget(self.checkbox, ref_span, 1)
        return ref_span + 1

    def validate(self, check: int):
        """Change the boolean value."""
        self.edit.try_set_state(self.edit.get_updated_state_dict({self.var: bool(check)}))


class Equationable:
    """Allow to manage a list of sympy equation."""

    def __init__(self, edit: EditBase, pos_state: tuple[int, str], label: str, re_symb=str):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert isinstance(pos_state, tuple), pos_state.__class__.__name__
        assert len(pos_state) == 2, pos_state
        position, state = pos_state
        assert isinstance(position, int), position.__class__.__name__
        assert position >= 0, position
        assert isinstance(state, str), state
        assert state in edit.state
        assert isinstance(edit.state[state], list), edit.state.__class__.__name__
        assert isinstance(label, str), label.__class__.__name__
        assert isinstance(re_symb, str), re_symb.__class__.__name__
        if len(edit.state[state]) < position:
            edit.state[state].extend(["0"]*(position-len(edit.state[state])))
        self.edit = edit
        self.position = position
        self.state = state
        self.label = QtWidgets.QLabel(label)
        self.re_symb = re_symb
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify an equation field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(self.label, ref_span, 0)
        if len(self.edit.state[self.state]) > self.position:
            self.textbox.setText(str(self.edit.state[self.state][self.position]))
        self.textbox.editingFinished.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def delete(self):
        """Delete the widgets."""
        self.label.deleteLater()
        self.textbox.deleteLater()

    def validate(self, text=None):
        """Check and updates the new equation."""
        text = text or self.textbox.text()
        eqs = self.edit.state[self.state].copy()
        reset = False
        if text:
            try:
                expr = parse_to_sympy(text)
            except (SyntaxError, ZeroDivisionError):
                self.textbox.setStyleSheet("background:red;")
                return
            for symb in map(str, expr.free_symbols):
                if not re.fullmatch(self.re_symb, symb):
                    self.textbox.setStyleSheet("background:red;")
                    return
            if self.position == len(eqs):
                eqs.append(str(expr))
                reset = True
            else:
                eqs[self.position] = str(expr)
        elif len(eqs) - 1 == self.position:
            if self.position == 0:
                self.textbox.setStyleSheet("background:red;")
                return
            del eqs[self.position]
            reset = True
        else:
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_updated_state_dict({self.state: eqs}), self.textbox)
        if reset:
            self.edit.reset()


class Numerable:
    """Allow to manage a number field to extract a fraction or or inf."""

    def __init__(
        self,
        edit: EditBase,
        state: str,
        bounds: tuple[numbers.Real, numbers.Real] = (-math.inf, math.inf),
        isfinite: bool = False,
    ):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert isinstance(state, str), state.__class__.__name__
        assert state in edit.state, f"{state} not in {sorted(edit.state)}"
        assert isinstance(bounds, tuple), bounds.__class__.__name__
        assert len(bounds) == 2, bounds
        assert isinstance(bounds[0], numbers.Real), bounds[0].__class__.__name__
        assert isinstance(bounds[1], numbers.Real), bounds[1].__class__.__name__
        assert bounds[0] < bounds[1], bounds
        assert isinstance(isfinite, bool), isfinite.__class__.__name__
        self.edit = edit
        self.edit.ref.append(self)
        self.state = state
        self.bounds = bounds
        self.isfinite = isfinite
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify the number field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(
            QtWidgets.QLabel(
                f"{self.state.replace('_', ' ').title()} "
                f"({self.bounds[0]} {'<=' if math.isfinite(self.bounds[0]) else '<'} "
                "number "
                f"{'<=' if math.isfinite(self.bounds[1]) else '<'} {self.bounds[1]}):",
                self.edit,
            ),
            ref_span,
            0,
        )
        self.textbox.setText(str(self.edit.state[self.state]))
        self.textbox.editingFinished.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def validate(self, text=None):
        """Check and updates the new number."""
        text = text or self.textbox.text()
        try:
            val = parse_to_number(text)
        except (ValueError, ZeroDivisionError):
            self.textbox.setStyleSheet("background:red;")
            return
        if val < self.bounds[0] or val > self.bounds[1]:
            self.textbox.setStyleSheet("background:red;")
            return
        if self.isfinite and not math.isfinite(val):
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(
            self.edit.get_updated_state_dict({self.state: str(val)}),
            self.textbox,
        )


class Seedable:
    """Allow to manage a `seed` field.

    It is a float between [0, 1[.
    """

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "seed" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify the seed field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel("Seed (0 <= float < 1):", self.edit), ref_span, 0)
        self.textbox.setText(str(self.edit.state["seed"]))
        self.textbox.editingFinished.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def validate(self, text=None):
        """Check and updates the new seed."""
        text = text or self.textbox.text()
        try:
            seed = float(text)
        except ValueError:
            self.textbox.setStyleSheet("background:red;")
            return
        if seed < 0 or seed >= 1:
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_updated_state_dict({"seed": seed}), self.textbox)


class Shapeable:
    """Allow to manage a `shape` field."""

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "shape" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.textbox = QtWidgets.QLineEdit(edit)
        self.combobox = QtWidgets.QComboBox(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify the shape field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        # textbox
        grid_layout.addWidget(QtWidgets.QLabel("Shape:", self.edit), ref_span, 0)
        self.textbox.editingFinished.connect(self.validate)
        self.textbox.setPlaceholderText("width x height")
        self.textbox.setText("x".join(map(str, self.edit.state["shape"][::-1])))  # h*w to w*h
        grid_layout.addWidget(self.textbox, ref_span, 1)
        # combobox
        self.combobox.textActivated.connect(self.select_shape)
        self.combobox.addItem("manual")
        self.combobox.addItems(map(_format_shape, sorted(CLASSICAL_SHAPES)))
        grid_layout.addWidget(self.combobox, ref_span+1, 1)
        return ref_span + 2

    def select_shape(self, text: str):
        """Change the shape given by the combobox."""
        if text == "manual":
            text = "x".join(map(str, self.edit.state["shape"][::-1]))
        self.validate(text)

    def validate(self, text=None):
        """Check and updates the new seed."""
        text = text or self.textbox.text()
        shape = tuple(map(int, re.findall(r"\d+", text)))[1::-1]
        if len(shape) != 2 or shape[0] <= 0 or shape[1] <= 0:
            self.textbox.setStyleSheet("background:red;")
            return
        if shape in CLASSICAL_SHAPES:
            self.combobox.setCurrentText(_format_shape(shape))
        else:
            self.combobox.setCurrentText("manual")
        self.edit.try_set_state(self.edit.get_updated_state_dict({"shape": list(shape)}))


class SingleEq:
    """Allow to manage a single sympy equation field."""

    def __init__(
        self,
        edit: EditBase,
        getter_setter: tuple[typing.Callable, typing.Callable],
        label: str,
        re_symb=str,
    ):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert isinstance(getter_setter, tuple), getter_setter.__class__.__name__
        assert len(getter_setter) == 2, getter_setter
        getter, setter = getter_setter
        assert hasattr(getter, "__call__"), getter.__class__.__name__
        assert hasattr(setter, "__call__"), setter.__class__.__name__
        assert isinstance(getter(), str), getter().__class__.__name__
        assert isinstance(label, str), label.__class__.__name__
        assert isinstance(re_symb, str), re_symb.__class__.__name__

        self.edit = edit
        self.edit.ref.append(self)
        self.getter = getter
        self.setter = setter
        self.label = QtWidgets.QLabel(label)
        self.re_symb = re_symb
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """Display and allows to modify an equation field."""
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(self.label, ref_span, 0)
        self.textbox.setText(self.getter())
        self.textbox.editingFinished.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def validate(self, text=None):
        """Check and updates the new equation."""
        text = text or self.textbox.text()
        try:
            expr = parse_to_sympy(text)
        except (SyntaxError, ZeroDivisionError):
            self.textbox.setStyleSheet("background:red;")
            return
        for symb in map(str, expr.free_symbols):
            if not re.fullmatch(self.re_symb, symb):
                self.textbox.setStyleSheet("background:red;")
                return
        self.edit.try_set_state(
            self.edit.get_updated_state(self.getter, self.setter, text),
            self.textbox,
        )
