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


from PySide6.QtCore import (
    Qt,
    QPoint,
    QPointF,
    QRectF,
)
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsItem,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from .constants import (
    TIMELINE_MASK_ON_COLOR,
    TIMELINE_MASK_OFF_COLOR,
    TIMELINE_TITLE_HEIGHT,
    TIMELINE_TITLE_BG_COLOR,
    TIMELINE_TITLE_FG_COLOR,
    TIMELINE_HEIGHT,
)
from .event import (
    EventCollection,
    ChangeEvent,
    ChooseEvent,
)
from .message import ConfirmMessageBox
from .occurrence import Occurrence
from .textedit import TextEdit
from .utils import color_fg_from_bg


class Timeline(QGraphicsRectItem):

    def __init__(self, name, order, description, time_pane):
        super().__init__(time_pane)
        self.time_pane = time_pane
        self.event_collection = EventCollection()
        self.title = TimelineTitle(name, self)
        self._name = None
        self.name = name
        self.mask = TimelineMask(self)
        self._select = False
        self._description = None
        self.description = description
        self.order = order
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, select):
        if select != self._select:
            self._select = select
            if select:
                self.time_pane.selected_timeline = self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name != self._name:
            self._name = name
            self.title.text = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description != self._description:
            self._description = description
            if self._description == "":
                self._description = "(no description)"
            self.title.setToolTip(self._description)

    def occurrences(self):
        return sorted(
            [x for x in self.childItems() if isinstance(x, Occurrence)],
            key=lambda x: x.begin_position,
        )

    def update_rect(self):
        rect = QRectF(
            0,
            0,
            self.time_pane.scene.width(),
            TIMELINE_HEIGHT,
        )
        self.setRect(rect)
        self.mask.setRect(rect)

    def update_rect_width(self, new_width: float):
        """Update the width of the timeline"""
        rect = self.rect()
        rect.setWidth(new_width)
        self.setRect(rect)
        self.title.update_rect_width(new_width)
        self.mask.update_rect_width(new_width)

    def on_remove(self):
        if len(self.occurrences()) > 0:
            dialog = ConfirmMessageBox(
                "Confirmation",
                "There are occurrences present. "
                "Do you want to remove this timeline?",
                self.time_pane.window,
            )
            if dialog.answer:
                for ocr in self.occurrences():
                    ocr.remove()
        self.time_pane.delete_timeline(self)

    def edit_properties(self):
        dialog = TimelinePropertiesDialog(self)
        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            is_changed = False
            name = dialog.get_name()
            if self.title.text != name:
                if not self.time_pane.check_new_timeline_name(name):
                    return
                self.name = name
                is_changed = True
            description = dialog.get_description()
            if self.description != description:
                self.description = description
                self.title.setToolTip(self.description)
                is_changed = True
            if is_changed:
                self.time_pane.data_needs_save = True

    def update_occurrences(self):
        for occurrence in self.occurrences():
            occurrence.update_style()

    def edit_events(self):
        while True:
            choose_dialog = ChooseEvent(
                self.event_collection, self.time_pane.view, "Finish"
            )
            choose_dialog.exec()
            if choose_dialog.result() == QMessageBox.DialogCode.Accepted:
                event = choose_dialog.get_chosen()
                name = event.name
                color = event.color
                description = event.description
                change_dialog = ChangeEvent(event, self.time_pane.window, True)
                change_dialog.exec()
                if (
                    change_dialog.result() == QMessageBox.DialogCode.Rejected
                    and change_dialog.request_remove()
                ):
                    self.remove_event(event)
                if (
                    name != event.name
                    or description != event.description
                    or color != event.color
                ):
                    self.update_occurrences()
                    self.time_pane.data_needs_save = True
            if choose_dialog.result() == QMessageBox.DialogCode.Rejected:
                break

        if self.event_collection.is_changed():
            self.time_pane.data_needs_save = True

    def remove_event(self, event):
        if event in set([x.event for x in self.occurrences()]):
            QMessageBox.warning(
                self.time_pane.window,
                "Warning",
                f'Event "{event.name}" cannot be removed because there are '
                "occurrences of it in the timeline",
            )
        else:
            self.event_collection.remove_event(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction(self.time_pane.window.menu.new_timeline_top_action)
        menu.addAction(self.time_pane.window.menu.new_timeline_above_action)
        menu.addAction(self.time_pane.window.menu.new_timeline_below_action)
        menu.addAction(self.time_pane.window.menu.new_timeline_bottom_action)
        menu.addAction("Delete timeline").triggered.connect(self.on_remove)
        menu.addAction("Edit timeline properties").triggered.connect(
            self.edit_properties
        )
        menu.addAction("Edit events").triggered.connect(self.edit_events)
        menu.addAction("Show events summary").triggered.connect(
            self.show_events_summary
        )
        try:
            pos = event.screenPos()
        except AttributeError:
            # Got here via keyPresEvent
            pos = QPoint(
                int(self.time_pane.window.width() / 2),
                int(self.time_pane.window.height() / 2),
            )
        menu.exec(pos)

    def new_timeline(self, where):
        self.time_pane.new_timeline(where)

    def can_create_occurrence(self, time):
        """Check whether an occurrence can be created at given time"""
        # Loop through the occurrences of the selected timeline
        valid = True
        for a in self.occurrences():
            if a.is_inside(time):
                valid = False
                break
        return valid

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Menu:
            self.contextMenuEvent(event)

    def show_events_summary(self):
        window = self.time_pane.window
        dialog = QDialog(window)
        dialog.setWindowTitle("Events summary")
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(QLabel(f'Summary of events in timeline "{self.name}"'))
        table = QTableWidget(sum(1 for _ in self.event_collection), 4)
        table.setHorizontalHeaderLabels(
            ["events", "total time (s)", "count", "description"]
        )
        row = 0
        frame_duration = self.time_pane.window.frame_duration()
        for name in self.event_collection:
            event = self.event_collection.get_event(name)
            bg_color = event.color
            fg_color = color_fg_from_bg(bg_color)
            item = QTableWidgetItem(name)
            item.setBackground(bg_color)
            item.setForeground(fg_color)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(row, 0, item)
            count = 0
            total_time = 0
            for ocr in [x for x in self.occurrences() if x.event == event]:
                total_time += (
                    frame_duration
                    * (ocr.end_position - ocr.begin_position + 1)
                    / 1000
                )
                count += 1
            item = QTableWidgetItem(f"{total_time:.3f}")
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 1, item)
            item = QTableWidgetItem(str(count))
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            table.setItem(row, 2, item)
            table.setItem(row, 3, QTableWidgetItem(event.description))
            row += 1
        table.horizontalHeader().setStretchLastSection(True)
        table.resizeColumnToContents(3)
        layout.addWidget(table)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok,
            window,
        )
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def select_occurrence(self, occurrence, direction):
        occurrences = self.occurrences()
        nb_occurrences = len(occurrences)
        if nb_occurrences > 0:
            idx = None
            for i, ocr in enumerate(occurrences):
                if ocr == occurrence:
                    idx = i
                    break
            occurrences[idx].setSelected(False)
            if direction == "next":
                idx += 1
                if idx == nb_occurrences:
                    idx = 0
            else:
                idx -= 1
                if idx < 0:
                    idx = nb_occurrences - 1
            occurrences[idx].setSelected(True)


class TimelineTitle(QGraphicsRectItem):

    def __init__(self, text: str, parent: Timeline = None):
        super().__init__(parent)
        self.text = text
        rect = parent.rect()
        rect.setHeight(TIMELINE_TITLE_HEIGHT)
        self.setRect(rect)
        self.parent = parent

    def paint(self, painter, option, widget=...):
        # Draw the rectangle
        self.draw_rect(painter)

        # Draw the text
        self.draw_text(painter)

    def draw_rect(self, painter):
        """Draw the timeline title rectangle"""
        # Set Pen and Brush for rectangle
        color = TIMELINE_TITLE_BG_COLOR
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(self.rect())

    def draw_text(self, painter):
        """Draw the timeline title text"""
        color = TIMELINE_TITLE_FG_COLOR
        painter.setPen(color)
        painter.setBrush(color)

        font = painter.font()
        fm = QFontMetrics(font)

        text_width = fm.boundingRect(self.text).width()
        text_height = fm.boundingRect(self.text).height()
        text_descent = fm.descent()

        # Get timeline polygon based on the viewport
        timeline_in_viewport_pos = self.parentItem().time_pane.view.mapToScene(
            self.rect().toRect()
        )

        bounding_rect = timeline_in_viewport_pos.boundingRect()

        # Get the viewport rect
        viewport_rect = self.parentItem().time_pane.view.viewport().rect()

        # Compute the x position for the text
        x_alignCenter = bounding_rect.x() + viewport_rect.width() / 2

        # No idea why the "-2", in the vertical position, is needed here
        text_position = QPointF(
            x_alignCenter - text_width / 2,
            TIMELINE_TITLE_HEIGHT / 2 + text_height / 2 - text_descent - 2,
        )

        painter.drawText(text_position, self.text)

    def update_rect_width(self, new_width):
        rect = self.rect()
        rect.setWidth(new_width)
        self.setRect(rect)


class TimelineMask(QGraphicsRectItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def paint(self, painter, option, widget=...):
        if self.parent.select:
            self.setZValue(-1)
            color = TIMELINE_MASK_ON_COLOR
        else:
            self.setZValue(1)
            color = TIMELINE_MASK_OFF_COLOR
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawRect(self.rect())

    def update_rect_width(self, new_width):
        rect = self.rect()
        rect.setWidth(new_width)
        self.setRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.parent.time_pane.occurrence_under_creation:
                self.parent.time_pane.select_timeline(self.parent)
        event.ignore()


class TimelinePropertiesDialog(QDialog):

    def __init__(self, timeline):
        window = timeline.time_pane.window
        super().__init__(window)
        self.setWindowTitle("Timeline properties")
        layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setText(timeline.name)
        self.name_edit.returnPressed.connect(self.accept)
        layout.addRow("Name: ", self.name_edit)
        layout.addRow("Description:", None)
        self.description_edit = TextEdit(self, timeline.description)
        layout.addRow(self.description_edit)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            window,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_name(self):
        return self.name_edit.text()

    def get_description(self):
        return self.description_edit.toPlainText()
