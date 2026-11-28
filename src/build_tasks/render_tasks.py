# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import _jsonnet
from ruamel.yaml import YAML


if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


def run_render_jsonnet(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Render the Jsonnet file at `source` into a YAML file at `output`.

    Jsonnet evaluates to JSON, which is parsed and re-emitted as block-style YAML.
    Key order from the Jsonnet source is preserved.

    Arguments:
        source: The Jsonnet file to evaluate.
        output: Where to write the YAML. Parent directories are created as needed.
        include_dirs: Additional directories to search when resolving ``import``
            statements, after the importing file's own directory.
    """
    result = _jsonnet.evaluate_file(
        str(source), jpathdir=[str(s) for s in include_dirs]
    )
    data = json.loads(result)

    yaml = YAML()
    yaml.default_flow_style = False

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fd:
        yaml.dump(data, fd)
