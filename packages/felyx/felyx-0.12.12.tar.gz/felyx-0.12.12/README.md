# Felyx – Video coder in Python for Experimental Psychology

[![PyPI Version](https://img.shields.io/pypi/v/felyx)](https://pypi.org/project/felyx/)
[![License](https://img.shields.io/pypi/l/felyx?color=lightblue)](https://www.gnu.org/licenses/gpl-3.0.en.html)

Felyx is an application for doing video coding, written entirely in Python, meant essentially for use in Experimental Psychology. Felyx looks like a video editor, but it is not possible to alter the video file loaded into it. Instead, it is possible to add temporal occurrences and save them as CSV (comma-separated value) files.

## Installation

The application is [available at PyPI][] and can be installed via:

    python -m pip install felyx

[available at PyPI]: https://pypi.org/project/felyx/

On Linux, In order to avoid the following warning at startup:
```
qt.multimedia.ffmpeg.libsymbolsresolver: Couldn't load VAAPI library
```
please install the `libav-dev` package (in Debian derivatives).

The application was developed primary on Linux and Windows, but should also work on MacOS.

## Usage

### Loading the video file

After launching the application (`felyx.exe` on Windows, `felyx` on Linux and MacOS), a video file can be loaded via the menu entry `File⇒Open…`. Almost all popular video formats are supported. It is also possible to load a “project” file, in the [ZIP][] format. This file contains a video file and the configuration and data files bundled together. Current work can then be saved to this project file and the worked can be resumed later. For the technical details about the project file, see the [FORMAT specification](FORMAT.md) file.

[ZIP]: https://en.wikipedia.org/wiki/ZIP


### Playing/stopping the video and moving around it

Once the video is loaded, it can be played and stopped using the space key. The left and right arrow keys can be used for going backward and forward, respectively, by one frame in the video. Positioning the cursor (a black triangle) with the mouse is also possible by clicking and dragging the cursor on the time pane.

### The time pane and its timelines

### Events

### Event occurrences

Event occurrences can be defined by pressing the enter key. This will mark one of the borders of the occurrence. The other border can be defined by using the arrow keys or by clicking and dragging the cursor. Once the cursor is at the desired position, type enter again. This will open a dialog window for choosing the label and the color of the occurrence. New labels can be defined in the dialog window by simply typing them. The new created labels will appear in the list of proposed labels when new occurrences will be subsequently created.

Once an occurrence is created, it is possible to change its borders by double-clicking on the occurrence. Two handles will appear, one at the left border of the occurrence and the other at the right border. Click on a border handle and move it with the left and right arrow keys.

The creation of an occurrence can be aborted, once it is start by either typing the Escape key or by clicking on the Abort button in the pop-up window.

The timeline can be zoomed in and out by using the scroll wheel of the mouse.

The occurrences can be saved as a CSV file via the menu item `File⇒Export CSV…`.

## Configuration

(more to come later)

## Contributing

The source code will be available in a public repository at the Gitlab instance of the University of Grenoble Alpes.

## The name of the game

Felyx is named after the grandson of one of the authors. The letter *_y_* is reminiscent of the  *_y_* in Python.

## Authors

Copyright (C) 2024  Esteban Milleret (<esteban.milleret@etu.univ-grenoble-alpes.fr>)

Copyright (C) 2024  Rafael Laboissière (<rafael.laboissiere@cnrs.fr>)


## License

This project is licensed under the terms of the GPL 3.0 or later.

<!--  LocalWords:  Felyx CSV PyPI Alpes Milleret Laboissière GPL MacOS Felyx
 -->
