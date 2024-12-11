#!/usr/bin/env python3

"""Entry point of the GUI."""

import pathlib
import sys
import typing

import click


@click.command()
@click.argument(
    "project_file",
    required=False,
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
)
def main(project_file: typing.Optional[pathlib.Path] = None) -> int:
    """Start the graphical user interface, alias to ``cutcutcodec-gui``."""
    # no global import for cutcutcodec.__main__
    from cutcutcodec.gui.run import run_gui_pipeline  # pylint: disable=C0415
    sys.exit(run_gui_pipeline(project_file))


if __name__ == '__main__':
    main()
