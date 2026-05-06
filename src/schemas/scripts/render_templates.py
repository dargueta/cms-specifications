#!/usr/bin/env python3

"""Render Jinja2 templates."""

from __future__ import annotations

import pathlib
import sys
import typing

import click
import jinja2


if typing.TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import TextIO


THIS_FILE = pathlib.Path(__file__)
HERE = THIS_FILE.parent
SCHEMAS_ROOT_DIR = HERE.parent


@click.argument(
    "sources", type=click.Path(exists=True, dir_okay=False, allow_dash=True), nargs=-1
)
@click.option(
    "-o",
    "--output",
    type=click.File(mode="w", atomic=True),
    help="The file to write the output to. Use `-` or omit to write to stdout.",
    default=sys.stdout,
)
@click.option(
    "-I",
    "include",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    multiple=True,
    help="Add the given directory to the template search path. Specify multiple times"
    " to add multiple directories. They will be searched in the order the paths are"
    " provided.",
)
@click.option(
    "-D",
    "define",
    multiple=True,
    help='Define a constant X set to the string Y with the syntax "X=Y". The forms "X="'
    ' and "X" will define X as an empty string.',
)
@click.command()
def main(
    define: Sequence[str],
    include: Sequence[pathlib.Path],
    output: TextIO,
    sources: Sequence[str],
) -> None:
    """Render Jinja2 template files.

    The output is the concatenation of all inputs.
    """
    search_paths = [str(p.absolute()) for p in include[::-1]] + [str(pathlib.Path.cwd())]
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=search_paths),
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    definitions = dict(item.partition("=")[::2] for item in define)
    for file in sources:
        try:
            text = render_single_file(file, environment, definitions)
        except jinja2.TemplateError as err:
            sys.exit(str(err))

        output.write(text)


def render_single_file(
    file: str, environment: jinja2.Environment, definitions: dict[str, str]
) -> str:
    """Render a single Jinja2 template file."""
    if file == "-":
        template = environment.from_string(sys.stdin.read())
    else:
        template = environment.get_template(file)

    return template.render(**definitions)


if __name__ == "__main__":
    main()
