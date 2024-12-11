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

import os

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)
from .mainwindow import MainWindow
from .constants import (
    APP_WINDOW_WIDTH,
    APP_WINDOW_HEIGHT,
)


class App(QApplication):

    def __init__(self, path=None, size=None, fullscreen=None, config=None):
        super().__init__([])
        window = MainWindow()
        width = APP_WINDOW_WIDTH
        height = APP_WINDOW_HEIGHT
        self.size = size
        if self.size:
            dim = self.size.split("x")
            if len(dim) == 2:
                try:
                    width = int(dim[0])
                    height = int(dim[1])
                except ValueError:
                    self.wrong_size_message()
            else:
                self.wrong_size_message()
        if fullscreen:
            window.showFullScreen()
        else:
            window.resize(width, height)
        if config:
            window.files.set_config_file(config)
        window.show()
        if path:
            window.load_file(os.path.abspath(path))
        else:
            window.no_video_loaded()

    def wrong_size_message(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Felyx: parse error of size argument")
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(
            f"The value given to the --size option ({self.size}) is not in "
            "the format 'WIDTHxHEIGHT', with WIDTH and HEIGHT being integer "
            "numbers. Using the default value "
            f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}."
        )
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec()
