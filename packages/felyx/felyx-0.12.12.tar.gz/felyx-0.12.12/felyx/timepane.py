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

import pandas as pd
from math import (
    ceil,
    floor,
    inf,
    isinf,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QColor,
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QAbstractSlider,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QMessageBox,
    QScrollBar,
    QStyle,
)
from .constants import (
    CSV_HEADERS,
    EVENT_DEFAULT_COLOR,
    MINIMUM_ZOOM_FACTOR,
    TIMELINE_HEIGHT,
    TIME_SCALE_HEIGHT,
    ZOOM_STEP,
)
from .event import (
    ChooseEvent,
    Event,
    EventCollection,
)
from .message import ConfirmMessageBox
from .occurrence import (
    Occurrence,
    OccurrenceHandle,
)
from .timeline import (
    Timeline,
    TimelinePropertiesDialog,
)
from .timescale import TimeScale


class TimePaneView(QGraphicsView):

    def __init__(self, window):
        super().__init__(window)
        self.zoom_step = ZOOM_STEP
        self.zoom_shift = None
        self.zoom_factor = MINIMUM_ZOOM_FACTOR
        self.window = window
        self.create_ui()

    def create_ui(self):
        vertical_scrollbar = QScrollBar(Qt.Orientation.Vertical, self)
        vertical_scrollbar.valueChanged.connect(
            self.on_vertical_scroll_value_changed
        )
        self.setVerticalScrollBar(vertical_scrollbar)

        self.horizontalScrollBar().valueChanged.connect(
            self.on_horizontal_scroll_value_changed
        )

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # This is necessary for getting the cursor being updated
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.scene = TimePaneScene(self)
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(self.scene)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not self.window.has_media():
                return
            mouse_pos = self.mapToScene(event.position().toPoint()).x()
            if event.angleDelta().y() > 0:
                self.zoom_shift = mouse_pos * (1 - self.zoom_step)
                self.zoom_in()
            else:
                self.zoom_shift = mouse_pos * (1 - 1 / self.zoom_step)
                self.zoom_out()
            self.zoom_shift = None
        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.angleDelta().y() > 0:
                action = QAbstractSlider.SliderSingleStepAdd
            else:
                action = QAbstractSlider.SliderSingleStepSub
            self.horizontalScrollBar().triggerAction(action)
        else:
            super().wheelEvent(event)

    def on_vertical_scroll_value_changed(self, value):
        """Allow the time scale to be always visible when scrolling"""
        if self.scene.time_pane.time_scale:
            self.scene.time_pane.time_scale.setPos(0, value)

    def on_horizontal_scroll_value_changed(self):
        self.scene.time_pane.put_cursor_in_view_port()

    def zoom_in(self):
        self.zoom_factor += 1
        self.update_scale()

    def zoom_out(self):
        self.zoom_factor = max([MINIMUM_ZOOM_FACTOR, self.zoom_factor - 1])
        self.update_scale()

    def update_scale(self):
        # Update the size of the scene with zoom_factor
        self.scene.setSceneRect(
            0,
            0,
            self.width() * (self.zoom_step**self.zoom_factor),
            self.scene.height(),
        )
        if self.zoom_shift:
            self.translate_view(self.zoom_shift)
        self.scene.time_pane.put_cursor_in_view_port()

    def translate_view(self, dx):
        previous_anchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.translate(dx, 0)
        self.setTransformationAnchor(previous_anchor)

    def resizeEvent(self, event):
        if self.window.video.media:
            origin = self.mapToScene(0, 0).x()
            width_before = self.scene.width() / (
                self.zoom_step**self.zoom_factor
            )
            width_after = self.width()
            shift = origin * (1 - width_after / width_before)
            self.update_scale()
            self.translate_view(shift)
        else:
            self.scene.setSceneRect(
                0,
                0,
                self.width(),
                self.scene.height(),
            )
        self.update()
        super().resizeEvent(event)


class TimePaneScene(QGraphicsScene):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.sceneRectChanged.connect(self.on_scene_changed)
        self.create_time_pane()

    def create_time_pane(self):
        self.time_pane = TimePane(self)
        self.time_pane.setY(TIME_SCALE_HEIGHT)
        self.addItem(self.time_pane)

    def on_scene_changed(self, rect):
        self.time_pane.on_change(rect)

    def get_view_pos(self):
        return self.view.mapToScene(0, 0).x()


class TimePane(QGraphicsRectItem):

    def __init__(self, scene):
        """Initialize the time pane graphics item"""
        super().__init__()
        self._length = 0
        self._position = 0

        self.selected_timeline = None
        self.occurrence_under_creation: Occurrence = None
        self.scene = scene
        self.view = scene.view
        self.window = self.view.window
        self.time_scale = None
        self.data_needs_save = False
        self.scrollbar_width = self.window.style().pixelMetric(
            QStyle.PM_ScrollBarExtent
        )

    def on_change(self, rect):
        # Update occurrences
        for timeline in self.timelines():
            timeline.update_rect_width(rect.width())
            for occurrence in timeline.occurrences():
                occurrence.update_rect()

        if self.occurrence_under_creation:
            self.occurrence_under_creation.update_rect()

        # Update time scale display
        if self.time_scale:
            # Update cursor
            if self.length:
                self.set_cursor_position(self.position, rect.width())
            self.time_scale.update_rect()

    def set_cursor_position(self, position, width):
        self.time_scale.cursor.setX(
            (position + 0.5) * width / (self.length + 1)
        )

    def select_cycle_timeline(self, delta):
        timelines = self.timelines()
        i, n = self.find_selected_timeline()
        selected_timeline = timelines[i]
        selected_timeline.select = False
        if delta > 0:
            if i == n - 1:
                i = -1
        else:
            if i == 0:
                i = n
        i += delta
        self.select_timeline(timelines[i])

    def find_selected_timeline(self):
        timelines = self.timelines()
        n = len(timelines)
        for i in range(n):
            if timelines[i].select:
                break
        return i, n

    def select_timeline(self, line):
        for tl in self.timelines():
            tl.select = False
        line.select = True
        self.occurrence_borders()
        line.update()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if position != self._position:
            view_begin, view_end = self.get_view_bounds()
            position = min([self.length, max([0, position])])
            if position <= view_begin:
                dx = view_begin - ceil(position)
                if dx > view_begin:
                    dx = view_begin
                self.translate_view(dx)
            elif position + 1 > view_end:
                dx = ceil(position) - view_end + 1
                if dx > self.length - view_end:
                    dx = self.length - view_end
                self.translate_view(-dx)
            self._position = position

            # First, update the occurrence under creation, if it exists. If
            # the cursor position goes beyond the allowed bounds, bring it
            # back and do not update the other widgets.
            ouc = self.occurrence_under_creation
            if ouc:
                if ouc.lower_bound and self._position < ouc.lower_bound:
                    self._position = ouc.lower_bound
                elif ouc.upper_bound and self._position > ouc.upper_bound:
                    self._position = ouc.upper_bound
                    if (
                        self.window.video.playback_state()
                        == QMediaPlayer.PlaybackState.PlayingState
                    ):
                        self.window.media_player_pause()
                ouc.update_end_position(self._position)

            # Cope with the selected occurrence
            for ocr in self.scene.selectedItems():
                if isinstance(ocr, Occurrence):
                    self._position = ocr.adjust_position_to_bounding_interval(
                        self._position
                    )
                    break

            # Set position of video
            self.window.video.position = (
                self._position * self.window.frame_duration()
            )

            # Update focused occurrence handle
            if isinstance(self.scene.focusItem(), OccurrenceHandle):
                occurrence_handle: OccurrenceHandle = self.scene.focusItem()
                self._position = occurrence_handle.change_position(
                    self._position
                )
                self.data_needs_save = True

            # Update cursor position
            if self.time_scale.cursor:
                self.set_cursor_position(self._position, self.scene.width())

            self.occurrence_borders()
            self.view.update()

    def get_view_bounds(self):
        factor = (self.length + 1) / self.scene.width()
        begin = self.scene.get_view_pos() * factor
        end = begin + self.scene.view.width() * factor
        return begin, end

    def translate_view(self, dx):
        self.scene.view.translate_view(
            dx * self.scene.width() / (self.length + 1)
        )

    def put_cursor_in_view_port(self):
        view_begin, view_end = self.get_view_bounds()
        if self.position < view_begin:
            self.position = ceil(view_begin)
        if self.position > view_end:
            self.position = floor(view_end)

    def occurrence_borders(self):
        # Change appearance of occurrence under the cursor
        # (Brute force approach; this ought to be improved)
        if not self.occurrence_under_creation:
            for tml in self.timelines():
                for ocr in tml.occurrences():
                    ocr.pen_width_off()
                    if tml.select:
                        if ocr.is_inside(self.position):
                            ocr.pen_width_on()

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if length != self._length:
            self._length = length
            # Recreate time pane scale and the cursor
            self.time_scale = TimeScale(self)
            self.scene.addItem(self.time_scale)
            self.view.update()

    def clear(self):
        # Clear graphics scene
        self.scene.clear()

    def handle_occurrence(self):
        """Handle the occurrence"""
        menu = self.window.menu

        focus_item = self.scene.focusItem()
        if isinstance(focus_item, OccurrenceHandle):
            focus_item.occurrence.setSelected(False)
        elif self.occurrence_under_creation is None:
            if self.selected_timeline.can_create_occurrence(self.position):
                self.occurrence_under_creation = Occurrence(
                    self.selected_timeline,
                    self.position,
                    self.position,
                )
            menu.start_occurence()
        else:
            # Finish the current occurrence
            events_dialog = ChooseEvent(
                self.selected_timeline.event_collection, self.view
            )
            events_dialog.exec()
            if events_dialog.result() == QMessageBox.DialogCode.Accepted:
                event = events_dialog.get_chosen()
                self.occurrence_under_creation.set_event(event)
                self.occurrence_under_creation.finish_creation()
                self.occurrence_under_creation = None
                self.occurrence_borders()
                menu.finish_occurence()
                self.data_needs_save = True
            self.view.update()

    def new_timeline(self, where):
        if not isinf(where):
            order = self.selected_timeline.order
            if where < 0:
                where = order - 0.5
            else:
                where = order + 0.5
        timeline = Timeline("", where, "", self)
        dialog = TimelinePropertiesDialog(timeline)
        dialog.exec()
        if dialog.result() == QMessageBox.DialogCode.Accepted:
            name = dialog.get_name()
            if not self.check_new_timeline_name(name):
                self.delete_timeline(timeline)
                return
            timeline.name = name
            timeline.description = dialog.get_description()
            self.add_timeline(timeline)
            self.place_timelines()
            self.data_needs_save = True

    def check_new_timeline_name(self, name):
        if name == "":
            QMessageBox.warning(
                self.window, "Warning", "Timeline name cannot be empty"
            )
            return False
        if name in self.get_timeline_names():
            QMessageBox.warning(
                self.window,
                "Warning",
                f'A timeline with name "{name}" exists already',
            )
            return False
        return True

    def abort_occurrence_creation(self):
        if self.occurrence_under_creation is not None:
            confirm_box = ConfirmMessageBox(
                "Warning", "Abort creation of occurrence?", self.window
            )
            if confirm_box.answer:
                self.occurrence_under_creation.remove()
                self.occurrence_under_creation = None
                self.view.update()
                self.window.menu.start_occurence()

    def add_timeline(self, timeline):
        # Set the timeline rectangle
        timeline.update_rect()

        # Select the new timeline
        for i in self.timelines():
            i.select = False
        timeline.select = True

        self.view.update_scale()

    def place_timelines(self):
        order = 0
        for i in self.timelines():
            i.order = order
            order += 1
        timelines = self.timelines()
        for timeline in timelines:
            timeline.setPos(0, timeline.order * TIMELINE_HEIGHT)

        # Adjust the height of of the scene
        rect = self.scene.sceneRect()
        height = len(self.timelines()) * TIMELINE_HEIGHT + TIME_SCALE_HEIGHT
        rect.setHeight(height)
        self.scene.setSceneRect(rect)

        # Set maximum height of the widget
        self.view.setMaximumHeight(int(height) + self.scrollbar_width + 2)

    def move_timeline(self, delta):
        if isinf(delta):
            if delta < 0:
                self.selected_timeline.order = -1
            else:
                self.selected_timeline.order = len(self.timelines())
        else:
            self.selected_timeline.order += delta * 1.5
        self.place_timelines()

    def add_data(self, data):
        fd = self.window.frame_duration()
        for _, row in data.iterrows():
            # Search for timeline
            timeline = self.get_timeline_by_name(str(row["timeline"]))

            # If timeline from csv doesn't exist in TimePane,
            # escape row
            if not timeline:
                continue

            # Search for event
            event = timeline.event_collection.get_event(str(row["event"]))

            # If event from csv doesn't exist in timeline,
            # then add it
            if not event:
                continue

            occurrence = Occurrence(
                timeline,
                round(row["begin"] / fd),
                round(row["end"] / fd) - 1,
                str(row["comment"]),
            )

            occurrence.set_event(event)
            occurrence.finish_creation()

    def get_timeline_by_name(self, name):
        """Get the timeline by name"""
        return next((x for x in self.timelines() if x.name == name), None)

    def has_occurrences(self) -> bool:
        return any(len(line.occurrences()) for line in self.timelines())

    def delete_occurrence(self):
        for i in self.scene.selectedItems():
            if isinstance(i, Occurrence):
                i.on_remove()
                break

    def timelines_from_config(self, config):
        for timeline in self.timelines():
            del timeline
        if "timelines" in config:

            # Set all absent order fields with Inf
            for k, v in config["timelines"].items():
                if not v:
                    v = dict()
                    config["timelines"][k] = v
                if "order" not in v:
                    v["order"] = -inf
                if "description" not in v:
                    v["description"] = ""

            # Sort according to order first and alphabetically from
            # timeline name, otherwise from the "order" property In the
            # loop below, the "order" attribute of the Timeline items will
            # receiving increasing nteger values, starting at zero.
            order = 0
            for item in sorted(
                config["timelines"].items(),
                key=lambda x: (x[1]["order"], x[0]),
            ):
                # Get name and properties of the timeline
                name = item[0]
                properties = item[1]
                description = properties["description"]

                # Create timeline
                line = Timeline(name, order, description, self)
                order += 1

                # Add the timeline to the TimePane
                self.add_timeline(line)

                # Loop over events of the timeline
                event_collection = EventCollection()
                if "events" in properties:
                    for k, v in properties["events"].items():
                        event = Event(k)
                        try:
                            event.color = QColor(v["color"])
                        except KeyError:
                            event.color = EVENT_DEFAULT_COLOR
                        try:
                            event.description = v["description"]
                        except KeyError:
                            event.description = ""
                        event_collection.add_event(event)
                    line.event_collection = event_collection

            self.place_timelines()

        self.on_change(self.scene.sceneRect())

    def timelines_to_dataframe(self):
        df = pd.DataFrame(columns=CSV_HEADERS)
        fd = self.window.frame_duration()
        for timeline in sorted(self.timelines(), key=lambda x: x.name):
            for occurrence in timeline.occurrences():
                comment = occurrence.comment.replace('"', '\\"')
                row = [
                    timeline.name,
                    occurrence.event.name,
                    f"{fd * occurrence.begin_position:.3f}",
                    f"{fd * (occurrence.end_position + 1):.3f}",
                    comment,
                ]
                df.loc[len(df.index)] = row
        return df

    def timelines(self):
        # Always return a list sorted by order
        return sorted(
            [x for x in self.childItems() if isinstance(x, Timeline)],
            key=lambda x: x.order,
        )

    def delete_timeline(self, timeline):
        # If the timeline to delted is the selected one, select the next one
        if self.selected_timeline == timeline:
            timelines = self.timelines()
            new_selected = None
            for i in timelines:
                if i.order > timeline.order:
                    new_selected = i
                    break
            if not new_selected:
                new_selected = timelines[0]
            new_selected.select = True
        self.scene.removeItem(timeline)
        self.place_timelines()
        del timeline
        self.data_needs_save = True

    def get_timeline_names(self):
        return [x.name for x in self.timelines()]

    def select_occurrence(self, direction):
        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            occurrence = selected_items[0]
            timeline = occurrence.timeline
            timeline.select_occurrence(occurrence, direction)
