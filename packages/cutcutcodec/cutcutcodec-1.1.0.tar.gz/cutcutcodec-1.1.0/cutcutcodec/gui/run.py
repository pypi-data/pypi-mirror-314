#!/usr/bin/env python3

"""Entry point of the GUI."""

import multiprocessing
import pathlib
import queue
import signal
import subprocess
import sys
import traceback
import typing

from qtpy import QtWidgets

from cutcutcodec.core.opti.graph import optimize
from cutcutcodec.core.compilation.ast_to_file import ast_to_file
from cutcutcodec.core.compilation.graph_to_ast import graph_to_ast
from cutcutcodec.gui.main import MainWindow


def run_gui(project_file: typing.Optional[pathlib.Path], output: multiprocessing.Queue):
    """Start the GUI."""
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    # soft ctrl+c management, replace lambda by signal.SIG_DFL for fast closing
    signal.signal(signal.SIGINT, lambda *_: app.quit())

    # create the window
    window = MainWindow(output)
    if project_file is not None:
        window.open(project_file)
    window.showMaximized()
    window.refresh()

    # catch and show global exceptions
    def crach_except_hook(exc, value, tb_):
        msg = "".join(traceback.format_exception(exc, value, tb_))
        sys.stderr.write(msg)
        window.crash(msg)
        app.quit()
    sys.excepthook = crach_except_hook

    app.exec()


def run_gui_pipeline(project_file: typing.Optional[pathlib.Path] = None) -> int:
    """Return the main complete pipeline including gui."""
    output = multiprocessing.Queue()

    process_gui = multiprocessing.Process(target=run_gui, args=(project_file, output))
    process_gui.start()
    process_gui.join()

    try:
        res = output.get(False)
    except queue.Empty:  # if the gui was prematuraly closed
        return 0
    if res["optimize"]:
        res["graph"] = optimize(res["graph"])

    # write the file
    filename = res["filename"].with_suffix(".py")
    ast_to_file(graph_to_ast(res["graph"]), filename)

    if res["excecute"]:
        subprocess.run([sys.executable, str(filename)], check=True)

    return 0
