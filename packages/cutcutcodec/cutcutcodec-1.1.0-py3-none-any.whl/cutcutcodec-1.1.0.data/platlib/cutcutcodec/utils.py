#!/usr/bin/env python3

"""Pythonic tools."""

import pathlib

import numpy as np


def get_compilation_rules() -> dict:
    """Return the extra compilation rules."""
    return {
        "define_macros": [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],  # for warning
        "extra_compile_args": [
            "-fopenmp",  # for threads
            "-fopenmp-simd",  # for single instruction multiple data
            "-lm",  # for math functions
            "-march=native",  # uses local processor instructions for optimization
            "-O3",  # hight optimization, -O3 include -ffast-math
        ],
        "include_dirs": [np.get_include()],  # requires for  #include numpy
    }


def get_project_root() -> pathlib.Path:
    """Return the absolute project root folder.

    Examples
    --------
    >>> from cutcutcodec.utils import get_project_root
    >>> root = get_project_root()
    >>> root.is_dir()
    True
    >>> root.name
    'cutcutcodec'
    >>> sorted(p.name for p in root.iterdir())
    ['__init__.py', '__main__.py', '__pycache__', 'core', 'examples', 'gui', 'testing', 'utils.py']
    >>>
    """
    return pathlib.Path(__file__).resolve().parent
