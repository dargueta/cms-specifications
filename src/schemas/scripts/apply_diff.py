"""Apply a diff in a basic format."""

from __future__ import annotations

import json
import pathlib
import sys
from typing import TYPE_CHECKING

import click
import jsonpath_ng
import jsonpath_ng.ext
from jsonpath_ng.exceptions import JsonPathLexerError


if TYPE_CHECKING:
    from typing import TextIO


@click.argument(
    "patch_file", type=click.Path(dir_okay=False, exists=True, path_type=pathlib.Path)
)
@click.argument(
    "path_root", type=click.Path(file_okay=False, exists=True, path_type=pathlib.Path)
)
@click.option("-o", "--output", type=click.File("w", atomic=True), default=sys.stdout)
@click.command()
def main(path_root: pathlib.Path, patch_file: pathlib.Path, output: TextIO) -> None:
    """Apply a diff to a JSON file.

    The file must have two top-level keys, `base` and `changes`.

    \b
    * `base`: The relative path from PATH_ROOT to the file that the diff will be applied
      to.
    * `changes`: A list of objects with two keys:
      - `selector`: A JSONPath selector for the key(s) to modify.
      - `new_value`: The replacement value. Use `null` to delete matching items.
    """
    with patch_file.open() as fd:
        patch = json.load(fd)

    base_file_path = path_root / patch["base"]
    with base_file_path.open() as fd:
        base = json.load(fd)

    for change in patch["changes"]:
        try:
            selector = jsonpath_ng.ext.parse(change["selector"])
        except JsonPathLexerError as err:
            sys.exit(f"Bad patch file `{patch_file}`: {err}")

        if change["new_value"] is not None:
            base = selector.update(base, change["new_value"])
        else:
            # Assignment to null means "delete this item".
            base = selector.filter(lambda _: True, base)

    json.dump(base, output, indent=2)


if __name__ == "__main__":
    main()
