# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import Dict

from onecode import FolderInput


class GeoFolderInput(FolderInput):
    def _interface_json(self) -> Dict:
        raise ValueError("FolderInput not implemented in GeoPortal")
