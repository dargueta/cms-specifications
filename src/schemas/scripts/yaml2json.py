#!/usr/bin/env python3

"""Convert YAML to JSON.

Normally a command line tool like `yq` would suffice, but we want users to be able to
use this repo with minimal other installation.
"""

from __future__ import annotations

import json
import sys
import typing

import click
import ruamel.yaml


if typing.TYPE_CHECKING:
    from typing import TextIO


@click.argument("json_file", type=click.File("w"), default=sys.stdout)
@click.argument("yaml_file", type=click.File("r"), default=sys.stdin)
@click.command()
def main(yaml_file: TextIO, json_file: TextIO) -> None:
    """Convert YAML into JSON."""
    yaml = ruamel.yaml.YAML(typ="safe")
    data = yaml.load(yaml_file)
    json.dump(data, json_file, indent=2, default=str)


if __name__ == "__main__":
    main()
