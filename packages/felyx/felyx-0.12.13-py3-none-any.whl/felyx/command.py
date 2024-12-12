# Felyx - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Felyx
~~~~~~~~

Video coder in Python for Experimental Psychology

Usage:
  felyx [--size=<WIDTHxHEIGTH> | --fullscreen] [--config=<CONFIGFILE>] [<path>]
  felyx -h | --help
"""

import sys

from docopt import docopt
from .app import App

usage = __doc__.split("\n\n")[2]


def main():
    """Entry point for the application"""
    args = docopt(usage, argv=sys.argv[1:])
    app = App(
        path=args["<path>"],
        size=args["--size"],
        fullscreen=args["--fullscreen"],
        config=args["--config"],
    )
    sys.exit(app.exec())
