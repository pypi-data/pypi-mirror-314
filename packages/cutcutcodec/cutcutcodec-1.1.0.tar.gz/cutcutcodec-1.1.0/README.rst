.. rst syntax: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/
.. version conv: https://peps.python.org/pep-0440/
.. icons: https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html or https://www.pythonguis.com/faq/built-in-qicons-pyqt/
.. pyqtdoc: https://www.riverbankcomputing.com/static/Docs/PyQt6/
.. colors-spaces: https://trac.ffmpeg.org/wiki/colorspace

***********
CutCutCodec
***********

.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: [license MIT]
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/linting-pylint-green
    :alt: [linting: pylint]
    :target: https://github.com/pylint-dev/pylint

.. image:: https://img.shields.io/badge/tests-pass-green
    :alt: [testing]
    :target: https://docs.pytest.org/

.. image:: https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue
    :alt: [versions]
    :target: https://framagit.org/robinechuca/cutcutcodec/-/blob/main/run_tests.sh

.. image:: https://static.pepy.tech/badge/cutcutcodec
    :alt: [downloads]
    :target: https://www.pepy.tech/projects/cutcutcodec

.. image:: https://readthedocs.org/projects/cutcutcodec/badge/?version=latest
    :alt: [documentation]
    :target: https://cutcutcodec.readthedocs.io/latest/


Description
===========

This **video editing software** has a graphical interface powered by qtpy (run ``cutcutcodec-gui``).
It has been designed for speed and to implement some effects that are hard to find elsewhere.
The kernel is written in python and C, so it's easy to integrate it in your own project (module ``cutcutcodec.core``).
Although it allows you to fine-tune many parameters, it's smart enough to find the settings that are best suited to your project.

This software is **light**, **fast** and **highly configurable** for the following reasons:

#. Based on ffmpeg, this software supports an incredible number of formats and codecs.
#. This software allows editing the assembly graph. Compared to a timeline, this representation permits to do everything.
#. This software doesn't export the final video directly from the graphic interface. Instead, it generates a python script. You can edit this script yourself, giving you infinite possibilities!
#. A complete test benchmark guarantees an excelent kernel reliability.
#. Powered by `torch <https://pytorch.org/>`_ and written in C, this software efficiently exploits the CPU and GPU in order to make it very fast.
#. Video export is performed without a graphical interface, releasing a large part of computer resources to speed up export.
#. This software is able to optimize the assembly graph in order to limit calculation waste.
#. The code is parallelised to take advantage of all the CPU threads, making it extremely fast.

.. image:: https://framagit.org/robinechuca/cutcutcodec/-/raw/main/doc/gui.avif
    :alt: An example of the cutcutcodec GUI.


Quick Start
===========

Installation
------------

Please follow the `cutcutcodec installation guide <https://cutcutcodec.readthedocs.io/latest/installation.html>`_.

You can use the following command to install everything automatically (not recommended, it's better to follow the guide).

.. code::

    pip install cutcutcodec[gui]


Running
-------

For a very complete description, please refer to `the documentation <https://cutcutcodec.readthedocs.io/latest/start.html>`_.

In a terminal, just type ``cutcutcodec-gui`` to start the GUI, it is possible to access the *cli* with:

.. code::

    python -m cutcutcodec --help


Features
========

Audio
-----

* General properties
    #. Supports a large number of channels (mono, stereo, 5.1, 7.1, ...) with all sampeling rate.
    #. Automatic detection of the optimal sample frequency.
* Generation
    #. White-noise generation.
    #. Generate any audio signal from any equation.
* Filters
    #. Cutting, translate and concatenate.
    #. Add multiple tracks.
    #. Arbitrary equation on several channels of several tracks. (dynamic volume, mixing, wouawoua, ...)
    #. Finite Impulse Response (FIR) invariant filter. (reverb, equalizer, echo, delay, volume, ...)
    #. Hight quality anti aliasing low pass filter (based on FIR).

Video
-----

* General properties
    #. Unlimited support of all image resolutions. (FULL HD, 4K, 8K, ...)
    #. No limit on fps. (60fps, 120fps, ...)
    #. Automatic detection of the optimal resolution and fps.
    #. Support for the alpha transparency layer.
    #. Floating-point image calculation for greater accuracy.
* Generation
    #. White-noise generation.
    #. Generate any video signal from any equation.
    #. Mandelbrot fractal generation.
* Filters
    #. Cutting, translate and concatenate.
    #. Resize and crop (high quality, no aliasing).
    #. Overlaying video tracks (with transparency control).
    #. Apply an arbitrary equation one several video streams.


Example
=======

In this example we open a video file, add video noise, add audio A and C note, select the subclip between t=0s and t=10s, and write the result to a new file:

.. code:: python

    from cutcutcodec.core.filter.audio.subclip import FilterAudioSubclip
    from cutcutcodec.core.filter.video.add import FilterVideoAdd
    from cutcutcodec.core.filter.video.equation import FilterVideoEquation
    from cutcutcodec.core.filter.video.subclip import FilterVideoSubclip
    from cutcutcodec.core.generation.audio.equation import GeneratorAudioEquation
    from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    from cutcutcodec.core.io import read
    from cutcutcodec.core.io.write import ContainerOutputFFMPEG

    with read("cutcutcodec/examples/video.mp4") as container:
        (trans,) = FilterVideoEquation(container.out_streams, "b0", "g0", "r0", "a0/2").out_streams
        (noise,) = GeneratorVideoNoise().out_streams
        (video,) = FilterVideoAdd([trans, noise]).out_streams
        (video_trunc,) = FilterVideoSubclip([video], 0, 10).out_streams
        (note_a,) = GeneratorAudioEquation("sin(2*pi*440*t)", "sin(2*pi*523.25*t)").out_streams
        (note_a_trunc,) = FilterAudioSubclip([note_a], 0, 10).out_streams
        ContainerOutputFFMPEG(
            [video_trunc, note_a_trunc],
            "final.mkv",
            [
                {"encodec": "libx264", "rate": 30, "shape": (720, 1080), "options": {"crf": "23"}},
                {"encodec": "libvorbis", "rate": 44100},
            ],
        ).write()


What's new ?
============

For the complete list of changes, refer to the `git commits <https://framagit.org/robinechuca/cutcutcodec/-/network/main?ref_type=heads>`_.

1.0.1
-----

* Add a command line interface.
* Compiling dynamic expressions in C.

1.0.2
-----

* Add support for ``ffmpeg 6``.
* Able to compile ``atan`` function.
* Handling of non-square pixel readings.

1.0.3
-----

* Improved ergonomics of the "Entry Tabs" and "Export" window.
* Speed-up codec/encoder/muxer tests of compatibility by a factor 10.

1.0.4
-----

* Read images and SVG as well.
