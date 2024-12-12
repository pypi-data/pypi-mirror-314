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

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QRadioButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)
from functools import partial
from datetime import datetime


class Coders:
    """Store and manipulate the list of coders"""

    def __init__(self, info, widget=None):
        self.coders = [Coder(item, widget) for item in info]
        self.current = None
        # FIXME: Eventually, transform self.dialog into a @property
        self.dialog = None
        self.widget = widget

    def set_current(self):

        if len(self.coders) == 0:
            if not self.new_coder():
                return False

        while True:

            self.changed = False

            self.dialog = QDialog(self.widget)
            self.dialog.setWindowTitle("Coders")

            layout = QVBoxLayout()
            self.dialog.setLayout(layout)

            label = QLabel("Select a coder identity:")
            layout.addWidget(label)

            for coder in self.coders:
                button = QRadioButton(coder.get_string())
                button.clicked.connect(partial(self.update, coder))
                if self.current == coder:
                    button.setChecked(True)
                layout.addWidget(button)

            buttonbox = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Open
                | QDialogButtonBox.StandardButton.Apply
                | QDialogButtonBox.StandardButton.Cancel
                | QDialogButtonBox.StandardButton.Ok,
                self.dialog,
            )
            buttonbox.accepted.connect(self.dialog.accept)
            buttonbox.rejected.connect(self.dialog.reject)
            buttonbox.button(QDialogButtonBox.StandardButton.Apply).setText(
                "Edit"
            )
            buttonbox.button(
                QDialogButtonBox.StandardButton.Apply
            ).clicked.connect(self.edit_coder)
            buttonbox.button(QDialogButtonBox.StandardButton.Open).setText(
                "New"
            )
            buttonbox.button(
                QDialogButtonBox.StandardButton.Open
            ).clicked.connect(self.new_coder)
            layout.addWidget(buttonbox)

            self.dialog.exec()
            if self.changed:
                continue
            if self.dialog.result() == QMessageBox.DialogCode.Rejected:
                self.current = None
                return False
            if self.current:
                return True

    def update(self, coder):
        self.current = coder

    def to_list(self):
        return [x.get_dict() for x in self.coders]

    def edit_coder(self):
        if self.current:
            self.current.edit()
        self.changed = True
        self.dialog.accept()

    def new_coder(self):
        coder = Coder({"name": "", "email": ""}, self.widget)
        coder.edit()
        if not coder.ok:
            return False
        if coder.name == "" and coder.email == "":
            QMessageBox.warning(
                self.widget,
                "New coder",
                "The name and and the email of the coder cannot be "
                "simultaneous empty",
            )
            return False
        else:
            self.coders.append(coder)
            self.changed = True
            self.current = coder
            return True


class Coder:
    """Store and manipulate information for individual coder"""

    def __init__(self, info, widget=None):
        self.name = info["name"]
        if "email" in info:
            self.email = info["email"]
        else:
            self.email = None
        if "last-time" in info:
            self.last_time = info["last-time"]
        else:
            self.last_time = None
        self.button = None
        self.widget = widget

    def get_string(self):
        retval = self.name
        if self.email:
            retval += f" <{self.email}>"
        if self.last_time:
            retval += f" ({self.last_time})"
        return retval

    def get_dict(self):
        retval = {"name": self.name}
        if self.email:
            retval["email"] = self.email
        if self.last_time:
            retval["last-time"] = self.last_time
        return retval

    def set_date_now(self):
        self.last_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    def edit(self):

        self.dialog = QDialog(self.widget)
        self.dialog.setWindowTitle("Edit coder information")

        layout = QFormLayout()
        self.dialog.setLayout(layout)

        self.name_edit = QLineEdit()
        self.name_edit.setText(self.name)
        layout.addRow("Name :", self.name_edit)

        self.email_edit = QLineEdit()
        if self.email:
            self.email_edit.setText(self.email)
        self.email_edit.setFixedWidth(300)
        layout.addRow("Email :", self.email_edit)

        buttonbox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok,
            self.dialog,
        )
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

        self.dialog.exec()

    def accept(self):
        self.name = self.name_edit.text()
        new_email = self.email_edit.text()
        if new_email != "":
            self.email = new_email
        self.ok = True
        self.dialog.accept()

    def reject(self):
        self.ok = False
        self.dialog.reject()
