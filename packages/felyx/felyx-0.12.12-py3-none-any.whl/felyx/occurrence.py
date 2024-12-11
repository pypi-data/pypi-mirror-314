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
    QRectF,
)
from PySide6.QtGui import (
    QAction,
    QPen,
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
)

from .constants import (
    OCCURRENCE_PEN_COLOR,
    OCCURRENCE_BG_COLOR,
    OCCURRENCE_PEN_WIDTH_OFF_CURSOR,
    OCCURRENCE_PEN_WIDTH_ON_CURSOR,
    OCCURRENCE_HANDLE_WIDTH,
    OCCURRENCE_HANDLE_HEIGHT_FRACTION,
    TIMELINE_HEIGHT,
    TIMELINE_TITLE_HEIGHT,
)
from .event import ChooseEvent
from .message import ConfirmMessageBox
from .textedit import TextEdit
from .utils import color_fg_from_bg


class Occurrence(QGraphicsRectItem):

    def __init__(
        self,
        timeline,
        begin_position: int,
        end_position: int,
        comment: str = "",
    ):
        """Initializes the Occurrence widget"""
        super().__init__(timeline)
        self.pen: QPen = QPen()
        self.pen_width_off()
        self.brush_color = OCCURRENCE_BG_COLOR
        self.pen_color = OCCURRENCE_PEN_COLOR
        self.event = None
        self.timeline = timeline
        self.time_pane = timeline.time_pane
        self.begin_position = begin_position
        self.end_position = end_position
        self.begin_handle: OccurrenceHandle = None
        self.end_handle: OccurrenceHandle = None
        self.comment = comment
        factor = self.time_pane.scene.width() / (self.time_pane.length + 1)
        self.set_rect(
            self.begin_position * factor,
            (self.end_position + 1) * factor,
        )
        self.get_bounds()

    def set_rect(self, x_begin, x_end):
        self.setRect(
            QRectF(
                0,
                0,
                x_end - x_begin,
                TIMELINE_HEIGHT - TIMELINE_TITLE_HEIGHT,
            )
        )
        self.setX(x_begin)
        self.setY(TIMELINE_TITLE_HEIGHT)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.time_pane.occurrence_under_creation:
                self.setSelected(True)
                self.get_bounds()

    def mouseReleaseEvent(self, event):
        return

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if self.time_pane.occurrence_under_creation is None:
            can_merge_previous = False
            for occurrence in self.timeline.occurrences():
                if (
                    occurrence.end_position + 1 == self.begin_position
                    and self.event == occurrence.event
                ):
                    can_merge_previous = True
                    break
            can_merge_next = False
            for occurrence in self.timeline.occurrences():
                if (
                    self.end_position + 1 == occurrence.begin_position
                    and self.event == occurrence.event
                ):
                    can_merge_next = True
                    break
            menu = QMenu()
            menu.addAction(
                QAction(
                    "Delete Occurrence",
                    self.time_pane.window,
                    shortcuts=[Qt.Key.Key_Backspace, Qt.Key.Key_Delete],
                    triggered=self.on_remove,
                )
            )
            menu.addAction("Change occurrence event").triggered.connect(
                self.change_event
            )
            if can_merge_previous:
                menu.addAction(
                    "Merge with previous occurrence"
                ).triggered.connect(self.merge_previous)
            if can_merge_next:
                menu.addAction("Merge with next occurrence").triggered.connect(
                    self.merge_next
                )
            menu.addAction("Comment occurrence").triggered.connect(
                self.edit_comment
            )
            try:
                pos = event.screenPos()
            except AttributeError:
                # Got here via keyPresEvent
                window = self.time_pane.window
                pos = QPoint(int(window.width() / 2), int(window.height() / 2))
            menu.exec(pos)

    def on_remove(self):
        dialog = ConfirmMessageBox(
            "Confirmation",
            "Do you want to remove the occurrence?",
            self.time_pane.window,
        )
        if dialog.answer():
            self.remove()

    def edit_comment(self):
        comment_dialog = OccurrenceComment(self.comment, self.time_pane.window)
        comment_dialog.exec()
        if comment_dialog.result() == QMessageBox.DialogCode.Accepted:
            comment = comment_dialog.get_text()
            if self.comment != comment:
                self.comment = comment
                self.setToolTip(self.comment)
                self.time_pane.data_needs_save = True

    def merge_previous(self):
        for occurrence in self.timeline.occurrences():
            if (
                self.begin_position == occurrence.end_position + 1
                and self.event == occurrence.event
            ):
                break
        self.begin_position = occurrence.begin_position
        occurrence.remove()
        self.update_rect()

    def merge_next(self):
        for occurrence in self.timeline.occurrences():
            if (
                self.end_position + 1 == occurrence.begin_position
                and self.event == occurrence.event
            ):
                break
        self.end_position = occurrence.end_position
        occurrence.remove()
        self.update_rect()

    def change_event(self):
        events_dialog = ChooseEvent(
            self.timeline.event_collection, self.timeline.time_pane.view
        )
        events_dialog.exec()
        if events_dialog.result() == QMessageBox.DialogCode.Accepted:
            event = events_dialog.get_chosen()
            if event != self.event:
                self.set_event(event)
                self.update()
                self.time_pane.data_needs_save = True

    def remove(self):
        self.time_pane.scene.removeItem(self)
        self.time_pane.data_needs_save = True
        del self

    def paint(self, painter, option, widget=None):
        # Draw the occurrence rectangle
        self.draw_rect(painter)

        # Draw the name of the occurrence in the occurrence rectangle
        self.draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def draw_rect(self, painter):
        """Draw the occurrence rectangle"""
        painter.setPen(self.pen)
        painter.setBrush(self.brush_color)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def draw_name(self, painter):
        """Draws the name of the occurrence"""
        if self.event:
            col = color_fg_from_bg(self.brush_color)
            painter.setPen(col)
            painter.setBrush(col)
            tp = self.time_pane
            begin, end = tp.get_view_bounds()
            rect = self.rect()
            factor = tp.scene.width() / (tp.length + 1)
            if begin > self.begin_position:
                dx = begin - self.begin_position
            else:
                dx = 0
            if end < self.end_position + 1:
                width = end - self.begin_position - dx + 1
            else:
                width = self.end_position - self.begin_position - dx + 1
            rect.setX(dx * factor)
            rect.setWidth(width * factor)
            painter.drawText(
                rect, Qt.AlignmentFlag.AlignCenter, self.event.name
            )

    def set_event(self, event=None):
        """Updates the event"""
        if event is None:
            self.event = None
            self.brush_color = OCCURRENCE_BG_COLOR
        else:
            self.event = event
            # FIXME: Put "(no comment)" in constants.py
            self.setToolTip(
                self.comment if self.comment != "" else "(no comment)"
            )
            self.update_style()

    def update_style(self):
        color = self.event.color
        self.brush_color = color
        if self.begin_handle:
            self.begin_handle.setBrush(color)
            self.end_handle.setBrush(color)

    def update_rect(self):
        new_rect = self.time_pane.scene.sceneRect()
        # Calculate position to determine width
        factor = new_rect.width() / (self.time_pane.length + 1)

        # Update the rectangle
        rect = self.rect()

        if self.end_position >= self.begin_position:
            begin_x_position = self.begin_position * factor
            end_x_position = (self.end_position + 1) * factor
        else:
            begin_x_position = (self.begin_position + 1) * factor
            end_x_position = self.end_position * factor
        self.setX(begin_x_position)
        rect.setWidth(end_x_position - begin_x_position)
        self.setRect(rect)

        if self.begin_handle:
            self.begin_handle.setX(self.rect().x())
            self.end_handle.setX(self.rect().width())

        self.update()

    def update_begin_position(self, begin_position: int):
        self.begin_position = begin_position
        self.update_rect()

    def update_end_position(self, end_position: int):
        """Updates the end position"""
        self.end_position = end_position
        self.update_rect()

    def finish_creation(self):
        """Finish the creation of the occurrence"""
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

        self.begin_handle = OccurrenceBeginHandle(self)
        self.end_handle = OccurrenceEndHandle(self)

        # if begin_position is greater than end_position then swap positions
        if self.begin_position > self.end_position:
            self.begin_position, self.end_position = (
                self.end_position,
                self.begin_position,
            )
            self.update_rect()

        self.update()

    def show_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(True)
        if self.end_handle:
            self.end_handle.setVisible(True)

    def hide_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(False)
        if self.end_handle:
            self.end_handle.setVisible(False)

    def get_bounds(self):
        lower_bound = 0
        upper_bound = self.timeline.time_pane.length
        # Loop through the occurrences of the associated timeline
        for a in self.timeline.occurrences():
            if a != self:
                if a.end_position <= self.begin_position:
                    lower_bound = max([lower_bound, a.end_position + 1])
                if a.begin_position >= self.end_position:
                    upper_bound = min([upper_bound, a.begin_position - 1])
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def adjust_position_to_bounding_interval(self, position) -> int:
        if self.lower_bound and position < self.lower_bound:
            position = self.lower_bound
        elif self.upper_bound and position > self.upper_bound:
            position = self.upper_bound
            self.time_pane.window.media_player_pause()
        return position

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Menu:
            self.contextMenuEvent(event)

    def is_inside(self, position):
        return position >= self.begin_position and position <= self.end_position

    def pen_width_off(self):
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_OFF_CURSOR)
        self.setPen(self.pen)

    def pen_width_on(self):
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_ON_CURSOR)
        self.setPen(self.pen)


class OccurrenceHandle(QGraphicsRectItem):

    def __init__(self, occurrence: Occurrence):
        super().__init__(occurrence)
        self.occurrence = occurrence

        self.pen: QPen = QPen(self.occurrence.pen_color)
        self.pen_width_off()
        self.setBrush(self.occurrence.brush_color)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)
        self.set_rect()

    def set_rect(self):
        height = (
            OCCURRENCE_HANDLE_HEIGHT_FRACTION * self.occurrence.rect().height()
        )
        self.setRect(
            QRectF(
                -OCCURRENCE_HANDLE_WIDTH / 2,
                -height / 2,
                OCCURRENCE_HANDLE_WIDTH,
                height,
            )
        )
        self.setY(self.occurrence.rect().height() / 2)

    def pen_width_off(self):
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_OFF_CURSOR)
        self.setPen(self.pen)

    def pen_width_on(self):
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_ON_CURSOR)
        self.setPen(self.pen)

    def focusInEvent(self, event):
        self.occurrence.setSelected(True)
        self.pen_width_on()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.occurrence.setSelected(False)
        self.pen_width_off()
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            ocr = self.occurrence
            tp = ocr.time_pane
            dur = tp.length + 1
            position = event.scenePos().x() * dur / tp.scene.width()
            position = ocr.adjust_position_to_bounding_interval(position)
            tp.position = self.limit_position(position)

    def limit_position(self, position):
        ocr = self.occurrence
        if isinstance(self, OccurrenceBeginHandle):
            et = ocr.end_position
            if position > et - 0.5:
                position = et - 0.5
        else:
            bt = ocr.begin_position
            if position < bt + 0.5:
                position = bt + 0.5
        return position


class OccurrenceBeginHandle(OccurrenceHandle):

    def __init__(self, occurrence: Occurrence):
        super().__init__(occurrence)
        self.setX(0)

    def focusInEvent(self, event):
        self.occurrence.time_pane.position = self.occurrence.begin_position
        super().focusInEvent(event)

    def change_position(self, position):
        position = self.limit_position(position)
        self.occurrence.update_begin_position(position)
        return position


class OccurrenceEndHandle(OccurrenceHandle):
    def __init__(self, occurrence: Occurrence):
        super().__init__(occurrence)
        self.setX(occurrence.rect().width())

    def focusInEvent(self, event):
        self.occurrence.time_pane.position = self.occurrence.end_position
        super().focusInEvent(event)

    def change_position(self, position):
        position = self.limit_position(position)
        self.occurrence.update_end_position(position)
        return position


class OccurrenceComment(QDialog):
    def __init__(self, text="", widget=None):
        super().__init__(widget)
        self.setWindowTitle("Occurrence comment")

        layout = QFormLayout(self)
        self.input = TextEdit(self, text)
        layout.addRow(self.input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_text(self):
        return self.input.toPlainText()
