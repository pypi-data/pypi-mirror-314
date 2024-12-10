# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import argparse
import importlib
import json
import sys
import os
from typing import Dict, List, Optional

import pydash
from slugify import slugify
from yaspin import yaspin

import onecode  # noqa
from onecode import (
    ElementType,
    Mode,
    Project
)
from onecode.cli import process_call_graph
import geoportal


def process(
    calls: List[Dict[str, str]],
    verbose: bool = False
) -> Dict:
    params = []

    for code in calls:
        try:
            t = eval(f"{code['func']}_type")

            # output are skipped
            if t == ElementType.INPUT:
                if verbose:
                    print(f"> {code['loc']}")

                p = eval(f"{code['loc']}")
                params.append(p)

        except Exception as e:
            print('Error ', e)

    return params


def extract_json(
    project_path: str,
    verbose: bool = False
) -> None:
    # hack to allow dynamic input
    if os.path.exists(os.path.join('config', "init_path.py")):
        spec = importlib.util.spec_from_file_location(
            os.path.basename(project_path),
            os.path.join('config', "init_path.py")
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        for k in module.init():
            globals()[k] = ""

    Project().mode = "_interface_json"
    statements = process_call_graph(project_path)

    name = os.path.basename(project_path)
    label = pydash.human_case(name)
    to_file = os.path.join(project_path, 'interface.json')
    i18n_file = os.path.join(project_path, 'i18n', 'en.json')

    # prepare i18n/en.json
    if os.path.exists(i18n_file):
        with open(i18n_file, 'r') as f:
            i18n = json.load(f)

    else:
        os.makedirs(os.path.dirname(i18n_file), exist_ok=True)
        i18n = {
            "panels": {},
            "parameters": {},
            "steps": {},
            "options": {}
        }


    # prepare interface.json
    if os.path.exists(to_file):
        with open(to_file, 'r') as f:
            interface = json.load(f)
            interface["steps"] = [{
                "name": label,
    			"key": "main",
    			"icon": "",
    			"default": True,
    			"read_only": True,
    			"inputs": [],
                "outputs": []
            }]
    else:
        interface = {
        	"jobKind": "PYTHON",
        	"key": slugify(name, separator='_'),
        	"name": label,
        	"label": label,
        	"icon": "fork",
        	"procedure": "Appraisal",
        	"order": 0,
        	"docs": "",
        	"options": [],
        	"steps": [{
                "name": label,
    			"key": "main",
    			"icon": "",
    			"default": True,
    			"read_only": True,
    			"inputs": [],
                "outputs": []
            }],
            "panels": {}
        }

    parameters = []
    panels = []
    for v in statements.values():
        params = process(v["calls"], verbose)

        pydash.set_(
            interface,
            ["steps", 0, "inputs"],
            pydash.get(interface, ["steps", 0, "inputs"]) + params
        )

        for param in params:
            # get parameter name for i18n
            key = param["name"]
            if not pydash.has(i18n, ["parameters", key]):
                pydash.set_(i18n, ["parameters", key], key)

        # get parameters and panels from elements
        parameters += pydash.map_(params, lambda x: x["name"])
        panels += pydash.map_(params, lambda x: x["panel"])

    panels = pydash.uniq(panels)

    # remove existing parameters no longer in use from i18n
    i18n["parameters"] = pydash.omit(
        i18n["parameters"],
        pydash.difference(pydash.keys(i18n["parameters"]), parameters)
    )

    # remove existing panels no longer in use
    panels_interface_to_remove = pydash.difference(pydash.keys(interface["panels"]), panels)
    interface["panels"] = pydash.omit(
        interface["panels"],
        panels_interface_to_remove
    )

    panels_i18n_to_remove = pydash.difference(pydash.keys(i18n["panels"]), panels)
    i18n["panels"] = pydash.omit(
        i18n["panels"],
        panels_i18n_to_remove
    )

    for p in panels:
        if not pydash.has(interface, ["panels", p]):
            pydash.set_(
                interface,
                ["panels", p],
                {
        			"name": p,
        			"icon": "file alternate outline",
            		"rank": len(interface["panels"])
                }
            )

        panel_name = pydash.get(interface, ["panels", p, "name"])
        if not pydash.has(i18n, ["panels", panel_name]):
            pydash.set_(
                i18n,
                ["panels", panel_name],
                {
        			"label": panel_name,
                    "description": panel_name
                }
            )

    if not pydash.has(i18n, ["steps", label]):
        # only 1 step, so overwrite the "steps" key
        pydash.set_(
            i18n,
            "steps",
            {
                label: label
            }
        )

    with open(to_file, 'w') as out:
        json.dump(interface, out, indent=4)

    with open(i18n_file, 'w') as out:
        json.dump(i18n, out, indent=4)


def main(cli: bool = True) -> None:    # pragma: no cover
    """
    ```bash
    usage: geoportal-extract [-h] [--path PATH] [--verbose]

    Extract OneCode project parameters to interface.json for GeoPortal.

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH           Path to the project root directory if not the current working directory
      --verbose             Print verbose information
    ```

    """
    parser = argparse.ArgumentParser(
        description='Extract OneCode project parameters to JSON file'
    )
    parser.add_argument(
        '--verbose',
        help='Print verbose information',
        action='store_true'
    )
    parser.add_argument(
        '--path',
        required=False,
        help='Path to the project root directory if not the current working directory'
    )
    args = parser.parse_args()

    with yaspin(text="Extracting parameters") as spinner:
        try:
            project_path = args.path if args.path is not None else os.getcwd()

            print('\n')
            extract_json(project_path, args.verbose)

            print('\n')
            spinner.text = f"Parameters extracted to {os.path.join(project_path, 'interface.json')}"
            spinner.ok("✅")

        except Exception as e:
            spinner.text = f"{e}"
            spinner.fail("💥 [Failed] -")

            if not cli:
                raise e
