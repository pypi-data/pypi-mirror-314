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
    QRectF,
    QLine,
    QPointF,
    QSizeF,
)
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import QGraphicsItem

from .constants import (
    CURSOR_BRUSH_COLOR_DEFAULT,
    CURSOR_BRUSH_COLOR_CREATION,
    CURSOR_HANDLE_WIDTH,
    CURSOR_PEN_COLOR,
    TIME_SCALE_HEIGHT,
)


class Cursor(QGraphicsItem):

    def __init__(self, parent):
        super().__init__(parent)
        self.time_pane = parent.time_pane
        self.pressed = False
        self.poly: QPolygonF = QPolygonF(
            [
                QPointF(-CURSOR_HANDLE_WIDTH, 0),
                QPointF(CURSOR_HANDLE_WIDTH, 0),
                QPointF(0, TIME_SCALE_HEIGHT),
            ]
        )
        # The constant value 10000 below should be enough, in practical terms
        self.line: QLine = QLine(0, TIME_SCALE_HEIGHT, 0, 10000)

        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setZValue(101)

    def paint(self, painter, option, widget=...):
        painter.setPen(CURSOR_PEN_COLOR)
        if self.time_pane.occurrence_under_creation is None:
            painter.setBrush(CURSOR_BRUSH_COLOR_DEFAULT)
        else:
            painter.setBrush(CURSOR_BRUSH_COLOR_CREATION)
        painter.drawLine(self.line)
        painter.drawPolygon(self.poly)

    def calculate_size(self):
        min_x: float = self.poly[0].x()
        max_x: float = self.poly[0].x()

        for i, point in enumerate(self.poly):
            if point.x() < min_x:
                min_x = point.x()
            if point.x() > max_x:
                max_x = point.x()

        return QSizeF(max_x - min_x, TIME_SCALE_HEIGHT)

    def boundingRect(self):
        size: QSizeF = self.calculate_size()
        return QRectF(-CURSOR_HANDLE_WIDTH, 0, size.width(), size.height())

    def focusInEvent(self, event):
        self.pressed = True
        super().focusInEvent(event)
        self.update()

    def focusOutEvent(self, event):
        self.pressed = False
        super().focusOutEvent(event)
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos: QPointF = event.scenePos()
        tp = self.time_pane
        if self.pressed:
            position = pos.x() * (tp.length + 1) / tp.scene.width()

            # During creation of a new occurrence
            if tp and tp.occurrence_under_creation:
                occurrence = tp.occurrence_under_creation
                if position != occurrence.adjust_position_to_bounding_interval(
                    position
                ):
                    # Stop player at the lower or upper bound when they
                    # are passed over
                    self.setPos(self.x(), 0)
                    return

            tp.position = position

            if pos.x() < 0:
                self.setPos(0, 0)
            elif pos.x() > tp.scene.width():
                self.setPos(tp.scene.width(), 0)
            else:
                self.setPos(pos.x(), 0)

        self.update()
