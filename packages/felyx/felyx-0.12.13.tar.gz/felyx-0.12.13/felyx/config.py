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
import appdirs
from yaml import load, Loader, safe_dump
from pathlib import Path

from .constants import (
    CONFIG_FILENAME,
    APP_NAME,
)
from .format import FORMAT


class Config(dict):
    def __init__(self, config_file=CONFIG_FILENAME):
        self.filename = config_file
        self._load()

    def _get_config_paths(self):
        return [
            Path(__file__).parent.joinpath("config", CONFIG_FILENAME),
            Path(appdirs.site_data_dir(APP_NAME)).joinpath(CONFIG_FILENAME),
            Path(appdirs.site_config_dir(APP_NAME)).joinpath(CONFIG_FILENAME),
            Path(appdirs.user_config_dir(APP_NAME)).joinpath(CONFIG_FILENAME),
            self.filename,
        ]

    def _load(self):
        for path in self._get_config_paths():
            config = self._load_file(path)
            if self._load_file(path):
                for k, v in config.items():
                    self[k] = v

    def _load_file(self, path):
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as fid:
                return load(fid, Loader=Loader)
        else:
            return None

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as fid:
            safe_dump(dict(self), fid, allow_unicode=True)
        pass

    def update_format(self, file_format):
        for fmt in range(file_format + 1, FORMAT + 1):
            if fmt == 3:
                if "timelines" in self:
                    tmp = self["timelines"]
                    del self["timelines"]
                    self["timelines"] = dict()
                    order = 0
                    for elem in sorted(tmp, key=lambda x: x["name"].casefold()):
                        name = elem["name"]
                        order += 1
                        timeline = dict()
                        timeline["order"] = order
                        if "events" in elem:
                            events = dict()
                            for ev in elem["events"]:
                                ev_dict = dict()
                                if "color" in ev:
                                    ev_dict["color"] = ev["color"]
                                events[ev["name"]] = ev_dict
                            timeline["events"] = events
                        self["timelines"][name] = timeline
