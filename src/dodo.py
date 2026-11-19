# SPDX-License-Identifier: BSD-3-Clause

"""doit build configuration for CMS file format schemas.

Run ``doit list`` to see available tasks, or ``doit`` to build everything.
"""

from __future__ import annotations

import collections
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import doit
import doit_api

from build_tasks.constants import DEFAULT_BUILD_DIR
from build_tasks.constants import FORMATS_BASE_DIR
from build_tasks.file_ops import link_or_copy
from build_tasks.render_tasks import run_render_jsonnet
from build_tasks.versions import ALL_PCUG_VERSIONS


if TYPE_CHECKING:
    from collections.abc import Iterator

    from build_tasks.versions import VersionSpec


logging.basicConfig(format="%(levelname)-8s %(message)s")
LOG = logging.getLogger(__name__)


DOIT_CONFIG = {"default_tasks": ["build"], "verbosity": 2}

BUILD_DIR = Path(
    doit.get_var("build_dir", str(DEFAULT_BUILD_DIR)) or DEFAULT_BUILD_DIR
).resolve()


build = doit_api.task(
    name="build",
    actions=[],
    tell_why_am_i_running=False,
    doc="Build all file format outputs",
    task_dep=[
        f"{path.stem}:*"
        for path in sorted(FORMATS_BASE_DIR.iterdir())
        if path.is_dir() and not path.stem.startswith("_")
    ],
)


def _create_generator_for_format(format_dir: Path) -> doit_api.taskgen:
    """Create the generator task for the given format."""

    @doit_api.taskgen(
        name=format_dir.stem, doc=f"Generate files for {format_dir.stem!r}"
    )
    def _generate() -> Iterator[doit_api.task]:
        yield from create_tasks_for_pcug_file_format(format_dir)

    return _generate


for _format_dir in FORMATS_BASE_DIR.iterdir():
    if not _format_dir.is_dir() or _format_dir.stem.startswith("_"):
        continue

    LOG.info("Processing %s", _format_dir)
    globals()[_format_dir.stem] = _create_generator_for_format(_format_dir)


def create_tasks_for_pcug_file_format(format_root_dir: Path) -> Iterator[doit_api.task]:
    """Create build tasks for a file format."""
    format_name = format_root_dir.stem
    record_types_root_dir = format_root_dir / "records"
    if not record_types_root_dir.exists():
        LOG.warning("Ignoring %s", record_types_root_dir.parent)
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
            yield from create_tasks_for_record(format_name, dirent)


def create_tasks_for_record(
    format_name: str, record_type_root_dir: Path
) -> Iterator[doit_api.task]:
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

            yield create_jsonnet_render_task(
                format_name,
                record_name,
                this_version,
                schema_file,
                schema_file.with_suffix(".json"),
            )
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
            yield create_copy_rendered_file_task(
                format_name=format_name,
                record_name=record_name,
                ancestor_version=last_defined_version,
                this_version=this_version,
                rendered_source_file=last_defined_schema_file.with_suffix(".json"),
                target_file=schema_file.with_suffix(".json"),
            )
        else:
            LOG.info(
                "format=%r record=%r v%s: unsupported (no schema file, no ancestor)",
                format_name,
                record_name,
                this_version,
            )


def create_jsonnet_render_task(
    format_name: str,
    record_name: str,
    pcug_version: VersionSpec,
    source_file: Path,
    target_file: Path,
) -> doit_api.task:
    """Create the task for rendering a Jsonnet file to JSON."""
    return doit_api.task(
        name=f"{format_name}:{record_name}:{pcug_version}",
        doc=f"{format_name=} {record_name=} {pcug_version=}",
        file_dep=[source_file],
        targets=[target_file],
        actions=[
            (
                run_render_jsonnet,
                [],
                {
                    "source": source_file,
                    "output": target_file,
                    "include_dirs": [FORMATS_BASE_DIR],
                },
            ),
        ],
    )


def create_copy_rendered_file_task(
    format_name: str,
    record_name: str,
    ancestor_version: VersionSpec,
    this_version: VersionSpec,
    rendered_source_file: Path,
    target_file: Path,
) -> doit_api.task:
    return doit_api.task(
        name=f"{format_name}:{record_name}:{this_version}:_clone",
        doc=f"Clone format {format_name} record {record_name} v{ancestor_version} to"
        " v{this_version}",
        actions=[(link_or_copy, [rendered_source_file, [target_file]])],
        file_dep=[rendered_source_file],
        uptodate=[target_file.exists],
        targets=[target_file],
    )
