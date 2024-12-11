#!/usr/bin/env python3

"""Interactive widget for help to choose the export codecs/encoders settings."""

from fractions import Fraction

from qtpy import QtCore, QtWidgets

from cutcutcodec.core.classes.encoder import AllEncoders
from cutcutcodec.core.classes.encoder import Encoder
from cutcutcodec.core.classes.muxer import AllMuxers
from cutcutcodec.core.compilation.export.compatibility import Compatibilities
from cutcutcodec.core.compilation.parse import parse_to_number
from cutcutcodec.gui.base import CutcutcodecWidget
from cutcutcodec.gui.export._helper import ComboBox
from cutcutcodec.gui.export.doc import DocViewer
from cutcutcodec.gui.preferences.audio_settings import PreferencesAudio
from cutcutcodec.gui.preferences.video_settings import PreferencesVideo


class BitRateSelector(CutcutcodecWidget, QtWidgets.QLineEdit):
    """Configure the bitrate of one stream."""

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.textEdited.connect(self._validate_flow)

    def _validate_flow(self, text):
        """Ensure the bitrate is correct."""
        if text == "":
            self.app.export_settings["bitrate"][self.parent.stream.type][self.parent.index] = None
            self.setStyleSheet("background:none;")
            return
        try:
            bitrate = round(parse_to_number(text))
        except ValueError:
            self.setStyleSheet("background:red;")
            return
        if bitrate < 0:
            self.setStyleSheet("background:red;")
            return
        self.app.export_settings["bitrate"][self.parent.stream.type][self.parent.index] = text
        self.setStyleSheet("background:none;")

    def refresh(self):
        """Write in the box the recorded value."""
        bitrate = self.app.export_settings["bitrate"][self.parent.stream.type][self.parent.index]
        if bitrate is None:
            self.setText("")
        else:
            self.setText(bitrate)
        self.setStyleSheet("background:none;")


class CodecComboBox(ComboBox):
    """Lists the availables codecs."""

    def _text_changed(self, name: str):
        if name == "default":
            name = None
        index = self.parent.index
        stream_type = self.parent.stream.type
        if self.app.export_settings["codecs"][stream_type][index] != name:
            self.app.export_settings["codecs"][stream_type][index] = name
            print(f"update codec (stream {stream_type} {index}): {name}")
            self.parent.widgets["encoder_combo_box"].text_changed("default")
            self.parent.parent.refresh()  # WindowsExportSettings

    def available_codecs(self) -> set[str]:
        """Set of codecs supporting for this streams.

        Takes in account the muxer and the stream type.
        """
        stream_type = self.parent.stream.type
        muxer = self.app.export_settings["muxer"]
        muxers = None if muxer is None else [muxer]
        if stream_type == "audio":
            return set(
                Compatibilities().codecs_audio(
                    muxers,  # we should to forward 'profile' as well
                    layout=self.parent.stream.layout.name,
                    rate=self.app.export_settings["rates"]["audio"][self.parent.index],
                )
            )
        if stream_type == "video":
            rate_json = self.app.export_settings["rates"]["video"][self.parent.index]
            return set(
                Compatibilities().codecs_video(
                    muxers,
                    shape=self.app.export_settings["shapes"][self.parent.index],
                    rate=(None if rate_json is None else Fraction(rate_json)),
                    pix_fmt=self.app.export_settings["pix_fmt"][self.parent.index],
                )
            )
        raise NotImplementedError(f"only available for audio and video, not for {stream_type}")

    def refresh(self):
        """Update the list with the available codecs."""
        self.clear()
        codec = self.app.export_settings["codecs"][self.parent.stream.type][self.parent.index]
        if codec is not None and codec not in self.available_codecs():
            self.text_changed("default")
            return
        self.addItem(codec or "default")
        for codec_ in [None] + sorted(self.available_codecs()):
            if codec_ == codec:
                continue
            self.addItem(codec_ or "default")


class EncoderComboBox(ComboBox):
    """Lists the availables encoders."""

    def _text_changed(self, name: str):
        if name == "default":
            name = None
        index = self.parent.index
        stream_type = self.parent.stream.type
        if self.app.export_settings["encoders"][stream_type][index] != name:
            self.app.export_settings["encoders"][stream_type][index] = name
            print(f"update encoder (stream {stream_type} {index}): {name}")
            self.parent.parent.refresh()  # WindowsExportSettings

    def available_encoders(self) -> set[str]:
        """Set of encoders supporting for this streams.

        The returned encoders are tested to ensure the compatibility with the muxer and the codec.
        """
        stream_type = self.parent.stream.type
        codec = self.app.export_settings["codecs"][stream_type][self.parent.index]
        muxer = self.app.export_settings["muxer"]
        muxers = [muxer] if muxer is not None else None

        if stream_type == "audio":
            if codec is None:
                encoders = sorted(AllEncoders().audio)
                comp = Compatibilities().check(  # we should to forward 'profile' as well
                    encoders, (muxers or sorted(AllMuxers().set)),
                    layout=self.parent.stream.layout.name,
                    rate=self.app.export_settings["rates"]["audio"][self.parent.index],
                )
                return {e for e, a in zip(encoders, (comp != "").any(axis=1)) if a}
            return set(
                Compatibilities().encoders_audio(
                    codec, muxers,  # we should to forward 'profile' as well
                    layout=self.parent.stream.layout.name,
                    rate=self.app.export_settings["rates"]["audio"][self.parent.index],
                )
            )
        if stream_type == "video":
            rate_json = self.app.export_settings["rates"]["video"][self.parent.index]
            if codec is None:
                encoders = sorted(AllEncoders().video)
                comp = Compatibilities().check(
                    encoders, (muxers or sorted(AllMuxers().set)),
                    shape=self.app.export_settings["shapes"][self.parent.index],
                    rate=(None if rate_json is None else Fraction(rate_json)),
                    pix_fmt=self.app.export_settings["pix_fmt"][self.parent.index],
                )
                return {e for e, a in zip(encoders, (comp != "").any(axis=1)) if a}
            return set(
                Compatibilities().encoders_video(
                    codec, muxers,
                    shape=self.app.export_settings["shapes"][self.parent.index],
                    rate=(None if rate_json is None else Fraction(rate_json)),
                    pix_fmt=self.app.export_settings["pix_fmt"][self.parent.index],
                )
            )
        raise NotImplementedError(f"only available for audio and video, not for {stream_type}")

    def refresh(self):
        """Update the list with the available encoders."""
        self.clear()
        encoder = self.app.export_settings["encoders"][self.parent.stream.type][self.parent.index]
        if encoder is not None and encoder not in self.available_encoders():
            self.text_changed("default")
            return
        self.addItem(encoder or "default")
        for encoder_ in [None] + sorted(self.available_encoders()):
            if encoder_ == encoder:
                continue
            self.addItem(encoder_ or "default")


class EncoderSettings(CutcutcodecWidget, QtWidgets.QWidget):
    """Able to choose and edit the encoder for a given stream."""

    def __init__(self, parent, stream):
        super().__init__(parent)
        self._parent = parent
        self.stream = stream

        self.widgets = {}
        self.widgets["preset"] = None
        self.widgets["codec_combo_box"] = CodecComboBox(self)
        self.widgets["encoder_label"] = QtWidgets.QLabel("Encoder:", self)
        self.widgets["encoder_label"].hide()
        self.widgets["encoder_combo_box"] = EncoderComboBox(self)
        self.widgets["encoder_combo_box"].hide()
        self.widgets["encoder_doc_viewer"] = DocViewer(
            self,
            self.app.export_settings["encoders_settings"][self.stream.type][self.index],
            lambda doc_viewer: (
                "" if (
                    encoder := (
                        doc_viewer.app.export_settings
                    )["encoders"][self.stream.type][doc_viewer.parent.index]
                ) is None else Encoder(encoder).doc
            )
        )
        self.widgets["encoder_doc_viewer"].hide()
        self.widgets["bitrate_selector"] = BitRateSelector(self)
        # if self.stream.type == "video":
        #     self.widgets["pix_fmt_label"] = QtWidgets.QLabel("Pixel Format:", self)
        #     self.widgets["pix_fmt_label"].hide()

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_title(grid_layout)
        ref_span = self.init_preset(grid_layout, ref_span)
        grid_layout.addWidget(QtWidgets.QLabel("Codec:"), ref_span+1, 0)
        grid_layout.addWidget(self.widgets["codec_combo_box"], ref_span+1, 1)
        grid_layout.addWidget(self.widgets["encoder_label"], ref_span+2, 0)
        grid_layout.addWidget(self.widgets["encoder_combo_box"], ref_span+2, 1)
        grid_layout.addWidget(self.widgets["encoder_doc_viewer"], ref_span+3, 0, 1, 2)
        # if self.stream.type == "video":
        #     grid_layout.addWidget(self.widgets["pix_fmt_label"], ref_span+4, 0)
        #     ref_span += 4
        # else:
        #     ref_span += 3
        grid_layout.addWidget(QtWidgets.QLabel("Flow (bits/s):"), ref_span+4, 0)
        grid_layout.addWidget(self.widgets["bitrate_selector"], ref_span+4, 1)
        self.setLayout(grid_layout)

    @property
    def index(self):
        """Return the input stream relative index of the container output."""
        for index, stream in enumerate(self.app.tree().in_select(self.stream.type)):
            if stream is self.stream:
                return index
        raise KeyError(f"the stream {self.stream} is missing in the container output")

    @property
    def index_abs(self):
        """Return the input stream absolute index of the container output."""
        for index, stream in enumerate(self.app.tree().in_streams):
            if stream is self.stream:
                return index
        raise KeyError(f"the stream {self.stream} is missing in the container output")

    def init_preset(self, grid_layout, ref_span=0):
        """Return the preferences."""
        grid_layout.addWidget(QtWidgets.QLabel("Profile:"), ref_span, 0)
        if self.stream.type == "audio":
            self.widgets["preset"] = PreferencesAudio(self, self.index_abs)
        elif self.stream.type == "video":
            self.widgets["preset"] = PreferencesVideo(self, self.index_abs)
        else:
            raise NotImplementedError(f"not yet supported {self.stream.type}")
        grid_layout.addWidget(self.widgets["preset"], ref_span, 1)
        return ref_span + 1

    def init_title(self, grid_layout, ref_span=0):
        """Return the section title."""
        title = QtWidgets.QLabel(
            f"Stream {self.index_abs} {self.stream.type} {self.index} Settings"
        )
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(title, ref_span, 0, 1, 2)
        return ref_span + 1

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        self.widgets["codec_combo_box"].refresh()
        self.widgets["encoder_combo_box"].refresh()
        if self.app.export_settings["codecs"][self.stream.type][self.index] is None:
            self.widgets["encoder_label"].hide()
            self.widgets["encoder_combo_box"].hide()
            # if self.stream.type == "video":
            #     self.widgets["pix_fmt_label"].hide()
        else:
            self.widgets["encoder_label"].show()
            self.widgets["encoder_combo_box"].show()
            # if self.stream.type == "video":
            #     self.widgets["pix_fmt_label"].show()
        self.widgets["encoder_doc_viewer"].refresh()
        self.widgets["preset"].refresh()
        self.widgets["bitrate_selector"].refresh()
