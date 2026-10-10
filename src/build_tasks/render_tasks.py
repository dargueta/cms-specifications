# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import TYPE_CHECKING

import doit_api
import more_itertools as mi
import ruamel.yaml

from .constants import COMMON_INCLUDE_DIR
from .constants import FORMATS_BASE_DIR
from .constants import SCHEMAS_SOURCE_DIR


if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


def construct_pythonpath() -> str:
    """Construct a PYTHONPATH to pass to subprocess invocations of Python."""
    return ":".join((*sys.path, str(SCHEMAS_SOURCE_DIR)))


def run_render_jsonnet(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Render the jsonnet file at `source` into `output`."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            "jsonnet",
            *mi.flatten(["-J", str(d)] for d in include_dirs),
            "-o",
            str(output),
            str(source),
        ],
        check=True,
    )


def run_postprocess_json(source: Path, output: Path) -> None:
    """Apply changes in the `__changes__` key of a JSON file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "scripts.postprocess_json",
            "-o",
            str(output),
            str(source),
        ],
        check=True,
        env={"PYTHONPATH": construct_pythonpath()},
    )


def create_json_postprocess_task(
    source: Path, target: Path, version: str, record_type: str
) -> doit_api.task:
    """Create the task to render a JSON file's `__changes__` list.

    Many records differ by only a few fields. Unfortunately, we can't override field
    definitions by name, because they're defined in a list. A specialized postprocessing
    task will allow us to specify changes in terms of a field name.

    Arguments:
        source (pathlib.Path):
            A valid JSONnet file that needs to be processed.
        target (pathlib.Path):
            The file to write the rendered (albeit unprocessed) JSON output to.
        version (str):
            The PCUG version that this file is for.
        record_type (str):
            The type of the record that the file describes, such as "header", "trailer",
            etc., not the file type.
    """
    return doit_api.task(
        name=f"{version}:{record_type}:postprocess",
        actions=[
            (run_postprocess_json, [], {"source": source, "output": target}),
        ],
        file_dep=[str(source)],
        targets=[str(target)],
    )


def create_render_jsonnet_task(
    source_file: Path,
    output_path: Path,
    version: str,
    record_type: str,
    extra_file_deps: Iterable[Path] = (),
) -> doit_api.task:
    """Return a task for rendering a JSONnet file."""
    return doit_api.task(
        name=f"{version}:{record_type}:render",
        actions=[
            (
                run_render_jsonnet,
                [],
                {
                    "source": source_file,
                    "output": output_path,
                    "include_dirs": [FORMATS_BASE_DIR],
                },
            ),
        ],
        file_dep=[str(source_file), *extra_file_deps],
        targets=[str(output_path)],
    )
