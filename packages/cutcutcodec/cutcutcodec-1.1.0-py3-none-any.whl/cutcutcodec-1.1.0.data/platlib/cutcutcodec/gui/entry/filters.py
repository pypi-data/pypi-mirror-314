#!/usr/bin/env python3

"""Allow to view and add all generators."""

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.gui.entry.base import Entry


class Filters(Entry):
    """Filters visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["filter"],
            {"Filter", "FilterAudioIdentity", "FilterVideoIdentity", "MetaFilter"},
            Filter,
        )


class FiltersAudio(Entry):
    """Audio filters visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["filter/audio"],
            {"Filter", "FilterAudioIdentity", "MetaFilter"},
            Filter,
        )


class FiltersVideo(Entry):
    """Video filters visualization window."""

    def __init__(self, parent):
        super().__init__(
            parent,
            ["filter/video"],
            {"Filter", "FilterVideoIdentity", "MetaFilter"},
            Filter,
        )
