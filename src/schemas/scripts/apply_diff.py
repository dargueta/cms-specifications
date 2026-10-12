# SPDX-License-Identifier: BSD-3-Clause
"""Apply a diff embedded in a JSON file."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

import click
import jsonpath_ng
import jsonpath_ng.ext
from jsonpath_ng.exceptions import JsonPathLexerError


if TYPE_CHECKING:
    from typing import TextIO


@click.argument("output", type=click.File("w", atomic=True), default=sys.stdout)
@click.argument("source_file", type=click.File(), default=sys.stdin)
@click.command()
def main(source_file: TextIO, output: TextIO) -> None:
    """Apply a diff embedded in a JSON file.

    This does nothing unless the file has a top-level key named ``__patch__``.
    ``__patch__`` is list of objects, each object having two keys:

    \b
    * `selector`: A JSONPath selector for the key(s) to modify.
    * `new_value`: The replacement value. Use `null` to delete matching items.
    """
    data = json.load(source_file)

    for change in data.get("__patch__", ()):
        try:
            selector = jsonpath_ng.ext.parse(change["selector"])
        except JsonPathLexerError as err:
            sys.exit(f"Bad selector {change['selector']!r} for patch: {err}")

        if change["new_value"] is not None:
            data = selector.update(data, change["new_value"])
        else:
            # Assignment to null means "delete this item".
            data = selector.filter(lambda _: True, data)

    json.dump(data, output, indent=2)


if __name__ == "__main__":
    main()
