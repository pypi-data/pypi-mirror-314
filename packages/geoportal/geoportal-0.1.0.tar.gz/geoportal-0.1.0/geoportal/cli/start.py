# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import os


def main(cli: bool = True) -> None:    # pragma: no cover
    """
    ```bash
    usage: geoportal-start [-h]

    Shortcut to onecode-start with module geoportal.

    optional arguments:
      -h, --help            show this help message and exit
    ```

    """
    os.system('onecode-start --modules geoportal')
