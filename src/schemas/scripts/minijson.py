#!/usr/bin/env python3

"""Minify JSON.

Normally a command line tool like `jq` would suffice for this, but we want users to be
able to use this repo with minimal other installation.
"""

from __future__ import annotations

import json
import sys
import typing

import click


if typing.TYPE_CHECKING:
    from typing import TextIO


@click.argument("output", type=click.File("w", atomic=True), default=sys.stdout)
@click.argument("source", type=click.File("r"), default=sys.stdin)
@click.command()
def main(source: TextIO, output: TextIO) -> None:
    """Minify JSON."""
    data = json.load(source)
    json.dump(data, output, separators=(",", ":"))


if __name__ == "__main__":
    main()
