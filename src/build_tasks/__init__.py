# SPDX-License-Identifier: BSD-3-Clause

"""Build task generation for CMS file format schemas."""

from __future__ import annotations

from typing import Any

from .constants import FORMAT_SOURCE_DIRS_BY_NAME
from .format_tasks import generate_tasks_for_format


TaskDict = dict[str, Any]


def generate_all_tasks() -> list[TaskDict]:
    """Generate doit task dicts for all known file formats."""
    tasks: list[TaskDict] = []
    for source_path in FORMAT_SOURCE_DIRS_BY_NAME.values():
        tasks.extend(generate_tasks_for_format(source_path))
    return tasks
