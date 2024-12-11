#!/usr/bin/env python3

"""Plays audio in background for the video preview."""

import queue
import threading
import sys
import subprocess

import numpy as np

from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.layout import Layout


class AudioPlayer(threading.Thread):
    """Allow to play sound buffers in the background, without blocking."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = "mono"  # is quicklely overwriten
        self._buff = queue.Queue()
        self._restart = False
        self._is_alive = True
        self._samplerate = 48000  # is quickely overwriten

    def get_layout(self) -> str:
        """Return the numbers of audio channels."""
        return self._layout

    def set_layout(self, new_profile: str):
        """Update the number of channels and recreate a new ffmpeg connection."""
        assert isinstance(new_profile, str), new_profile.__class__.__name__
        if new_profile != self.get_layout():
            self._layout = new_profile
            self.restart()

    def restart(self):
        """Allow to reset link with the sound card."""
        while True:
            try:
                self._buff.get_nowait()
            except queue.Empty:
                break
        self._restart = True
        self._buff.put(b"")
        while self._restart:
            continue

    def run(self):
        """Allow interaction with the sound card."""
        while self._is_alive:
            cmd = [
                "ffmpeg",
                "-v", "error",
                "-f", "f32le",  # means 32 bit input
                "-acodec", "pcm_f32le",  # means raw 32 bit input
                "-ar", str(self.get_samplerate()),
                "-ac", str(len(Layout(self.get_layout()).channels)),
                "-i", "pipe:",
                "-c:a", "copy", "-bufsize:a", "1024",
                "-f", "pulse",
                "-name", "cutcutcodec",
                "-buffer_size", "1024",  # in bytes or "-buffer_duration", "20",  # in ms
                "cutcutcodec",
            ]
            with subprocess.Popen(
                cmd,
                bufsize=1024,
                stdin=subprocess.PIPE,
                stdout=sys.stdout,
                stderr=sys.stderr
            ) as process:
                with process.stdin as stdin:
                    while self._is_alive and not self._restart:
                        stdin.write(self._buff.get())
            self._restart = False

    def get_samplerate(self) -> int:
        """Return the audio signal sampling frequency in Hz."""
        return self._samplerate

    def set_samplerate(self, new_samplerate: int):
        """Update the samplerate and recreate a new ffmpeg connection."""
        assert isinstance(new_samplerate, int), new_samplerate.__class__.__name__
        assert new_samplerate > 0, new_samplerate
        if new_samplerate != self.get_samplerate():
            self._samplerate = new_samplerate
            self.restart()

    def stop(self):
        """Set run flag to False and waits for thread to finish."""
        self._is_alive = False
        self._buff.put(b"")  # relunch loop in run for exit
        self.join()

    def update_frame(self, frame: FrameAudio):
        """Add the new samples to the buffer."""
        audio_data = bytes(frame.numpy(force=True).astype(np.float32).ravel(order="F"))
        self.set_layout(frame.layout.name)
        self.set_samplerate(frame.rate)
        self._buff.put(audio_data)
