# SPDX-License-Identifier: BSD-3-Clause

"""doit build configuration for CMS file format schemas.

Run ``doit list`` to see available tasks, or ``doit`` to build everything.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import doit_api
from doit import get_var
from doit_api import pytask

from build_tasks.constants import DEFAULT_BUILD_DIR
from build_tasks.constants import FORMAT_SOURCE_DIRS_BY_NAME
from build_tasks.format_tasks import generate_tasks_for_format


if TYPE_CHECKING:
    from collections.abc import Iterator


DOIT_CONFIG = {
    "default_tasks": ["build"],
    "verbosity": 2,
}

BUILD_DIR = Path(
    get_var("build_dir", str(DEFAULT_BUILD_DIR)) or DEFAULT_BUILD_DIR
).resolve()


@pytask(targets=[BUILD_DIR], uptodate=[BUILD_DIR.is_dir])
def create_build_dir() -> None:
    """Create the build output directory."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)


def _make_format_taskgen(format_name: str, source_path: Path) -> doit_api.taskgen:
    def _generate() -> Iterator[doit_api.task]:
        yield from generate_tasks_for_format(
            format_name,
            source_path,
            build_dir=BUILD_DIR,
            extra_task_dep=[create_build_dir],
        )

    return doit_api.taskgen(name=format_name, doc=f"Build all {format_name} outputs")(
        _generate
    )


for _format_name, _source_path in sorted(FORMAT_SOURCE_DIRS_BY_NAME.items()):
    globals()[_format_name] = _make_format_taskgen(_format_name, _source_path)
del _format_name, _source_path

build = doit_api.task(
    name="build",
    actions=[],
    tell_why_am_i_running=False,
    doc="Build all file format outputs",
    task_dep=[f"{name}:*" for name in sorted(FORMAT_SOURCE_DIRS_BY_NAME)],
)
