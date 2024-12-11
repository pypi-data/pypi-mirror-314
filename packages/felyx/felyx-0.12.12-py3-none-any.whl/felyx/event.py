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

from PySide6.QtWidgets import (
    QColorDialog,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
)
from PySide6.QtWidgets import QStyle
from functools import partial

from .assets import Assets
from .constants import EVENT_DEFAULT_COLOR
from .textedit import TextEdit
from .utils import color_fg_from_bg


class Event:

    def __init__(self, name=None, color=None, description=None):
        self._name = name
        self._color = color
        self._description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description


class EventCollection:
    def __init__(self):
        self._collection = list()
        self._changed = False

    def __iter__(self):
        self.names = sorted(
            [x.name for x in self._collection], key=str.casefold
        )
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.names):
            result = self.names[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def set_changed(self):
        self._changed = True

    def is_changed(self):
        return self._changed

    def get_event(self, name):
        for event in self._collection:
            if event.name == name:
                return event
        return None

    def add_event(self, event):
        if not isinstance(event.name, str):
            raise EventCollectionError("The name of an event must be a string")
        if event.name == "":
            raise EventCollectionError("The name of an event must not be empty")
        if event.name in list(iter(self)):
            raise EventCollectionError(
                f"An event with name '{event.name}' already exists"
            )
        else:
            if not isinstance(event.color, QColor):
                raise EventCollectionError("Color must be a QColor object")
            if not isinstance(event.description, str):
                raise EventCollectionError(
                    "The description of an event must be a string"
                )
            self._collection.append(event)

    def remove_event(self, event):
        self._collection.remove(event)


class EventCollectionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        QMessageBox.warning(None, "Error", f"{message}")


class ChooseEvent(QDialog):

    def __init__(self, event_collection, widget, action="Cancel"):
        super().__init__(widget)
        self.chosen = None
        self.event_collection = event_collection
        self.widget = widget
        self.layout = None
        self.action = action
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Events")
        self.setStyleSheet(
            "QPushButton {"
            "    border: 1px solid gray;"
            "    border-radius: 5px;"
            "    padding: 5px"
            "}"
            "QPushButton:default {"
            "    border: 3px solid black;"
            "}"
        )
        self.re_layout()

        if len(list(iter(self.event_collection))) > 0:
            event_buttons = QHBoxLayout()
            self.buttons = []
            for name in iter(self.event_collection):
                event = self.event_collection.get_event(name)
                button = QPushButton(event.name)
                button.setDefault(len(self.buttons) == 0)
                self.buttons.append(button)
                bg_color = event.color
                fg_color = color_fg_from_bg(bg_color)
                button.setStyleSheet(
                    "QPushButton {"
                    "    background-color: qlineargradient("
                    "        x1:0, y1:0, x2:0, y2:1,"
                    f"       stop:0 {bg_color.name()},"
                    f"       stop:1 {bg_color.name()}"
                    "    );"
                    f"   color: {fg_color.name()};"
                    "}"
                )
                button.setAutoFillBackground(False)
                button.clicked.connect(partial(self.set_chosen, event))
                button.setToolTip(event.description)
                event_buttons.addWidget(button)
            self.layout.addRow(event_buttons)
        control_buttons = QHBoxLayout()
        control_buttons.addStretch()
        assets = Assets()
        new_button = QPushButton(
            QIcon(assets.get("plus.png")),
            "New",
            self,
        )
        new_button.setDefault(False)
        new_button.clicked.connect(self.new_event)
        control_buttons.addWidget(new_button)
        finish_button = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton),
            self.action,
            self,
        )
        finish_button.setDefault(False)
        finish_button.clicked.connect(self.reject)
        control_buttons.addWidget(finish_button)
        control_buttons.addStretch()
        self.layout.addRow(control_buttons)

    def re_layout(self):
        if self.layout:
            QWidget().setLayout(self.layout)
        self.layout = QFormLayout(self)

    def set_chosen(self, val):
        self.chosen = val
        self.accept()

    def get_chosen(self):
        return self.chosen

    def new_event(self):
        event = Event("", EVENT_DEFAULT_COLOR, "")
        dialog = ChangeEvent(event, self.widget)
        dialog.exec()
        if dialog.result() == QMessageBox.DialogCode.Accepted:
            if event.name == "":
                QMessageBox.warning(
                    self, "Warning", "Event name cannot be empty"
                )
            else:
                self.event_collection.add_event(event)
                self.event_collection.set_changed()
        self.create_ui()


class ChangeEvent(QDialog):
    def __init__(self, event, widget=None, may_remove=False):
        super().__init__(widget)
        self.setWindowTitle("Change event")
        self.event = event
        self._request_remove = False
        self.may_remove = may_remove
        self.create_ui()

    def create_ui(self):
        layout = QFormLayout(self)
        widgetbox = QHBoxLayout()
        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self.event.name)
        widgetbox.addWidget(self.name_edit)
        self.color_button = QPushButton("color")
        self.color_button.clicked.connect(self.choose_color)
        self.set_style()
        widgetbox.addWidget(self.color_button)
        layout.addRow("Name: ", widgetbox)
        layout.addRow("Description:", None)
        self.description_edit = TextEdit(self, self.event.description)
        layout.addRow(self.description_edit)
        control_buttons = QHBoxLayout()
        control_buttons.addStretch()
        if self.may_remove:
            remove_button = self.add_control_button(
                self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon),
                "Remove",
                self.set_request_remove,
            )
            control_buttons.addWidget(remove_button)
        cancel_button = self.add_control_button(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogCancelButton
            ),
            "Cancel",
            self.reject,
        )
        control_buttons.addWidget(cancel_button)
        ok_button = self.add_control_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton),
            "Ok",
            self.accept,
        )
        control_buttons.addWidget(ok_button)
        control_buttons.addStretch()
        layout.addRow(control_buttons)

    def add_control_button(self, icon, label, connect):
        button = QPushButton(icon, label)
        button.setDefault(False)
        button.clicked.connect(connect)
        return button

    def accept(self):
        self.event.name = self.name_edit.text()
        self.event.description = self.description_edit.toPlainText()
        super().accept()

    def choose_color(self):
        dialog = QColorDialog(self.event.color, self)
        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.event.color = dialog.currentColor()
            self.set_style()

    def set_style(self):
        bg_color = self.event.color
        fg_color = color_fg_from_bg(bg_color)
        self.color_button.setStyleSheet(
            "QPushButton {"
            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            f"   stop:0 {bg_color.name()}, stop:1 {bg_color.name()});"
            f" color: {fg_color.name()};"
            "border: 2px solid black;"
            "border-radius: 5px;"
            "padding: 6px"
            "}"
            "QPushButton:hover {"
            "    border: 3px solid black;"
            "}"
        )

    def request_remove(self):
        return self._request_remove

    def set_request_remove(self):
        self._request_remove = True
        self.reject()
