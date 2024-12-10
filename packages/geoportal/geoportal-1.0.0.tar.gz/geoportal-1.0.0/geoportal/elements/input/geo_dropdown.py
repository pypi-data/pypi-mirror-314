# SPDX-FileCopyrightText: 2023-2024 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import Dict

from onecode import Dropdown


class GeoDropdown(Dropdown):
    def _interface_json(self) -> Dict:
        key, value = self._extract()
        panel = self.panel if 'panel' in self.__dict__ else "PANEL_INPUT"

        return {
            "name": key,
            "select": "VARIABLE",
            "required": True,
            "read_only": False,
            "default": value,
            "default_from": "user",
            "panel": panel
        }
