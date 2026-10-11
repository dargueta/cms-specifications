# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING

import doit_api
import more_itertools as mi

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


def run_apply_diff(source: Path, output: Path, format_root_dir: Path) -> None:
    """Run applying a JSON diff."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "scripts.apply_diff",
            "-o",
            str(output),
            str(format_root_dir),
            str(source),
        ],
        env={"PYTHONPATH": construct_pythonpath()},
        check=True,
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


def create_apply_diff_task(
    source_file: Path,
    output_path: Path,
    format_root_dir: Path,
    version: str,
    record_type: str,
) -> doit_api.task:
    """Generate a JSON file by applying a diff given by another file."""
    return doit_api.task(
        name=f"{version}:{record_type}:render",
        actions=[
            (
                run_apply_diff,
                [],
                {
                    "source": source_file,
                    "output": output_path,
                    "format_root_dir": format_root_dir,
                },
            ),
        ],
        file_dep=[str(source_file)],
        targets=[str(output_path)],
    )
