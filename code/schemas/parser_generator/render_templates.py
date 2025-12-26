#!/usr/bin/env python3

from __future__ import annotations

import os
import typing

import click
import mako.template  # pyright: ignore[reportMissingTypeStubs]
import mako.lookup  # pyright: ignore[reportMissingTypeStubs]

if typing.TYPE_CHECKING:
    from typing import TextIO


@click.argument("sources", type=click.File(), nargs=-1)
@click.option(
    "-o",
    "--output",
    type=click.File(mode="w", atomic=True),
    help="The file to write the output to. Use `-` or omit to write to stdout.",
)
@click.option(
    "-I",
    "include",
    type=click.Path(exists=True, file_okay=False),
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
    define: list[str], include: list[str], output: TextIO, sources: list[TextIO]
) -> None:
    """Render mako template files.

    The output is the concatenation of all inputs.
    """
    lookup = mako.lookup.TemplateLookup(directories=include + [os.getcwd()])
    definitions = dict(item.partition("=")[::2] for item in define)
    for file in sources:
        template = mako.template.Template(file.read(), lookup=lookup)
        output.write(template.render(**definitions))


if __name__ == "__main__":
    main()
