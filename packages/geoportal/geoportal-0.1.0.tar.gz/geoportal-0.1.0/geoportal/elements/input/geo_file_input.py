# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import os
from typing import Any, Dict, List, Optional, Tuple, Union

from onecode import FileInput, Logger, Project


class GeoFileInput(FileInput):
    def __init__(
        self,
        key: str,
        value: Optional[Union[str, List[str], List[List[str]]]],
        label: Optional[str] = None,
        count: Optional[Union[int, str]] = None,
        optional: Union[bool, str] = False,
        hide_when_disabled: bool = False,
        types: List[Tuple[str, str]] = None,
        multiple: bool = False,
        tags: Optional[List[str]] = None,
        **kwargs: Any
    ):
        if (
            value is not None and
            Project().data is not None and
            not os.path.exists(value) and
            optional and
            key not in Project().data
        ):
            Logger.warning(f"[{key}] File {value} does not exist but is flagged as optional => None will be returned")
            value = None

        super().__init__(
            key,
            value,
            label,
            count,
            optional,
            hide_when_disabled,
            types=types,
            multiple=multiple,
            tags=tags,
            **kwargs
        )

    def _validate_file_value(
        self,
        value: str
    ) -> None:
        group = bool(self.group) if 'group' in self.__dict__ else False

        if not os.path.exists(value):
            raise FileNotFoundError(f"[{self.key}] File not found: {value}")

        # shpfile case: group file with path to dir being ok
        elif not os.path.isfile(value) and not group:
            raise FileNotFoundError(f"[{self.key}] Path is not a file: {value}")

    def _interface_json(self) -> Dict:
        panel = self.panel if 'panel' in self.__dict__ else "PANEL_INPUT"
        type = self.type if 'type' in self.__dict__ else "None"
        group = bool(self.group) if 'group' in self.__dict__ else False

        p = {
            "name": self.key,
            "kind": type,
            "select": "FILE",
            "required": True,
            "read_only": False,
            "default_from": "user",
            "panel": panel
        }

        if "extension" in self.__dict__:
            p["extension"] = self.extension

        if group:
            p["properties"] = {
				"special": "multi",
				"dest_path": f"/{self.key}"
			}

        return p
