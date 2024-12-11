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

import os
import re
import tempfile
import zipfile
import yaml
from functools import partial
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QStyle,
    QVBoxLayout,
)
from PySide6.QtMultimedia import QMediaFormat
from .coders import Coders
from .config import Config
from .constants import (
    CONFIG_FILENAME,
    CSV_DELIMITER,
    CSV_ALLOWED_DELIMITERS,
    METADATA_FILENAME,
)
from .data import (
    Data,
    MetaData,
)
from .exceptions import LoadProjectError
from .format import FORMAT
from .utils import sha1_file


class Files:

    def __init__(self, window):

        self.window = window
        self.data_to_load = None
        self._csv_delimiter = None
        self.csv_delimiter = CSV_DELIMITER
        self.config_file_name = CONFIG_FILENAME
        self.metadata_file_name = METADATA_FILENAME
        self.temp_dir = None
        self.file_format = None
        self.project_file_path = None
        self.coders = Coders({}, self.window)
        # FIXME: This attribute is confusing, as regards self.config_file_name
        # This ought to be improved
        self._config_file = None
        self._video_inclusion = True

        # Search for supported video file formats
        self.video_file_extensions = []
        for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
            mime_type = QMediaFormat(f).mimeType()
            name = mime_type.name()
            if re.search("^video/", name):
                self.video_file_extensions.extend(mime_type.suffixes())
        extensions = " ".join(["*." + x for x in self.video_file_extensions])
        self.file_name_filters = [
            f"Video Files ({extensions})",
            "All Files (*.*)",
        ]

        self.project_file_filters = [
            f"Zip files ({' '.join(['*.zip'])})",
            "All Files (*.*)",
        ]

    @property
    def csv_delimiter(self):
        return self._csv_delimiter

    @csv_delimiter.setter
    def csv_delimiter(self, csv_delimiter):
        if csv_delimiter in [v for k, v in CSV_ALLOWED_DELIMITERS.items()]:
            self._csv_delimiter = csv_delimiter
        else:
            QMessageBox.warning(
                self.window,
                "Warning",
                "The CSV delimiter is not valid.\n"
                f'The string "{self.csv_delimiter}" will be used.\n'
                "It is possible to change it via the menu entry\n"
                "Data ⇒ Change CSV Delimiter",
            )

    def set_config_file(self, path):
        self._config_file = path

    def open_video(self, widget=None):
        """Open a video file in a MediaPlayer"""
        dialog_txt = "Open Video File"
        file_dialog = QFileDialog(self.window if not widget else widget)
        file_dialog.setWindowTitle(dialog_txt)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(self.file_name_filters)
        file_dialog.exec()
        if file_dialog.result() == QMessageBox.DialogCode.Accepted:
            # Load only the first of the selected file
            try:
                filename = file_dialog.selectedFiles()[0]
                self.load_video_file(filename)
                self.set_config_from_video_filename(filename)
                self.load_config_file(self._config_file)
            except Exception as e:
                QMessageBox.critical(self.window, "Error", f"{e}")

    def set_config_from_video_filename(self, filename):
        if self._config_file is None:
            dir = os.path.dirname(filename)
            config_file = Path(dir).joinpath(CONFIG_FILENAME)
            if os.path.isfile(config_file):
                self.set_config_file(config_file)

    def open_project(self, widget=None):
        """Open a project file"""
        dialog_txt = "Open Project File"
        project_dialog = QFileDialog(self.window if not widget else widget)
        project_dialog.setWindowTitle(dialog_txt)
        project_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        project_dialog.setNameFilters(self.project_file_filters)
        project_dialog.exec()
        if project_dialog.result() == QMessageBox.DialogCode.Accepted:
            try:
                filename = project_dialog.selectedFiles()[0]
                self.load_project_file(filename)
            except Exception as e:
                QMessageBox.critical(self.window, "Error", f"{e}")

    def load_file(self, filename):
        try:
            if os.path.splitext(filename)[1] in [
                "." + ext for ext in self.video_file_extensions
            ]:
                self.load_video_file(filename)
                self.set_config_from_video_filename(filename)
                self.load_config_file(self._config_file)
            elif os.path.splitext(filename)[1] == ".zip":
                self.load_project_file(filename)
            else:
                QMessageBox.warning(
                    self.window,
                    "Warning",
                    f"File {filename} does not have a supported extension "
                    "(video or ZIP file)",
                )
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"{e}")

    def file_is_absent(self, filename):
        return not os.path.exists(filename) or not os.path.isfile(filename)

    def load_video_file(self, filename, size=None, sha1sum=None):
        """Load video file"""
        if self.file_is_absent(filename):
            raise FileNotFoundError(
                f"FileNotFoundError: {filename} doesn't exist"
            )
        if sha1sum:
            if sha1sum != sha1_file(filename):
                QMessageBox.warning(
                    self.window,
                    "Warning",
                    "The SHA-1 checksum of the video file differs from the one "
                    "declared in the project file",
                )
                return
        if size:
            if size != os.path.getsize(filename):
                QMessageBox.warning(
                    self.window,
                    "Warning",
                    "The size of the video file differs from the one "
                    "declared in the project file",
                )
                return

        self.media = QUrl.fromLocalFile(filename)
        self.window.set_source(self.media)

    def load_project_file(self, filename):
        """Load project file"""
        if self.file_is_absent(filename):
            raise FileNotFoundError(f"FileNotFoundError: {filename} not found")

        # filename is a zip file
        self.project_file_path = filename
        project_file_dir = os.path.dirname(filename)

        with zipfile.ZipFile(filename, "r") as zip_file:
            # Create temp dir
            temp_dir = tempfile.TemporaryDirectory()

            # Load data from metadata.yml
            with zip_file.open(self.metadata_file_name) as f:
                data = MetaData(f, self.window)
                if data is None:
                    raise LoadProjectError("Format problem")
                self.file_format = data["format"]
                files = zip_file.namelist()

                # Search for video in temp dir
                video_info = data["video"]
                video_file = video_info["filename"]
                if video_file not in files:
                    if self.file_is_absent(
                        Path(project_file_dir).joinpath(video_file)
                    ):
                        raise LoadProjectError("Failed to load video file")
                    else:
                        video_file_in_zip = False
                else:
                    video_file_in_zip = True

                # Search for configuration file in temp dir
                if self.config_file_name not in files:
                    raise LoadProjectError("Failed to load config file")

                # Search for csv file in temp dir
                data_file = os.path.splitext(video_file)[0] + ".csv"
                if data_file not in files:
                    raise LoadProjectError("Failed to load data file")

                # Extract all files in temp dir
                zip_file.extractall(temp_dir.name)

                # Load video file from temp dir
                if video_file_in_zip:
                    path = Path(temp_dir.name).joinpath(video_file)
                else:
                    path = Path(project_file_dir).joinpath(video_file)
                self.load_video_file(
                    path, data["video"]["size"], data["video"]["sha1sum"]
                )

                # Load config file from in temp dir
                self.load_config_file(
                    Path(temp_dir.name).joinpath(self.config_file_name)
                )

                # Load csv data file from in temp dir
                self.data_to_load = Path(temp_dir.name).joinpath(data_file)

            self.temp_dir = temp_dir

        self.window.time_pane.data_needs_save = False

    def load_config_file(self, filename=None):
        """load presets from configuration file"""
        # Read the YAML file
        config = Config() if filename is None else Config(filename)

        # Update the config file, eventually
        if self.file_format:
            config.update_format(self.file_format)

        self.window.time_pane.timelines_from_config(config)

        if "csv-delimiter" in config:
            self.csv_delimiter = config["csv-delimiter"]

        if "coders" in config:
            self.coders = Coders(config["coders"], self.window)

    def load_data_file(self, filename=None):
        """Load data file"""
        if os.path.isfile(filename):
            data = Data(filename, self.file_format)
            self.window.time_pane.add_data(data)
        else:
            QMessageBox.critical(
                self.window,
                "Error",
                "The file you tried to load does not exist.",
            )

        self.data_to_load = None

    def save_project(self) -> bool:
        """Save project file"""
        temp_dir = tempfile.TemporaryDirectory()

        # 1. Create config file from information of time_pane in
        # tmp directory
        if not self.coders.current:
            if not self.coders.set_current():
                return
        if not self.coders.current:
            return
        self.coders.current.set_date_now()

        # Construct the default file name from the QUrl of the video file
        target_directory = self.media.path()
        target_file_name = os.path.splitext(
            os.path.basename(self.media.path())
        )[0]
        data_file_name = target_file_name + ".csv"
        if self.project_file_path:
            target_directory = self.project_file_path
            target_file_name = os.path.splitext(
                os.path.basename(self.project_file_path)
            )[0]

        target_directory = (
            os.path.dirname(target_directory) + "/" + target_file_name + ".zip"
        )

        config_file_path = Path(temp_dir.name).joinpath(self.config_file_name)
        self.export_config_file(config_file_path)

        # 2. Create CSV file "data.csv" from information of time_pane in
        # tmp directory
        data_file_path = Path(temp_dir.name).joinpath(data_file_name)
        self.export_data_file(data_file_path)

        metadata_file_path = Path(temp_dir.name).joinpath(
            self.metadata_file_name
        )
        sha1_hexdigest = sha1_file(self.media.toLocalFile())

        with open(metadata_file_path, "w", encoding="utf-8") as fid:
            yaml.safe_dump(
                {
                    "video": {
                        "filename": os.path.basename(self.media.path()),
                        "size": os.path.getsize(self.media.toLocalFile()),
                        "sha1sum": sha1_hexdigest,
                    },
                    "format": FORMAT,
                },
                fid,
                allow_unicode=True,
            )

        # Open FileDialog
        path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save project",
            target_directory,
            "Zip Files (*.zip);;All Files (*)",
        )
        if path:
            with zipfile.ZipFile(path, "w") as zip_file:
                zip_file.write(metadata_file_path, self.metadata_file_name)
                zip_file.write(config_file_path, self.config_file_name)
                zip_file.write(data_file_path, data_file_name)
                if self._video_inclusion:
                    zip_file.write(
                        self.media.toLocalFile(),
                        os.path.basename(self.media.path()),
                    )
            self.window.time_pane.data_needs_save = False
            return True
        return False

    def export_data_file(self, target_path=None) -> bool:
        """Export data in CSV file"""
        if not target_path:
            if not self.is_exportable():
                QMessageBox.warning(
                    self.window, "No Data", "There is no data to save."
                )
                return False

            # Construct the default file name from the QUrl of the video file
            default_target_path = (
                os.path.dirname(self.media.path())
                + "/"
                + os.path.splitext(os.path.basename(self.media.path()))[0]
                + ".csv"
            )

            target_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Save data (CSV file)",
                default_target_path,
                "CSV Files (*.csv);;All Files (*)",
            )

        if target_path:
            df = self.window.time_pane.timelines_to_dataframe()
            df.to_csv(
                target_path,
                sep=self.csv_delimiter,
                encoding="utf-8",
                index=False,
            )
            self.window.time_pane.data_needs_save = False
            return True
        return False

    def is_exportable(self) -> bool:
        """Return true if the media file is exportable"""
        return (
            self.window.video.media_player is not None
            and self.window.time_pane is not None
            and len(self.window.time_pane.timelines()) > 0
            and self.window.time_pane.has_occurrences()
        )

    def save_config_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save Configuration File",
            str(
                Path(os.path.dirname(self.media.path())).joinpath(
                    self.config_file_name
                )
            ),
            "YAML Files (*.yml);;All Files (*)",
        )
        if path:
            self.export_config_file(path)

    def export_config_file(self, target_path=None):
        config = Config(target_path)

        timelines = self.window.time_pane.timelines()

        config["timelines"] = {
            t.name: {
                "order": i + 1,
                "description": t.description,
                "events": {
                    name: {
                        "color": t.event_collection.get_event(
                            name
                        ).color.name(),
                        "description": t.event_collection.get_event(
                            name
                        ).description,
                    }
                    for name in t.event_collection
                },
            }
            for i, t in enumerate(timelines)
        }

        if self.coders:
            coders_list = self.coders.to_list()
            if len(coders_list) > 0:
                config["coders"] = coders_list

        config["csv-delimiter"] = self.csv_delimiter

        # Write data
        config.save()

    def no_video_loaded(self):
        dialog = OpenProjectDialog(self)
        dialog.exec()

    def temp_dir_cleanup(self):
        if self.temp_dir:
            self.temp_dir.cleanup()

    def change_csv_delimiter(self):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("CSV delimiter")
        layout = QFormLayout()
        label = QLabel("Select a CSV delimiter:")
        layout.addWidget(label)
        for k, v in CSV_ALLOWED_DELIMITERS.items():
            button = QRadioButton(k)
            button.clicked.connect(partial(self.set_csv_delimiter, v))
            if self.csv_delimiter == v:
                button.setChecked(True)
            layout.addWidget(button)
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self.window,
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec()

    def set_csv_delimiter(self, csv_delimiter):
        self.csv_delimiter = csv_delimiter

    def toggle_video_inclusion(self):
        self._video_inclusion = not self._video_inclusion
        common = "project file at next save"
        if self._video_inclusion:
            text = f"Exclude video from {common}"
        else:
            text = f"Include video in {common}"
        self.window.menu.video_inclusion_exclusion_action.setText(text)


class OpenProjectDialog(QDialog):
    def __init__(self, files):
        super().__init__(files.window)
        self.files = files
        self.setWindowTitle("Open a project")

        layout = QVBoxLayout(self)

        self.open_video_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open video",
            self,
        )
        self.open_project_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open project",
            self,
        )

        buttons = QDialogButtonBox(self)
        buttons.addButton(
            self.open_video_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        buttons.addButton(
            self.open_project_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        buttons.clicked.connect(self.perform_action)
        buttons.rejected.connect(self.reject)

        layout.addWidget(
            QLabel("Choose a video or a project file to start coding")
        )
        layout.addWidget(buttons)
        self.setLayout(layout)

    def perform_action(self, button):
        if button == self.open_video_btn:
            self.files.open_video(self)
        elif button == self.open_project_btn:
            self.files.open_project(self)
        self.accept()
