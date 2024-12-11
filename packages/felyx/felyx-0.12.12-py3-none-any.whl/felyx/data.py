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
from yaml import (
    load,
    Loader,
)

from .format import (
    FORMAT,
    format_ok,
)


class Data(pd.DataFrame):
    def __init__(self, filename, file_format):
        super().__init__(pd.read_csv(filename, sep=None, engine="python"))
        self.update_format(file_format)

    def update_format(self, file_format):
        for fmt in range(file_format + 1, FORMAT):
            if fmt == 3:
                self.rename(columns={"label": "event"}, inplace=True)


class MetaData(dict):
    def __init__(self, filename, window=None):
        super().__init__(self._load_file(filename))
        if "format" not in self:
            self = None
        else:
            if not format_ok(self["format"], window):
                self = None
            else:
                self.update_format()

    def _load_file(self, fid):
        data = load(fid, Loader=Loader)
        if not isinstance(data, dict):
            raise TypeError(
                "Metadata file does not contain a dict at top level"
            )
        return data

    def update_format(self):
        for fmt in range(self["format"] + 1, FORMAT + 1):
            if fmt == 4:
                filename = self["video"]
                self["video"] = {
                    "filename": filename,
                    "size": None,
                    "sha1sum": None,
                }
