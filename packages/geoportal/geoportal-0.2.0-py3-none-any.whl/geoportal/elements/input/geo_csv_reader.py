# SPDX-FileCopyrightText: 2023-2024 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import Dict

from onecode import CsvReader


class GeoCsvReader(CsvReader):
    def _interface_json(self) -> Dict:
        panel = self.panel if 'panel' in self.__dict__ else "PANEL_INPUT"
        type = self.type if 'type' in self.__dict__ else "CSV",
        extension = self.extension if 'extension' in self.__dict__ else ".csv"

        return {
            "name": self.key,
            "kind": type,
            "select": "FILE",
            "extension": extension,
            "required": True,
            "read_only": False,
            "default_from": "user",
            "panel": panel
        }
