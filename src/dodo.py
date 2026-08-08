# SPDX-License-Identifier: BSD-3-Clause

"""doit build configuration for CMS file format schemas.

Run ``doit list`` to see available tasks, or ``doit`` to build everything.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from doit import get_var
from doit_api import pytask

from build_tasks.constants import DEFAULT_BUILD_DIR
from build_tasks.constants import FORMAT_SOURCE_DIRS_BY_NAME
from build_tasks.format_tasks import generate_tasks_for_format


if TYPE_CHECKING:
    from collections.abc import Iterator

    from .build_tasks import TaskDict


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


def task_build() -> Iterator[TaskDict]:
    """Build all file format outputs."""
    for format_name, source_path in sorted(FORMAT_SOURCE_DIRS_BY_NAME.items()):
        subtasks = generate_tasks_for_format(source_path, build_dir=BUILD_DIR)
        subtask_names = [f"build:{t['name']}" for t in subtasks]
        for subtask in subtasks:
            subtask.setdefault("task_dep", []).append("create_build_dir")
            yield subtask

        # Group task per format: `doit build:bqn4` builds all bqn4 subtasks.
        yield {
            "name": format_name,
            "actions": None,
            "doc": f"Build all {format_name} outputs",
            "task_dep": subtask_names,
        }
