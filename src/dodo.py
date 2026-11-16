# SPDX-License-Identifier: BSD-3-Clause

"""doit build configuration for CMS file format schemas.

Run ``doit list`` to see available tasks, or ``doit`` to build everything.
"""

from __future__ import annotations

import collections
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from doit import get_var

from build_tasks.constants import DEFAULT_BUILD_DIR
from build_tasks.constants import FORMATS_BASE_DIR
from build_tasks.versions import ALL_PCUG_VERSIONS


if TYPE_CHECKING:
    from collections.abc import Iterator

    from build_tasks.versions import VersionSpec


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

# DOIT_CONFIG = {
#     "default_tasks": ["build"],
#     "verbosity": 2,
# }

# BUILD_DIR = Path(
#     get_var("build_dir", str(DEFAULT_BUILD_DIR)) or DEFAULT_BUILD_DIR
# ).resolve()


def main():
    for format_root_dir in FORMATS_BASE_DIR.iterdir():
        if format_root_dir.is_dir() and not format_root_dir.stem.startswith("_"):
            LOG.info("Processing %s", format_root_dir)
            create_tasks_for_format(format_root_dir)


def create_tasks_for_format(format_root_dir: Path) -> None:
    """Create build tasks for a file format."""
    format_name = format_root_dir.stem
    record_types_root_dir = format_root_dir / "records"
    if not record_types_root_dir.exists():
        LOG.warning("Ignoring %s", record_types_root_dir)
        return

    # Find all record types by listing top-level directories inside "<format>/records/"
    # and only including those that both (A) don't start with an underscore and
    # (B) contain at least one Jsonnet file.
    for dirent in record_types_root_dir.iterdir():
        if (
            dirent.is_dir()
            and (not dirent.stem.startswith("_"))
            and any(dirent.glob("*.jsonnet"))
        ):
            LOG.info("Found format %r record type %r", format_name, dirent.stem)
            create_tasks_for_record(format_name, dirent)


def create_tasks_for_record(format_name: str, record_type_root_dir: Path):
    record_name = record_type_root_dir.stem
    schema_file_to_versions = collections.defaultdict(list)
    last_defined_schema_file: Path | None = None
    last_defined_version: VersionSpec | None = None
    removed_at: VersionSpec | None = None

    for this_version in ALL_PCUG_VERSIONS:
        schema_file = record_type_root_dir / f"{this_version}.jsonnet"
        removed_sentinel_file = record_type_root_dir / f"{this_version}.removed"

        if schema_file.exists():
            LOG.debug(
                "format=%r record=%r v%s: NEW",
                format_name,
                record_name,
                this_version,
            )
            schema_file_to_versions[schema_file].append(this_version)
            last_defined_schema_file = schema_file
            last_defined_version = this_version
            removed_at = None
        elif removed_sentinel_file.exists():
            LOG.debug(
                "format=%r record=%r v%s: REMOVED",
                format_name,
                record_name,
                this_version,
            )
            removed_at = this_version
        elif removed_at:
            LOG.debug(
                "format=%r record=%r v%s: ignored, was marked deleted in v%s",
                format_name,
                record_name,
                this_version,
                removed_at,
            )
        elif last_defined_schema_file:
            LOG.debug(
                "format=%r record=%r v%s: inherits v%s",
                format_name,
                record_name,
                this_version,
                last_defined_version,
            )
            schema_file_to_versions[last_defined_schema_file].append(this_version)
        else:
            LOG.info(
                "format=%r record=%r v%s: unsupported (no schema file, no ancestor)",
                format_name,
                record_name,
                this_version,
            )


main()
