#!/usr/bin/env python3

"""Convert JSON to YAML.

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


@click.argument("yaml_file", type=click.File("w"), default=sys.stdout)
@click.argument("json_file", type=click.File("r"), default=sys.stdin)
@click.command()
def main(json_file: TextIO, yaml_file: TextIO) -> None:
    """Convert JSON into YAML."""
    data = json.load(json_file)

    # Set arrays to be indented two spaces underneath the keys they're mapped to. It
    # drives me crazy otherwise.
    yaml = ruamel.yaml.YAML(typ="safe")
    yaml.indent(offset=2)
    yaml.dump(data, yaml_file)


if __name__ == "__main__":
    main()
