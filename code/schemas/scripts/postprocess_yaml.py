#!/usr/bin/env python3

"""Expand all anchors and constructors in a YAML file."""

from __future__ import annotations

import functools
import pathlib
import typing

import click
import deep_chainmap
import ruamel.yaml
from ruamel.yaml.constructor import ConstructorError
from ruamel.yaml.error import MarkedYAMLError

from ._common import deep_merge_dicts
from ._common import deep_to_dict


if typing.TYPE_CHECKING:
    from collections.abc import Mapping
    from collections.abc import Sequence
    from typing import Any
    from typing import TextIO

    from ruamel.yaml import Node
    from ruamel.yaml import YAML
    from ruamel.yaml.constructor import Constructor


@click.argument("file", type=click.File())
@click.option("-o", "--output", type=click.File(mode="w", atomic=True))
@click.option(
    "-I",
    "include_dirs",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    multiple=True,
)
@click.command()
def main(file: TextIO, include_dirs: Sequence[pathlib.Path], output: TextIO) -> None:
    """Expand all anchors and constructors in a YAML file."""
    yaml = ruamel.yaml.YAML(typ="safe")
    yaml.register_class(Filler)
    yaml.register_class(Const)

    for include_dir in include_dirs:
        for dirent in include_dir.iterdir():
            if not dirent.is_file() or dirent.suffix != ".yaml":
                continue
            constructor = create_constructor_class(yaml, dirent)
            yaml.register_class(constructor)

    # Load the YAML file provided. As we've already registered all the constructors, we
    # don't need to do anything special after we load it.
    resulting_yaml = yaml.load(file)

    # Set arrays to be indented two spaces underneath the keys they're mapped to. It
    # drives me crazy otherwise.
    yaml.indent(offset=2)
    yaml.dump(resulting_yaml, output)


def create_constructor_class(yaml_loader: YAML, fragment_file: pathlib.Path) -> type:
    """Create a class that implements a YAML constructor that merges in a fragment.

    Unlike PyYAML, ruamel.yaml doesn't support using a single function to implement a
    YAML constructor.
    """
    with fragment_file.open() as fd:
        try:
            fragment = yaml_loader.load(fd)
        except MarkedYAMLError as yerr:
            raise ValueError(f"Failed to load {fragment_file}: {yerr}") from None

    class_name = fragment_file.stem
    yaml_name = class_name.replace("_", "-")
    namespace = {
        "yaml_tag": "!" + yaml_name,
        "from_yaml": classmethod(
            functools.partial(
                construct_item, fragment_name=yaml_name, fragment=fragment
            )
        ),
    }

    return type(class_name, (object,), namespace)


def construct_item(
    _cls: Any,
    constructor: Constructor,
    node: Node,
    *,
    fragment_name: str,
    fragment: Mapping[str, Any],
) -> dict[str, Any]:
    """Merge a loaded dictionary from YAML with a predefined dict."""
    try:
        user_fragment = constructor.construct_mapping(node, True)
    except ConstructorError as err:
        raise ValueError(
            f"Constructor !{fragment_name} requires a dictionary as its argument."
            f" Original error: {err}"
        ) from None

    deep_map = deep_chainmap.DeepChainMap(user_fragment, dict(fragment))
    return deep_to_dict(deep_map)


class Filler:
    """A class for loading blank filler space in a file."""

    yaml_tag = "!filler"
    count = 0

    @classmethod
    def from_yaml(cls, constructor: Constructor, node: Node) -> dict[str, Any]:
        """Create a field representing filler space in a file."""
        width = constructor.construct_yaml_int(node)
        cls.count += 1
        name = "_filler" if cls.count == 1 else f"_filler_{cls.count}"
        return {
            "name": name,
            "title": "Filler",
            "type": "string",
            "constraints": {
                "enum": [""],
                "maxLength": width,
            },
        }


class Const:
    """A class for representing an immutable string in a file."""

    yaml_tag = "!const"
    count = 0

    @classmethod
    def from_yaml(cls, constructor: Constructor, node: Node) -> dict[str, Any]:
        """Create a field representing filler space in a file."""
        string_value: str
        dict_value = {}

        try:
            string_value = constructor.construct_yaml_str(node)
        except ConstructorError:
            dict_value = constructor.construct_mapping(node, True)
            string_value = dict_value.pop("__value")

        base = {
            "name": "_const" if cls.count == 1 else f"_const_{cls.count}",
            "type": "string",
            "constraints": {
                "enum": [string_value],
                "minLength": len(string_value),
                "maxLength": len(string_value),
                "required": True,
            },
        }

        return deep_merge_dicts(dict_value, base)


if __name__ == "__main__":
    main()
