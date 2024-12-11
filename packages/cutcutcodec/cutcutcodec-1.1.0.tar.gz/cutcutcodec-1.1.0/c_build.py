#!/usr/bin/env python3

"""The rules of compilation for setuptools."""

import os
import sys

from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py

sys.path.insert(0, os.getcwd()) # it is required to find cutcutcodec
from cutcutcodec.utils import get_compilation_rules


class Build(_build_py):
    """Builder to compile c files."""

    def run(self):
        self.run_command("build_ext")
        return super().run()

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules is None:
            self.distribution.ext_modules = []
        self.distribution.ext_modules.append(
            Extension(
                "cutcutcodec.core.generation.video.fractal.fractal",
                sources=["cutcutcodec/core/generation/video/fractal/fractal.c"],
                **get_compilation_rules(),
            )
        )
