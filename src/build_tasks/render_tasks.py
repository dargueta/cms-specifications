# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING

import more_itertools as mi

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
        [  # noqa: S607
            "jsonnet",
            *mi.flatten(["-J", str(d)] for d in include_dirs),
            "-o",
            str(output),
            str(source),
        ],
        check=True,
    )
