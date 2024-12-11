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

from math import floor, ceil, log10
from numpy import arange

from PySide6.QtCore import (
    QPointF,
    QRectF,
    Qt,
)
from PySide6.QtWidgets import (
    QGraphicsRectItem,
)
from PySide6.QtGui import QFontMetrics

from .constants import (
    TICK_LOCATOR_MIN_GAP,
    TIME_SCALE_HEIGHT,
)
from .cursor import Cursor


class TimeScale(QGraphicsRectItem):

    def __init__(self, time_pane):
        super().__init__()
        self.time_pane = time_pane
        self.cursor = Cursor(self)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), TIME_SCALE_HEIGHT)
        )

    def paint(self, painter, option, widget=...):
        self.draw_rect(painter)

        if self.time_pane.length != 0:
            self.draw_scale(painter)

    def update_rect(self):
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), TIME_SCALE_HEIGHT)
        )
        self.update()

    def draw_rect(self, painter):
        """Draw the background rectangle of the timeline scale"""
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.lightGray)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), TIME_SCALE_HEIGHT)
        )
        painter.drawRect(self.rect())

    def draw_scale(self, painter):
        tl = TickLocator()
        tp = self.time_pane
        dur = (tp.length + 1) * tp.window.frame_duration()
        wid = self.time_pane.scene.width()
        font = painter.font()
        fm = QFontMetrics(font)
        loc = tl.find_locations(0, dur / 1000, wid, fm)
        # Compute the height of the text
        font_height = fm.height()
        line_height = 5
        y = self.rect().height()

        for p in loc:

            i = 1000 * (p[0] * wid / dur)

            # Compute the position of the text
            text_width = fm.boundingRect(p[1]).width()
            text_position = QPointF(i - text_width / 2, font_height)

            # Draw the text
            painter.drawText(text_position, p[1])

            # Compute the position of the line
            painter.drawLine(QPointF(i, y), QPointF(i, y - line_height))

    def mousePressEvent(self, event):
        # Compute the time of the position click
        tp = self.time_pane
        position = round(
            event.scenePos().x() * (tp.length + 1) / tp.scene.width()
        )

        self.time_pane.position = position

    def mouseReleaseEvent(self, event):
        return


class TickLocator:
    def find_locations(self, tmin, tmax, width, font_metric):
        """Arguments:\
    tmin: minimum time in the timescale (in seconds)
    tmax: maximum time in the timescale (in seconds)
    width: width of the timeline (in pixels)
    font_metric: Metric of QFont to be used

Value: list of [location, label] lists
"""
        gap_prev = None
        delta_prev = None
        delta = 1
        while True:
            imax = delta * floor(tmax / delta)
            imin = delta * ceil(tmin / delta)
            nb_int_digit = floor(log10(imax)) + 1
            nb_dec_digit = floor(log10(delta))
            if nb_int_digit > 0:
                label = "0" * nb_int_digit
            else:
                label = "0"
            if nb_dec_digit < 0:
                label += "." + "0" * -nb_dec_digit
            text_width = (
                font_metric.boundingRect(label).width() * (tmax - tmin) / width
            )
            gap = (delta - text_width) / text_width
            if gap >= TICK_LOCATOR_MIN_GAP:
                if gap_prev and gap_prev < TICK_LOCATOR_MIN_GAP:
                    break
                else:
                    delta_prev = delta
                    delta = self.change(delta, "decrease")
            else:
                if gap_prev and gap_prev >= TICK_LOCATOR_MIN_GAP:
                    delta = delta_prev
                    break
                else:
                    delta_prev = delta
                    delta = self.change(delta, "increase")
            gap_prev = gap
        retval = []
        fmt = f"{{:.{max([0, -floor(log10(delta))])}f}}"
        for t in arange(imin, imax + delta, delta):
            label = fmt.format(t)
            label_width = (
                font_metric.boundingRect(label).width() * (tmax - tmin) / width
            )
            if (t - label_width / 2 > tmin) and (t + label_width / 2 < tmax):
                retval.append([t, label])
        return retval

    def change(self, delta, direction):
        logdelta = log10(delta)
        factor = 10 ** floor(logdelta)
        last = round(10**logdelta / factor)
        if direction == "decrease":
            if last == 1:
                last = 0.5
            else:
                if last == 2:
                    last = 1
                else:
                    last = 2
        else:
            if last == 1:
                last = 2
            else:
                if last == 2:
                    last = 5
                else:
                    last = 10
        return factor * last
