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

import colour
import hashlib
from PySide6.QtGui import QColor


def milliseconds_to_formatted_string(milliseconds):
    """
    Converts milliseconds to a string in the format hh:mm:ss.ssss.
    """

    # Convert milliseconds to seconds
    total_seconds = milliseconds / 1000

    # Extract hours, minutes, seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format time string with leading zeros
    time_string = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    # Extract milliseconds (avoiding floating-point rounding issues)
    milliseconds = milliseconds % 1000
    millisecond_string = f"{milliseconds:03d}"  # Pad with leading zeros

    return (
        '<pre style="font-family: monospace">'
        f"{time_string}.{millisecond_string}"
        "</pre>"
    )


def color_fg_from_bg(bg):
    if colour.Color(bg.name()).luminance < 0.5:
        return QColor("white")
    else:
        return QColor("black")


def sha1_file(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
