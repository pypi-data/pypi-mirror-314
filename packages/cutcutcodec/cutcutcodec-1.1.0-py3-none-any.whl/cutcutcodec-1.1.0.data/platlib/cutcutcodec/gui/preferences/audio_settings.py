#!/usr/bin/env python3

"""Allow to select the parameters of an audio stream."""

import logging
import re
import typing

from qtpy import QtWidgets

from cutcutcodec.core.compilation.export.compatibility import Compatibilities
from cutcutcodec.core.compilation.export.rate import available_audio_rates, suggest_audio_rate
from cutcutcodec.gui.base import CutcutcodecWidget


CLASSICAL_RATES = {
    8000: "telephone",
    11025: "lower-quality PCM",
    22050: "speech low quality",
    32000: "speech hight quality",
    37800: "cd-rom-xa",
    44056: "ntsc",
    44100: "standard cd-audio, human perception threshold",
    47250: "pcm",
    48000: "standard video",
    50000: "sound-stream",
    50400: "Mitsubishi X-80",
    88200: "pro audio gear uses 2*44100",
    96000: "dvd-audio, bd-rom 2*48000",
    176400: "pro audio gear uses 4*44100",
    192000: "pro audio gear uses 4*48000",
}


class PreferencesAudio(CutcutcodecWidget, QtWidgets.QWidget):
    """Allow to select the sampling frequency and the number of channels of an audio stream."""

    def __init__(self, parent, index_abs):
        super().__init__(parent)
        self._parent = parent

        self.rate_textbox = None
        self.rate_combobox = None

        tree = self.app.tree()
        self.stream = tree.in_streams[index_abs]
        self.index_rel = None
        for i, stream in enumerate(tree.in_select("audio")):
            if stream is self.stream:
                self.index_rel = i
        assert self.index_rel is not None, "the output container has been modified in background"

        grid_layout = QtWidgets.QGridLayout()
        self.init_rate(grid_layout)
        self.setLayout(grid_layout)
        self.refresh()

    def _select_rate(self, text: str):
        """From combo box."""
        # decode the rate int or None
        if "automatic" in text:
            rate = None
        elif text == "manual":
            rate = self.best_rate
        else:
            if (match := re.search(r"\d+", text)) is None:
                raise ValueError(f"failed to find a rate from the text {text}")
            rate = int(match.group())

        # update only if it changed
        if rate != self.app.export_settings["rates"]["audio"][self.index_rel]:
            self.app.export_settings["rates"]["audio"][self.index_rel] = rate
            print(f"update rate (stream audio {self.index_rel}) to {rate}")
            self.main_window.refresh()

    def _validate_rate(self):
        """Check that the sample rate is a correct integer."""
        text = self.rate_textbox.text()
        # parsing verification
        if re.fullmatch(r"\d*[1-9]\d*", text):  # ensure != 0
            rate = int(text)
        elif re.fullmatch(r"\s*", text):
            rate = None
        else:
            self.rate_textbox.setStyleSheet("background:red;")
            return

        # update and continue checking only if it changed
        if rate != self.app.export_settings["rates"]["audio"][self.index_rel]:
            # compatibility with codec verification
            if rate is not None and (choices := self.available_rates) is not None:
                if rate not in choices:
                    self.rate_textbox.setStyleSheet("background:red;")
                    msg = (
                        f"the only available sample rates are {sorted(choices)}, "
                        f"but {rate} is specified"
                    )
                    logging.warning(msg)
                    return

            # validation, apply changed
            self.app.export_settings["rates"]["audio"][self.index_rel] = rate
            print(f"update rate (stream audio {self.index_rel}): {rate}")
            self.rate_textbox.setStyleSheet("background:none;")

            # refresh all
            if rate in CLASSICAL_RATES:
                self.rate_combobox.setCurrentText(f"{rate} ({CLASSICAL_RATES[rate]})")
            else:
                self.rate_combobox.setCurrentText("manual")
            self.main_window.refresh()

    @property
    def available_rates(self) -> typing.Union[None, set[int]]:
        """Return the set of the available sample rates for the given encoder/muxer.

        The value None means there is no constraints.
        """
        if self.app.export_settings["encoders"]["audio"][self.index_rel] is not None:
            encoders = {self.app.export_settings["encoders"]["audio"][self.index_rel]}
        elif self.app.export_settings["codecs"]["audio"][self.index_rel] is not None:
            muxer = self.app.export_settings["muxer"]
            muxers = [muxer] if muxer is not None else None
            encoders = set(Compatibilities().encoders_audio(
                self.app.export_settings["codecs"]["audio"][self.index_rel], muxers,
                layout=self.stream.layout.name,  # we should to forward 'profile' as well
                rate=self.app.export_settings["rates"]["audio"][self.index_rel],
            ))
        else:
            return None
        return available_audio_rates(encoders)

    @property
    def best_rate(self) -> int:
        """Return the most appropriated rate for the current configuration.

        If the rate is specified by the user, it returns the given rate.
        Otherwise it ask to ``cutcutcodec.core.compilation.export.rate.suggest_audio_rate``
        for the best estimation.
        """
        if (rate := self.app.export_settings["rates"]["audio"][self.index_rel]) is not None:
            return rate
        return suggest_audio_rate(self.stream, self.available_rates)

    def init_rate(self, grid_layout, ref_span=0):
        """Display and allows to modify the framerate."""
        grid_layout.addWidget(QtWidgets.QLabel("Sample Rate (Hz):"), ref_span, 0)
        self.rate_textbox = QtWidgets.QLineEdit()
        self.rate_textbox.editingFinished.connect(self._validate_rate)
        grid_layout.addWidget(self.rate_textbox, ref_span, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Selection:"), ref_span+1, 0)
        self.rate_combobox = QtWidgets.QComboBox()
        self.rate_combobox.textActivated.connect(self._select_rate)
        grid_layout.addWidget(self.rate_combobox, ref_span+1, 1)
        return ref_span + 2

    def refresh(self):
        """Update the elements of this widget and child widgets."""
        # update combobox items
        self.rate_combobox.clear()
        self.rate_combobox.addItem("automatic (optimal Nyquist–Shannon)")
        self.rate_combobox.addItem("manual")
        choices = set()
        for rate in sorted(self.available_rates or CLASSICAL_RATES):
            if rate in CLASSICAL_RATES:
                choices.add(rate)
                self.rate_combobox.addItem(f"{rate} ({CLASSICAL_RATES[rate]})")

        # select the write combobox item
        if (rate := self.app.export_settings["rates"]["audio"][self.index_rel]) is None:
            self.rate_combobox.setCurrentText("automatic (optimal Nyquist–Shannon)")
        elif rate in choices:
            self.rate_combobox.setCurrentText(f"{rate} ({CLASSICAL_RATES[rate]})")
        else:
            self.rate_combobox.setCurrentText("manual")

        # update textbox item
        self.rate_textbox.setPlaceholderText(
            str(suggest_audio_rate(self.stream, self.available_rates))
        )
        if (rate := self.app.export_settings["rates"]["audio"][self.index_rel]) is not None:
            self.rate_textbox.setText(str(rate))
        else:
            self.rate_textbox.setText("")
        self.rate_textbox.setStyleSheet("background:none;")
