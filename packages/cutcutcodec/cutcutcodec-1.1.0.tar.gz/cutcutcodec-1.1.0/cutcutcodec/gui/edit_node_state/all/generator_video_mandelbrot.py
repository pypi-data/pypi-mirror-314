#!/usr/bin/env python3

"""Props of ``cutcutcodec.core.generation.video.fractal.mandelbrot.GeneratorVideoMandelbrot``."""

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import SingleEq


class EditGeneratorVideoMandelbrot(EditBase):
    """View and modify the properties of a generator of type ``GeneratorVideoMandelbrot``."""

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        grid_layout = QtWidgets.QGridLayout()

        class _Getter:

            def __init__(self, state, name):
                self.state = state
                self.name = name

            def __call__(self):
                return self.state["bounds"][self.name]

            def __repr__(self):
                return f"{self.name} bounds getter"

        class _Setter:

            def __init__(self, state, name):
                self.state = state
                self.name = name

            def __call__(self, value):
                self.state["bounds"][self.name] = value

            def __repr__(self):
                return f"{self.name} bounds setter"

        ref_span = 0
        for name in self.state["bounds"]:
            ref_span = SingleEq(
                self,
                (_Getter(self.state, name), _Setter(self.state, name)),
                f"Expr of {name}:",
                r"t",
            )(grid_layout, ref_span=ref_span)

        def setter_iters(value):
            self.state["iterations"] = value

        SingleEq(
            self,
            ((lambda: self.state["iterations"]), setter_iters),
            "Iterations Max:",
            r"t"
        )(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)
