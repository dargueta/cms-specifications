# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

from typing import TYPE_CHECKING

import _jsonnet


if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


def run_render_jsonnet(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Render the jsonnet file at `source` into `output`."""
    result = _jsonnet.evaluate_file(
        str(source), jpathdir=[str(s) for s in include_dirs]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result, encoding="utf-8")
