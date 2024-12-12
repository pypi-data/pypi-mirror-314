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

from PySide6.QtCore import (
    QEvent,
    QSize,
    Qt,
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QSplitter,
)

from .assets import Assets
from .constants import (
    MAIN_WINDOW_MINIMUM_WIDTH,
    MAIN_WINDOW_MINIMUM_HEIGHT,
)
from .files import Files
from .menu import Menu
from .video import Video
from .timepane import TimePaneView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.files = Files(self)
        self.files.data_to_load = None

        self.setWindowTitle("Felyx")
        self.setMinimumSize(
            QSize(
                MAIN_WINDOW_MINIMUM_WIDTH,
                MAIN_WINDOW_MINIMUM_HEIGHT,
            )
        )

        # Load the QSS file
        with open(Assets().get("style.qss"), "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)

        self.installEventFilter(self)

        self.create_ui()

    def create_ui(self):
        """Set up the user interface, signals & slots"""
        self.video = Video(self)

        splitter = QSplitter(Qt.Orientation.Vertical)
        self.setCentralWidget(splitter)
        splitter.addWidget(self.video)

        # Add TimePaneView
        view = TimePaneView(self)
        splitter.addWidget(view)

        self.time_pane = view.scene.time_pane
        self.scene = view.scene

        self.menu = Menu(self)

    def on_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        """Display a warning dialog to user when app is closing"""

        action = "ok"
        if self.time_pane.data_needs_save:
            msgBox = QMessageBox(
                QMessageBox.Icon.Warning,
                "Quit the application",
                (
                    "You are about to quit the application. "
                    "The changes made in this session will be lost."
                ),
                QMessageBox.StandardButton.Cancel
                | QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Ok,
                self,
            )

            msgBox.button(QMessageBox.StandardButton.Save).setText(
                "Save and Quit"
            )
            msgBox.button(QMessageBox.StandardButton.Ok).setText("Quit")
            msgBox.exec()

            if msgBox.clickedButton() == msgBox.button(
                QMessageBox.StandardButton.Ok
            ):
                action = "ok"
            elif msgBox.clickedButton() == msgBox.button(
                QMessageBox.StandardButton.Save
            ):
                action = "save"
            else:
                action = "ignore"

        if action == "ok":
            # Clean up temp dir
            self.files.temp_dir_cleanup()
            event.accept()
        elif action == "save":
            if self.files.save_project():
                # Clean up temp dir
                self.files.temp_dir_cleanup()
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Right:
                if event.isAutoRepeat():
                    if (
                        self.video.media_player.playbackState()
                        != QMediaPlayer.PlaybackState.PlayingState
                    ):
                        self.video.media_player.play()
                else:
                    self.video.media_player.pause()
                return True
        return False

    def media_status_changed(self):
        if self.files.data_to_load:
            self.files.load_data_file(self.files.data_to_load)
            self.time_pane.changed = False

    def duration_changed(self, duration):
        fd = self.frame_duration()
        if fd:
            length = int(duration / fd)
            self.time_pane.length = length
        else:
            self.time_pane.length = None
        self.time_pane.view.update()

    def load_file(self, path):
        self.files.load_file(path)

    def no_video_loaded(self):
        self.files.no_video_loaded()

    def set_source(self, media):
        # Change video player media
        self.video.set_source(media)

        # Set the media filename as window title
        self.setWindowTitle(os.path.basename(media.path()))

        # Clear the time_pane
        self.time_pane.clear()
        self.scene.create_time_pane()
        self.time_pane = self.scene.time_pane
        self.time_pane.view.update_scale()

    def has_media(self):
        return self.video.media

    def media_player_pause(self):
        self.video.media_player.pause()

    def frame_duration(self):
        return self.video.frame_duration

    def move_to_frame(self, nb_frame, checked=False):
        self.time_pane.position = self.time_pane.position + nb_frame
