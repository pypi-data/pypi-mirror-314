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

import platform
from functools import partial
from math import inf

from PySide6.QtCore import (
    Qt,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QDesktopServices,
    QKeySequence,
)
from PySide6.QtWidgets import (
    QMessageBox,
    QStyle,
)

from .about import About
from .constants import (
    PYPI_URL,
    REPOSITORY_URL,
)


class Menu:

    def __init__(self, window):

        self.window = window
        self.menu_bar = window.menuBar()
        self.style = self.window.style()

        self.create_file_menu()
        self.create_play_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_data_menu()
        self.create_help_menu()

    def create_file_menu(self):
        menu = self.menu_bar.addMenu("&File")

        # Add actions to file menu
        open_action = QAction(
            self.style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "&Open video",
            self.window,
            shortcut=QKeySequence.StandardKey.Open,
            triggered=self.window.files.open_video,
        )

        open_project_action = QAction(
            self.style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open &project",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_O
            ),
            triggered=self.window.files.open_project,
        )

        icon = self.style.standardIcon(
            QStyle.StandardPixmap.SP_DialogSaveButton
        )
        self.save_project_action = QAction(
            icon,
            "Save project",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_S),
            triggered=self.window.files.save_project,
            enabled=False,
        )

        export_data_action = QAction(
            icon,
            "Export Data",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_S
            ),
            triggered=self.window.files.export_data_file,
        )

        export_config_action = QAction(
            icon,
            "Export Configuration",
            self.window,
            triggered=self.window.files.save_config_file,
        )

        close_action = QAction(
            "Quit",
            self.window,
            shortcut=(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Q)
                if platform.system() == "Windows"
                else QKeySequence.StandardKey.Quit
            ),
            triggered=self.window.close,
        )

        menu.addAction(open_action)
        menu.addAction(open_project_action)
        menu.addAction(self.save_project_action)
        menu.addAction(export_data_action)
        menu.addAction(export_config_action)
        menu.addAction(close_action)

    def create_play_menu(self):
        # Add actions to play menu
        menu = self.menu_bar.addMenu("&Play")
        self.play_action = QAction(
            self.style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay),
            "Play",
            self.window,
            shortcut=Qt.Key.Key_Space,
            triggered=self.window.video.play_pause,
            enabled=False,
        )

        icon = self.style.standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        self.stop_action = QAction(
            icon,
            "Stop",
            self.window,
            shortcut=Qt.Key.Key_S,
            triggered=self.window.video.stop,
            enabled=False,
        )

        icon = self.style.standardIcon(
            QStyle.StandardPixmap.SP_MediaSkipBackward
        )
        self.previous_frame_action = QAction(
            icon,
            "Go to the previous frame",
            self.window,
            shortcut=Qt.Key.Key_Left,
            triggered=partial(self.window.move_to_frame, -1),
            enabled=False,
        )
        self.fifth_previous_frame_action = QAction(
            icon,
            "Go to the fifth previous frame",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Left),
            triggered=partial(self.window.move_to_frame, -5),
            enabled=False,
        )
        self.tenth_previous_frame_action = QAction(
            icon,
            "Go to the tenth previous frame",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_Left
            ),
            triggered=partial(self.window.move_to_frame, -10),
            enabled=False,
        )

        icon = self.style.standardIcon(
            QStyle.StandardPixmap.SP_MediaSkipForward
        )
        self.next_frame_action = QAction(
            icon,
            "Go to the next frame",
            self.window,
            shortcut=Qt.Key.Key_Right,
            triggered=partial(self.window.move_to_frame, 1),
            enabled=False,
        )
        self.fifth_next_frame_action = QAction(
            icon,
            "Go to the fifth next frame",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Right),
            triggered=partial(self.window.move_to_frame, 5),
            enabled=False,
        )
        self.tenth_next_frame_action = QAction(
            icon,
            "Go to the tenth next frame",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_Right
            ),
            triggered=partial(self.window.move_to_frame, 10),
            enabled=False,
        )

        for action in [
            self.play_action,
            self.stop_action,
            self.tenth_previous_frame_action,
            self.fifth_previous_frame_action,
            self.previous_frame_action,
            self.next_frame_action,
            self.fifth_next_frame_action,
            self.tenth_next_frame_action,
        ]:
            menu.addAction(action)

    def create_edit_menu(self):
        menu = self.menu_bar.addMenu("&Edit")

        # Edit Timeline submenu
        edit_timeline_menu = menu.addMenu("&Timeline")

        self.new_timeline_top_action = QAction(
            "Add new timeline at the top",
            self.window,
            shortcuts=[
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Return),
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Enter),
            ],
            triggered=partial(self.new_timeline, -inf),
            enabled=True,
        )
        edit_timeline_menu.addAction(self.new_timeline_top_action)

        self.new_timeline_above_action = QAction(
            "Add new timeline above selected",
            self.window,
            triggered=partial(self.new_timeline, -1),
            enabled=True,
        )
        edit_timeline_menu.addAction(self.new_timeline_above_action)

        self.new_timeline_below_action = QAction(
            "Add new timeline below selected",
            self.window,
            triggered=partial(self.new_timeline, 1),
            enabled=True,
        )
        edit_timeline_menu.addAction(self.new_timeline_below_action)

        self.new_timeline_bottom_action = QAction(
            "Add new timeline at the bottom",
            self.window,
            triggered=partial(self.new_timeline, inf),
            enabled=True,
        )
        edit_timeline_menu.addAction(self.new_timeline_bottom_action)

        self.edit_timeline_properties_action = QAction(
            "Edit Properties of Selected Timeline",
            self.window,
            triggered=self.edit_timeline_properties,
            enabled=True,
        )
        edit_timeline_menu.addAction(self.edit_timeline_properties_action)

        self.edit_timeline_events_action = QAction(
            "Edit Events of Selected Timeline",
            self.window,
            triggered=self.edit_timeline_events,
            enabled=True,
        )
        edit_timeline_menu.addAction(self.edit_timeline_events_action)

        select_next_timeline_action = QAction(
            "Select Next Timeline",
            self.window,
            shortcut=Qt.Key.Key_Down,
            triggered=partial(self.select_cycle_timeline, 1),
            enabled=True,
        )
        edit_timeline_menu.addAction(select_next_timeline_action)

        select_previous_timeline_action = QAction(
            "Select Previous Timeline",
            self.window,
            shortcut=Qt.Key.Key_Up,
            triggered=partial(self.select_cycle_timeline, -1),
            enabled=True,
        )
        edit_timeline_menu.addAction(select_previous_timeline_action)

        move_timeline_top_action = QAction(
            "Move Timeline To Top",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.SHIFT | Qt.Modifier.CTRL | Qt.Key.Key_Up
            ),
            triggered=partial(self.move_timeline, -inf),
            enabled=True,
        )
        edit_timeline_menu.addAction(move_timeline_top_action)

        move_timeline_up_action = QAction(
            "Move Timeline Up",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Up),
            triggered=partial(self.move_timeline, -1),
            enabled=True,
        )
        edit_timeline_menu.addAction(move_timeline_up_action)

        move_timeline_down_action = QAction(
            "Move Timeline Down",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Down),
            triggered=partial(self.move_timeline, 1),
            enabled=True,
        )
        edit_timeline_menu.addAction(move_timeline_down_action)

        move_timeline_bottom_action = QAction(
            "Move Timeline To The Bottom",
            self.window,
            shortcut=QKeySequence(
                Qt.Modifier.SHIFT | Qt.Modifier.CTRL | Qt.Key.Key_Down
            ),
            triggered=partial(self.move_timeline, inf),
            enabled=True,
        )
        edit_timeline_menu.addAction(move_timeline_bottom_action)

        # Edit Occurrence submenu
        edit_occurrence_menu = menu.addMenu("&Occurrence")

        self.add_occurrence_action = QAction(
            "Start Occurrence",
            self.window,
            shortcuts=[Qt.Key.Key_Return, Qt.Key.Key_Enter],
            triggered=self.add_occurrence,
            enabled=False,
        )
        edit_occurrence_menu.addAction(self.add_occurrence_action)

        self.abort_occurrence_creation_action = QAction(
            "Abort Creation of Occurrence",
            self.window,
            shortcut=Qt.Key.Key_Escape,
            triggered=self.abort_occurrence_creation,
            enabled=False,
        )
        edit_occurrence_menu.addAction(self.abort_occurrence_creation_action)

        self.delete_occurrence_action = QAction(
            "Delete Occurrence",
            self.window,
            shortcuts=[Qt.Key.Key_Backspace, Qt.Key.Key_Delete],
            triggered=self.delete_occurrence,
            enabled=True,
        )
        edit_occurrence_menu.addAction(self.delete_occurrence_action)

        self.select_previous_occurence_action = QAction(
            "Select Previous Occurrence ",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.ALT | Qt.Key.Key_Left),
            triggered=partial(self.select_occurrence, "previous"),
            enabled=True,
        )
        edit_occurrence_menu.addAction(self.select_previous_occurence_action)

        self.select_next_occurence_action = QAction(
            "Select Next Occurrence ",
            self.window,
            shortcut=QKeySequence(Qt.Modifier.ALT | Qt.Key.Key_Right),
            triggered=partial(self.select_occurrence, "next"),
            enabled=True,
        )
        edit_occurrence_menu.addAction(self.select_next_occurence_action)

    def new_timeline(self, where, checked=False):
        self.window.time_pane.new_timeline(where)

    def add_occurrence(self):
        self.window.time_pane.handle_occurrence()

    def select_cycle_timeline(self, delta, checked=False):
        self.window.time_pane.select_cycle_timeline(delta)

    def move_timeline(self, delta, checked=False):
        self.window.time_pane.move_timeline(delta)

    def abort_occurrence_creation(self):
        self.window.time_pane.abort_occurrence_creation()

    def delete_occurrence(self):
        self.window.time_pane.delete_occurrence()

    def create_data_menu(self):
        menu = self.menu_bar.addMenu("&Data")
        csv_delimiter_action = QAction(
            "Change CSV Delimiter",
            self.window,
            triggered=self.window.files.change_csv_delimiter,
        )
        menu.addAction(csv_delimiter_action)
        set_coder_action = QAction(
            "Set Coder",
            self.window,
            triggered=self.set_coder,
        )
        menu.addAction(set_coder_action)
        self.video_inclusion_exclusion_action = QAction(
            "Exclude video from project file at next save",
            self.window,
            triggered=self.window.files.toggle_video_inclusion,
        )
        menu.addAction(self.video_inclusion_exclusion_action)

    def set_coder(self):
        self.window.files.coders.set_current()

    def select_occurrence(self, direction, checked=False):
        self.window.time_pane.select_occurrence(direction)

    def create_view_menu(self):
        # Add actions to view menu
        menu = self.menu_bar.addMenu("&View")
        self.fullscreen_action = QAction(
            self.style.standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton),
            "Toggle Fullscreen",
            self.window,
            shortcut=Qt.Key.Key_F11,
            triggered=self.window.on_fullscreen,
        )

        menu.addAction(self.fullscreen_action)

    def create_help_menu(self):
        # Help menu
        menu = self.menu_bar.addMenu("&Help")

        self.about_action = QAction(
            "About Felyx",
            self.window,
            triggered=self.about,
        )
        menu.addAction(self.about_action)

        self.visit_pypi_action = QAction(
            "Visit PyPI project",
            self.window,
            triggered=partial(self.open_url, PYPI_URL),
        )
        menu.addAction(self.visit_pypi_action)

        self.visit_repository_action = QAction(
            "Visit Git repository",
            self.window,
            triggered=partial(self.open_url, REPOSITORY_URL),
        )
        menu.addAction(self.visit_repository_action)

    def about(self):
        About(self.window).exec()

    def open_url(self, url, checked=False):
        qurl = QUrl(url)
        if not QDesktopServices.openUrl(qurl):
            QMessageBox.warning(
                self.window, "Open Url", f"Could not open url '{url}'"
            )

    def start_occurence(self):
        self.toggle_occurrence_menu("start")

    def finish_occurence(self):
        self.toggle_occurrence_menu("finish")

    def toggle_occurrence_menu(self, action):
        self.add_occurrence_action.setText(
            "Finish Occurence" if action == "start" else "Start  Occurence"
        )
        self.abort_occurrence_creation_action.setEnabled(action == "start")
        self.delete_occurrence_action.setEnabled(action == "finish")

    def edit_timeline_properties(self):
        self.window.time_pane.selected_timeline.edit_properties()

    def edit_timeline_events(self):
        self.window.time_pane.selected_timeline.edit_events()
