# SPDX-License-Identifier: BSD-3-Clause

"""doit build configuration for CMS file format schemas.

Run ``doit list`` to see available tasks, or ``doit`` to build everything.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

import doit
import doit_api

from build_tasks.constants import DEFAULT_BUILD_DIR
from build_tasks.constants import FORMATS_BASE_DIR
from build_tasks.file_ops import cleanup_intermediate
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

# Matches `import 'x'`, `importstr "x"`, and `importbin 'x'`. Group 1 is the keyword,
# group 3 is the imported path.
_IMPORT_RE = re.compile(r"""\b(import|importstr|importbin)\s+(['"])(.+?)\2""")


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


def _output_path(format_name: str, version: VersionSpec) -> Path:
    """Return the path of the generated ODCS file for a format and PCUG version."""
    return BUILD_DIR / format_name / f"{version}.odcs.yaml"


def _resolve_import(importer: Path, imported: str) -> Path | None:
    """Resolve an import path the same way Jsonnet does.

    Jsonnet first looks relative to the directory of the importing file, then in each
    library search directory. The only search directory used here is
    `FORMATS_BASE_DIR`.

    Arguments:
        importer: The file containing the ``import`` statement.
        imported: The path string from the ``import`` statement.

    Returns:
        The resolved absolute path, or None if the file can't be found.
    """
    for candidate in (importer.parent / imported, FORMATS_BASE_DIR / imported):
        if candidate.is_file():
            return candidate.resolve()
    return None


def find_jsonnet_dependencies(source: Path) -> list[Path]:
    """Find every file that `source` imports, directly or indirectly.

    Imports are found with a regular expression, not a real parser, so an import
    inside a comment or string is also counted. That only adds a harmless extra
    dependency. Imports that can't be resolved are logged and skipped; Jsonnet itself
    will report an error if the import is real.

    Only ``import`` targets are scanned recursively. ``importstr`` and ``importbin``
    targets are raw data, so they are dependencies but contain no imports of their own.

    Arguments:
        source: The Jsonnet file to scan.

    Returns:
        A sorted list of the resolved paths of all dependencies, not including
        `source` itself.
    """
    source = source.resolve()
    seen: set[Path] = {source}
    to_scan = [source]

    while to_scan:
        current = to_scan.pop()
        text = current.read_text(encoding="utf-8")
        for match in _IMPORT_RE.finditer(text):
            keyword, imported = match.group(1), match.group(3)
            resolved = _resolve_import(current, imported)
            if resolved is None:
                LOG.warning("%s: can't resolve import %r", current, imported)
                continue
            if resolved in seen:
                continue
            seen.add(resolved)
            if keyword == "import":
                to_scan.append(resolved)

    seen.discard(source)
    return sorted(seen)


def create_tasks_for_pcug_file_format(format_root_dir: Path) -> Iterator[doit_api.task]:
    """Create build tasks for every PCUG version of a file format.

    Each ``<format>/versions/<V>.jsonnet`` file is rendered to ``<V>.odcs.yaml`` in
    the build directory. A PCUG version with no file of its own inherits the most
    recent earlier version, so its output is a link to that version's output. A
    ``<format>/versions/<V>.removed`` file stops this inheritance from version V
    onward, until the next version that has its own Jsonnet file.
    """
    format_name = format_root_dir.stem
    versions_dir = format_root_dir / "versions"
    if not versions_dir.is_dir():
        LOG.warning("Ignoring %s: no versions/ directory", format_root_dir)
        return

    last_defined_version: VersionSpec | None = None
    removed_at: VersionSpec | None = None

    for this_version in ALL_PCUG_VERSIONS:
        schema_file = versions_dir / f"{this_version}.jsonnet"
        removed_sentinel_file = versions_dir / f"{this_version}.removed"

        if schema_file.exists():
            LOG.debug("format=%r v%s: NEW", format_name, this_version)
            last_defined_version = this_version
            removed_at = None
            yield create_jsonnet_render_task(
                format_name=format_name,
                pcug_version=this_version,
                source_file=schema_file,
                target_file=_output_path(format_name, this_version),
            )
        elif removed_sentinel_file.exists():
            LOG.debug("format=%r v%s: REMOVED", format_name, this_version)
            removed_at = this_version
        elif removed_at:
            LOG.debug(
                "format=%r v%s: ignored, was marked removed in v%s",
                format_name,
                this_version,
                removed_at,
            )
        elif last_defined_version:
            LOG.debug(
                "format=%r v%s: inherits v%s",
                format_name,
                this_version,
                last_defined_version,
            )
            yield create_copy_rendered_file_task(
                format_name=format_name,
                ancestor_version=last_defined_version,
                this_version=this_version,
                rendered_source_file=_output_path(format_name, last_defined_version),
                target_file=_output_path(format_name, this_version),
            )
        else:
            LOG.info(
                "format=%r v%s: unsupported (no schema file, no ancestor)",
                format_name,
                this_version,
            )


def create_jsonnet_render_task(
    format_name: str,
    pcug_version: VersionSpec,
    source_file: Path,
    target_file: Path,
) -> doit_api.task:
    """Create the task for rendering a Jsonnet file to ODCS YAML.

    The task depends on `source_file` and on every file it imports, directly or
    indirectly, so editing any shared fragment rebuilds every version that uses it.
    """
    return doit_api.task(
        # doit_api.taskgen prefixes this with "<format_name>:" automatically.
        name=str(pcug_version),
        doc=f"Render {format_name} v{pcug_version}",
        file_dep=[source_file, *find_jsonnet_dependencies(source_file)],
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
        clean=True,
    )


def create_copy_rendered_file_task(
    format_name: str,
    ancestor_version: VersionSpec,
    this_version: VersionSpec,
    rendered_source_file: Path,
    target_file: Path,
) -> doit_api.task:
    """Create the task that makes an inherited version's output from its ancestor's.

    `target_file` becomes a link to (or, if linking isn't possible, a copy of)
    `rendered_source_file`. Any existing target is deleted first, so a copy is
    refreshed whenever the ancestor changes.
    """
    return doit_api.task(
        # doit_api.taskgen prefixes this with "<format_name>:" automatically.
        name=f"{this_version}:_clone",
        doc=f"Clone {format_name} v{ancestor_version} to v{this_version}",
        actions=[
            (cleanup_intermediate, [target_file]),
            (link_or_copy, [rendered_source_file, [target_file]]),
        ],
        file_dep=[rendered_source_file],
        targets=[target_file],
        clean=True,
    )
