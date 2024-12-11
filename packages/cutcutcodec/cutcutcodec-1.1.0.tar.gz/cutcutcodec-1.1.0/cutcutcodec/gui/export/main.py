#!/usr/bin/env python3

"""Interactive window for help to choose the export settings."""

import pathlib

from qtpy import QtWidgets

from cutcutcodec.core.compilation.export.default import suggest_export_params
from cutcutcodec.core.compilation.tree_to_graph import tree_to_graph
from cutcutcodec.core.exceptions import IncompatibleSettings
from cutcutcodec.core.io.write import ContainerOutputFFMPEG
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.export.container import ContainerSettings
from cutcutcodec.gui.export.encodec import EncoderSettings
from cutcutcodec.gui.tools import WaitCursor


class WindowsExportSettings(CutcutcodecWidget, QtWidgets.QDialog):
    """Show the exportation settings."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.encoders_widgets = []

        with WaitCursor(self.main_window):
            self._container_settings = ContainerSettings(self)
            self.encoders_widgets = [
                EncoderSettings(self, stream) for stream in self.app.tree().in_streams
            ]

            self.setWindowTitle("Export settings")

            # simplified configuration
            simplified_tab = QtWidgets.QWidget()
            simplified_layout = QtWidgets.QVBoxLayout()
            simplified_layout.addWidget(
                QtWidgets.QLabel("Not yet implemented, Please go in 'Advanced Settings' tab.")
            )
            simplified_tab.setLayout(simplified_layout)

            # advanced settings
            advanced_tab = QtWidgets.QWidget()
            advanced_layout = QtWidgets.QVBoxLayout()
            advanced_layout.addWidget(self._container_settings)
            advanced_streams_w = QtWidgets.QWidget()
            advanced_layout_streams = QtWidgets.QHBoxLayout()
            advanced_streams_w.setLayout(advanced_layout_streams)
            for i, encoder in enumerate(self.encoders_widgets):
                if i:
                    separador = QtWidgets.QFrame()
                    separador.setFrameShape(QtWidgets.QFrame.Shape.VLine)
                    advanced_layout_streams.addWidget(separador)
                advanced_layout_streams.addWidget(encoder)
            advanced_layout.addWidget(advanced_streams_w)
            advanced_tab.setLayout(advanced_layout)

            # positioning of the widgets
            tabs = QtWidgets.QTabWidget()
            tabs.addTab(simplified_tab, "Simplifed Configuration")
            tabs.addTab(advanced_tab, "Advanced Settings")
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(tabs)
            self.init_next(layout)
            self.setLayout(layout)

            self.refresh()

    def export(self):
        """Complete the job or the next step in the main pipeline."""
        self.accept()
        streams = self.app.tree().in_streams

        # conversion of supplied parameters
        filename = (
            pathlib.Path(self.app.export_settings["parent"]) / self.app.export_settings["stem"]
        )

        indexs = {}
        streams_settings = []
        for stream in streams:
            index = indexs.get(stream.type, -1) + 1
            indexs[stream.type] = index
            streams_settings.append({
                "encodec": self.app.export_settings["encoders"][stream.type][index],
                "options": self.app.export_settings["encoders_settings"][stream.type][index],
            })
            if streams_settings[-1]["encodec"] is None:
                streams_settings[-1]["encodec"] = (
                    self.app.export_settings["codecs"][stream.type][index]
                )
            if stream.type == "audio":
                streams_settings[-1]["rate"] = self.app.export_settings["rates"]["audio"][index]
                streams_settings[-1]["bitrate"] = (
                    self.app.export_settings["bitrate"]["audio"][index]
                )
            elif stream.type == "video":
                streams_settings[-1]["rate"] = self.app.export_settings["rates"]["video"][index]
                streams_settings[-1]["shape"] = self.app.export_settings["shapes"][index]
                streams_settings[-1]["bitrate"] = (
                    self.app.export_settings["bitrate"]["video"][index]
                )
                streams_settings[-1]["pix_fmt"] = self.app.export_settings["pix_fmt"][index]
            else:
                raise TypeError(f"not yet supported {stream.type}")

        container_settings = {
            "format": self.app.export_settings["muxer"],
            "container_options": self.app.export_settings["muxer_settings"],
        }

        # completes the missing parameters
        try:
            filename, streams_settings, container_settings = suggest_export_params(
                streams,
                filename=filename,
                streams_settings=streams_settings,
                container_settings=container_settings,
            )
        except IncompatibleSettings as err:
            QtWidgets.QMessageBox.warning(None, "Incompatible Parameters", str(err))

        # transmission of the information for next steps
        tree = ContainerOutputFFMPEG(
            streams,
            filename=filename,
            streams_settings=streams_settings,
            container_settings=container_settings,
        )
        self.main_window.output.put_nowait({
            "graph": tree_to_graph(tree),
            "optimize": self.app.export_settings["optimize"],
            "excecute": self.app.export_settings["excecute"],
            "filename": (
                pathlib.Path(self.app.export_settings["parent"]) / self.app.export_settings["stem"]
            )
        })

        # close
        self.main_window.close()

    def init_next(self, layout):
        """Return the button for the next stape."""

        def set_optimize(state):
            self.app.export_settings["optimize"] = bool(state)

        def set_excecute(state):
            self.app.export_settings["excecute"] = bool(state)

        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)
        optimize = QtWidgets.QCheckBox("Optimize the graph.")
        optimize.setChecked(self.app.export_settings["optimize"])
        optimize.stateChanged.connect(set_optimize)
        layout.addWidget(optimize)
        excecute = QtWidgets.QCheckBox("Excecute the generated code.")
        excecute.setChecked(self.app.export_settings["excecute"])
        excecute.stateChanged.connect(set_excecute)
        layout.addWidget(excecute)
        button = QtWidgets.QPushButton("Let's Go!")
        button.setAutoDefault(False)
        button.clicked.connect(self.export)
        layout.addWidget(button)

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        with WaitCursor(self):
            self._container_settings.refresh()
            for enc in self.encoders_widgets:
                enc.refresh()
