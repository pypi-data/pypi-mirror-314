#!/usr/bin/env python3

"""Allow to view and add all generators."""

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.gui.entry.base import Entry


class Generators(Entry):
    """Generators visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["generation"],
            {"ContainerInput", "GeneratorAudioEmpty", "GeneratorVideoEmpty"},
            ContainerInput
        )


class GeneratorsAudio(Entry):
    """Audio generators visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["generation/audio"],
            {"ContainerInput", "GeneratorAudioEmpty"},
            ContainerInput
        )


class GeneratorsVideo(Entry):
    """Video generators visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["generation/video"],
            {"ContainerInput", "GeneratorVideoEmpty"},
            ContainerInput
        )
