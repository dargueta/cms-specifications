# SPDX-License-Identifier: BSD-3-Clause

"""Build task generation for CMS file format schemas."""

from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

from .constants import DEFAULT_BUILD_DIR
from .constants import FORMAT_SOURCE_DIRS_BY_NAME
from .format_tasks import generate_tasks_for_format


if TYPE_CHECKING:
    from pathlib import Path


TaskDict = dict[str, Any]


def generate_all_tasks(build_dir: Path = DEFAULT_BUILD_DIR) -> list[TaskDict]:
    """Generate doit task dicts for all known file formats."""
    tasks: list[TaskDict] = []
    for source_path in FORMAT_SOURCE_DIRS_BY_NAME.values():
        tasks.extend(generate_tasks_for_format(source_path, build_dir=build_dir))
    return tasks
