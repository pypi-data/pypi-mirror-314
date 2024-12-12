# Felyx - A video coder for Experimental Psychology
#
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

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# Configuration and metadada file
CONFIG_FILENAME = "config.yml"
METADATA_FILENAME = "metadata.yml"

# Application name
APP_NAME = "felyx"

# URLs for the About window
LICENSE_NAME = "GPL v3 or later"
LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.en.html"
REPOSITORY_URL = (
    "https://gricad-gitlab.univ-grenoble-alpes.fr/babylab-lpnc/video-coder"
)
PYPI_URL = "https://pypi.org/project/felyx/"

# Default dimensions of the main application window
APP_WINDOW_WIDTH = 640
APP_WINDOW_HEIGHT = 480

# Time scale height
TIME_SCALE_HEIGHT = 25

# Cursor appearance
CURSOR_PEN_COLOR = Qt.GlobalColor.black
CURSOR_BRUSH_COLOR_DEFAULT = QColor(0, 0, 0, 100)
CURSOR_BRUSH_COLOR_CREATION = QColor(255, 0, 0, 100)
CURSOR_HANDLE_WIDTH = 10

# Minimum size of main window
MAIN_WINDOW_MINIMUM_WIDTH = 640
MAIN_WINDOW_MINIMUM_HEIGHT = 320

# Occurrence appearance
OCCURRENCE_PEN_COLOR = QColor(0, 0, 0)
OCCURRENCE_BG_COLOR = QColor(128, 128, 128)
OCCURRENCE_PEN_WIDTH_ON_CURSOR = 3
OCCURRENCE_PEN_WIDTH_OFF_CURSOR = 1
OCCURRENCE_HANDLE_WIDTH = 9
OCCURRENCE_HANDLE_HEIGHT_FRACTION = 0.5

# Tick locator parameter
TICK_LOCATOR_MIN_GAP = 0.05

# Timeline appearance
TIMELINE_HEIGHT = 60
TIMELINE_MASK_ON_COLOR = QColor(0, 0, 0, 0)
TIMELINE_MASK_OFF_COLOR = QColor(0, 0, 0, 80)
TIMELINE_TITLE_HEIGHT = 20
TIMELINE_TITLE_BG_COLOR = QColor(100, 100, 100)
TIMELINE_TITLE_FG_COLOR = Qt.GlobalColor.white

# Event default color
EVENT_DEFAULT_COLOR = QColor(255, 255, 255)

# Data file constants
CSV_HEADERS = ["timeline", "event", "begin", "end", "comment"]
CSV_DELIMITER = ","
CSV_ALLOWED_DELIMITERS = {
    "comma (,)": ",",
    "semicolon (;)": ";",
    "tab": "\t",
}

# GraphicsView zooming constants
MINIMUM_ZOOM_FACTOR = 0
ZOOM_STEP = 1.2

# Timestamp height
TIMESTAMP_HEIGHT = 24
