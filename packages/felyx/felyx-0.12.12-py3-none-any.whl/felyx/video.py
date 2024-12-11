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

import time
from pathlib import Path
from functools import partial

from PySide6.QtCore import (
    Qt,
    QSize,
    QTimer,
)
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaMetaData,
    QMediaPlayer,
)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from .assets import Assets
from .constants import TIMESTAMP_HEIGHT
from .utils import (
    milliseconds_to_formatted_string,
)

with open(Path(__file__).parent.joinpath("images.py")) as f:
    exec(f.read())


class Video(QWidget):
    """A simple Media Player using Qt"""

    def __init__(self, window):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.media = None
        self._position = 0
        self.frame_duration = None
        self.window = window

        self.create_ui()

        self.setup_timer()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if position != self._position:
            self._position = int(position)
            if self.playback_state() != QMediaPlayer.PlaybackState.PlayingState:
                self.media_player.setPosition(self.position)
            self.timestamp.update(self.media_player.position())
            self.window.time_pane.position = round(
                self.position / self.frame_duration
            )

    def create_ui(self):
        """Set up the user interface, signals & slots"""
        # Create the video widget
        video_widget = QVideoWidget()

        # Create Assets object
        assets = Assets()

        # Create the button layout
        self.button_box = QHBoxLayout()

        # Create the timestamp
        self.timestamp = Timestamp(self.media_player)
        self.button_box.addWidget(self.timestamp)

        self.button_box.addStretch(1)

        # Create the -10 frame button
        backward_10_frames = self.add_player_button(
            QIcon(assets.get("minus10.png")),
            "10th Previous Frame\n[Ctrl+Shift+Left]",
            partial(self.window.move_to_frame, -10),
        )

        # Create the -5 frame button
        backward_5_frames = self.add_player_button(
            QIcon(assets.get("minus5.png")),
            "5th Previous Frame\n[Ctrl+Left]",
            partial(self.window.move_to_frame, -5),
        )

        # Create the previous frame button
        previous_frame = self.add_player_button(
            QIcon(assets.get("minus1.png")),
            "Previous Frame\n[Left]",
            partial(self.window.move_to_frame, -1),
        )

        # Create the play/pause button
        self.play_button = self.add_player_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay),
            "Play\n[Space]",
            self.play_pause,
        )

        # Create the stop button
        self.stop_button = self.add_player_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop),
            "Stop\n[s]",
            self.stop,
        )

        # Create the next frame button
        next_frame = self.add_player_button(
            QIcon(assets.get("plus1.png")),
            "Next Frame\n[Right]",
            partial(self.window.move_to_frame, 1),
        )

        # Create the +5 frame button
        forward_5_frames = self.add_player_button(
            QIcon(assets.get("plus5.png")),
            "5th Next Frame\n[Ctrl+Right]",
            partial(self.window.move_to_frame, 5),
        )

        # Create the +10 frame button
        forward_10_frames = self.add_player_button(
            QIcon(assets.get("plus10.png")),
            "10th Next Frame\n[Ctrl+Shift+Right]",
            partial(self.window.move_to_frame, 10),
        )

        self.frame_buttons = [
            backward_10_frames,
            backward_5_frames,
            previous_frame,
            next_frame,
            forward_5_frames,
            forward_10_frames,
        ]

        self.button_box.addStretch(1)

        # Create the volume slider
        self.volume = VolumeSlider(self)
        # Add the volume slider to the button layout
        self.button_box.addWidget(self.volume)

        # Create the main layout and add the button layout and video widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(video_widget)
        self.layout.addLayout(self.button_box)

        # Setup the media player
        self.media_player.setVideoOutput(video_widget)
        self.media_player.playbackStateChanged.connect(
            self.playback_state_changed
        )
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        # Setup the audio output
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Prevent the individual UIs from getting the focus
        for ui in [
            self.play_button,
            self.stop_button,
            self.volume,
            video_widget,
        ] + self.frame_buttons:
            ui.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Add the main layout to the main window
        self.setLayout(self.layout)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(
            partial(self.timestamp.update, self.media_player.position())
        )

    def play_pause(self):
        """Toggle play/pause status"""
        action = self.window.menu.play_action
        if self.playback_state() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            action.setText("Play")
            action.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
        else:
            self.media_player.play()
            action.setText("Pause")
            action.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )

    def stop(self):
        """Stop player"""
        self.media_player.stop()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )

    def playback_state(self):
        return self.media_player.playbackState()

    def playback_state_changed(self, state):
        """Set the button icon when media changes state"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.timer.start()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
        else:
            self.timer.stop()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
            self.window.time_pane.position = round(
                self.media_player.position() / self.frame_duration
            )

        self.stop_button.setEnabled(
            state != QMediaPlayer.PlaybackState.StoppedState
        )
        self.window.menu.stop_action.setEnabled(
            state != QMediaPlayer.PlaybackState.StoppedState
        )
        for ui in self.frame_buttons:
            ui.setEnabled(state == QMediaPlayer.PlaybackState.PausedState)

        for action in [
            self.window.menu.previous_frame_action,
            self.window.menu.next_frame_action,
            self.window.menu.fifth_previous_frame_action,
            self.window.menu.tenth_previous_frame_action,
            self.window.menu.fifth_next_frame_action,
            self.window.menu.tenth_next_frame_action,
            self.window.menu.add_occurrence_action,
        ]:
            action.setEnabled(state == QMediaPlayer.PlaybackState.PausedState)

    def media_status_changed(self, state):
        if state == QMediaPlayer.MediaStatus.LoadedMedia:
            # Enable play button
            self.window.menu.play_action.setEnabled(True)
            # Enable save project button
            self.window.menu.save_project_action.setEnabled(True)

        if state == QMediaPlayer.MediaStatus.BufferedMedia:
            self.window.media_status_changed()

    def position_changed(self, position):
        """Update the position slider"""
        self.position = position

    def duration_changed(self, duration):
        """Update the duration slider"""
        metadata = self.media_player.metaData()
        fps = metadata.value(QMediaMetaData.Key.VideoFrameRate)
        self.frame_duration = 1000 / fps
        self.window.duration_changed(duration)

    def add_player_button(self, icon, tooltip, cbfunc):
        ui = QPushButton()
        ui.setEnabled(False)
        ui.setFixedHeight(24)
        ui.setFixedWidth(26)
        ui.setIconSize(QSize(16, 16))
        ui.setIcon(icon)
        ui.setToolTip(tooltip)
        ui.clicked.connect(cbfunc)
        self.button_box.addWidget(ui)
        return ui

    def set_source(self, media):
        self.media = media

        # Before loading a new media, stop the current one. Also, wait a
        # little amount of time, in order to avoid race conditions.
        self.media_player.stop()
        time.sleep(0.1)
        # Set the source of the media player
        self.media_player.setSource(media)

        # Show first frame
        self.media_player.play()
        self.media_player.pause()

        # Enable the buttons
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)


class Timestamp(QLabel):

    def __init__(self, media_player):
        super().__init__()
        self.set_text(0)
        self.setFixedHeight(TIMESTAMP_HEIGHT)
        self.media_player = media_player

    def set_text(self, time):
        self.setText(milliseconds_to_formatted_string(time))

    def update(self, time):
        """Update the timestamp"""
        self.set_text(time)


class VolumeSlider(QSlider):

    def __init__(self, parent):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.parent = parent
        self.setMinimumWidth(110)
        self.setRange(0, 100)
        self.setValue(100)
        self.valueChanged.connect(self.set_audio_volume)
        self.update_tooltip()

    def set_audio_volume(self, volume):
        self.parent.audio_output.setVolume(volume / 100)
        self.update_tooltip()

    def update_tooltip(self):
        self.setToolTip(f"Audio volume ({self.value()}%)")
