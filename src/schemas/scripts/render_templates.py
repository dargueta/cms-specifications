#!/usr/bin/env python3

"""Render Jinja2 templates."""

from __future__ import annotations

import collections
import pathlib
import sys
import typing

import click
import jinja2
import ruamel.yaml
from ruamel.yaml import YAMLError


if typing.TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any
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
    "-v",
    "--vars-file",
    "variable_files",
    metavar="[NAME=]PATH",
    multiple=True,
    help="A YAML or JSON file containing values to make available to the template."
    " If this is a simple file path, all values are loaded into the global namespace."
    " Alternatively, use the form `name=path` to load all values into a global variable"
    ' named `name`. `path` may be "-" to read from stdin. This option can be passed any'
    " number of times. If two or more files define the same value, the last file given"
    " on the command line wins. Values defined by -D always take precedence over a"
    " value defined in these files.",
)
@click.option(
    "-I",
    "include",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    multiple=True,
    help="Add the given directory to the template search path. Specify multiple times"
    " to add multiple directories. Directories are searched in the order provided.",
)
@click.option(
    "-D",
    "key_value_pairs",
    metavar="KEY=[VALUE]",
    multiple=True,
    help='Define a constant KEY set to the string VALUE. The forms "KEY=" and "KEY"'
    " define KEY as an empty string. If a value is passed multiple times, the last one"
    " wins. These take precedence over keys loaded from a file given by `--vars-file`.",
)
@click.command()
def main(
    key_value_pairs: Sequence[str],
    include: Sequence[pathlib.Path],
    output: TextIO,
    sources: Sequence[str],
    variable_files: Sequence[str],
) -> None:
    """Render Jinja2 template files.

    The output is the concatenation of all inputs.
    """
    search_paths = [str(p.absolute()) for p in include[::-1]] + [
        str(pathlib.Path.cwd())
    ]
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=search_paths),
        undefined=jinja2.StrictUndefined,
        # Deliberately turn HTML escaping off, since we're generating YAML. HTML
        # entities can actually break otherwise valid YAML.
        autoescape=False,  # noqa: S701
    )

    uses_stdin_as_varfile = sum(
        1 for f in variable_files if f == "-" or f.endswith("=-")
    )
    uses_stdin_as_template = sum(1 for f in sources if f == "-")

    if uses_stdin_as_varfile and uses_stdin_as_template:
        sys.exit(
            "`stdin` cannot be used both to provide variables and serve as a template"
            " source. stdin would be exhausted while loading variables, then cause this"
            " to hang while waiting for further input when loading a template."
        )

    try:
        namespace = collections.ChainMap(
            dict(item.partition("=")[::2] for item in key_value_pairs),
            *(
                load_variable_file(name_and_file_pair)
                for name_and_file_pair in variable_files
            ),
        )
    except (ValueError, FileNotFoundError) as err:
        sys.exit(str(err))

    for file in sources:
        try:
            text = render_single_file(file, environment, dict(namespace))
        except jinja2.TemplateError as err:
            sys.exit(str(err))

        output.write(text)


def load_variable_file(path_or_pair: str) -> dict[str, Any]:
    """Load a YAML file, optionally namespaced.

    Usage:

    >>> load_variable_file("foo.yaml")
    {"foo": 123, "bar": True}
    >>> load_variable_file("namespace=foo.yaml")
    {"namespace": {"foo": 123, "bar": True}}

    Arguments:
        path_or_pair (str):
            Either a file path, or a string of the form `name=path` where `name` is a
            top-level key to load the contents of the file into.
    """
    yaml = ruamel.yaml.YAML(typ="safe")

    if "=" in path_or_pair:
        name, _, file_path = path_or_pair.partition("=")
    else:
        name = ""
        file_path = path_or_pair

    with open(file_path) as fd:
        try:
            data = yaml.load(fd)
        except YAMLError as err:
            raise ValueError(f"Failed to load {file_path!r} as YAML: {err}") from None

    if name:
        return {name: data}
    return data


def validate_stdin_usage(
    var_files: Sequence[str], template_files: Sequence[str]
) -> None:
    """Assert `stdin` is only used exactly once.

    Attempting to use `stdin` more than once would hang the process.
    """
    num_varfile_usages = sum(1 for f in var_files if f == "-" or f.endswith("=-"))
    num_template_usages = sum(1 for f in template_files if f == "-")

    if num_varfile_usages and num_template_usages:
        sys.exit(
            "`stdin` cannot be used both to provide variables and serve as a template"
            " source. stdin would be exhausted while loading variables, then cause this"
            " to hang while waiting for further input when loading a template."
        )
    if num_varfile_usages > 1:
        sys.exit(
            "Error: `stdin` passed multiple times as a variables file. This would hang."
        )
    if num_template_usages > 1:
        sys.exit(
            "Error: `stdin` passed multiple times as a template file. This would hang."
        )


def render_single_file(
    file: str, environment: jinja2.Environment, definitions: dict[str, Any]
) -> str:
    """Render a single Jinja2 template file."""
    if file == "-":
        template = environment.from_string(sys.stdin.read())
    else:
        with open(file) as fd:
            template = environment.from_string(fd.read())

    return template.render(**definitions)


if __name__ == "__main__":
    main()
