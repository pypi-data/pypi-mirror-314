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
from PySide6.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    def __init__(self, parent, text):
        super().__init__()
        self.append(text)
        self.parent = parent

    def keyPressEvent(self, event):
        if (
            event.key() == Qt.Key.Key_Return
            and event.modifiers() == Qt.KeyboardModifier.NoModifier
        ):
            self.parent.accept()
        else:
            if event.key() == Qt.Key.Key_Return:
                self.append("")
            else:
                super().keyPressEvent(event)
