# SPDX-License-Identifier: BSD-3-Clause

"""Create tasks for each PCUG file format."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

import doit_api

from .build_rules import parse_build_rules
from .file_ops import link_or_copy
from .render_tasks import render_template_task
from .render_tasks import yaml_postprocess_tasks


if TYPE_CHECKING:
    from collections.abc import Collection
    from collections.abc import Iterator
    from collections.abc import Mapping
    from collections.abc import MutableMapping
    from collections.abc import Sequence

    from .versions import VersionSpec


LOG = logging.getLogger(__name__)


def _iter_version_dirs(source_path: Path) -> Iterator[Path]:
    """Yield the version subdirectories of a format's source directory, sorted."""
    for version_dir in sorted(source_path.iterdir()):
        if re.match(r"\d+\.\d+$", version_dir.name) and version_dir.is_dir():
            yield version_dir


def _record_type(source_file: Path) -> str:
    """Return the record type name: the filename stem up to the first `.`."""
    return source_file.name.split(".", 1)[0]


def _record_type_tasks(  # noqa: PLR0913, PLR0917
    format_name: str,
    version: str,
    record_type: str,
    source_file: Path,
    version_build_dir: Path,
    extra_file_deps: Collection[Path] = (),
) -> Iterator[doit_api.task]:
    """Generate the render/postprocess/yaml stage tasks for a single source file."""
    if source_file.suffix == ".jinja2":
        rendered_name = source_file.stem
        is_yaml = Path(rendered_name).suffix == ".yaml"

        # YAML requires special handling. We need to render the file first, and then
        # run it through an additional pass that converts it to JSON to get rid of all
        # the custom constructors.
        if is_yaml:
            rendered_path = version_build_dir / (
                Path(rendered_name).stem + ".rendered.yaml"
            )
        else:
            rendered_path = version_build_dir / rendered_name

        yield render_template_task(
            source_file,
            rendered_path,
            extra_file_deps,
            version=version,
            record_type=record_type,
        )

        if is_yaml:
            postprocess_tasks = yaml_postprocess_tasks(
                rendered_path,
                version_build_dir,
                output_stem=Path(rendered_name).stem,
                version=version,
                record_type=record_type,
            )
            # Clean up intermediate rendered YAML when `doit clean` is run.
            postprocess_tasks[-1].clean = [
                (Path.unlink, [rendered_path], {"missing_ok": True}),
            ]
            yield from postprocess_tasks
        # Non-YAML template files are already handled by the render task.
    elif source_file.suffix == ".yaml":
        # If we get here then the source file is YAML but *not* templated.
        yield from yaml_postprocess_tasks(
            source_file,
            version_build_dir,
            extra_file_deps,
            version=version,
            record_type=record_type,
        )
        return
    else:
        # Not YAML, not templated...
        LOG.warning(
            "Not sure what to do with this file in format %r: %s",
            format_name,
            source_file,
        )
        return

    # No-op grouping task: `doit {format}:{version}:{record_type}` builds every stage.
    yield doit_api.task(
        name=f"{version}:{record_type}",
        actions=[],
        task_dep=[f"{version}:{record_type}:*"],
    )


def _version_tasks(
    format_name: str,
    version_dir: Path,
    target_root: Path,
    dep_map: Mapping[Path, Collection[Path]],
    *,
    extra_task_dep: Collection[object] = (),
) -> Iterator[doit_api.task]:
    """Generate the render/postprocess/yaml/group tasks for one version directory."""
    version = version_dir.name
    records_dir = version_dir / "records"
    if not records_dir.exists():
        LOG.debug(
            "Format %r version %s has no records directory; skipping.",
            format_name,
            version,
        )
        return

    version_build_dir = target_root / version / "records"
    produced_any = False

    for source_file in sorted(records_dir.iterdir()):
        if not source_file.is_file():
            continue

        record_type = _record_type(source_file)
        extra_deps = dep_map.get(source_file.resolve(), [])

        for t in _record_type_tasks(
            format_name,
            version,
            record_type,
            source_file,
            version_build_dir,
            extra_deps,
        ):
            if t.actions:
                # Only real leaf tasks need to depend on the build dir existing; the
                # no-op grouping tasks don't run any actions.
                t.task_dep = [*(t.task_dep or []), *extra_task_dep]
            produced_any = True
            yield t

    if produced_any:
        # No-op grouping task: `doit {format}:{version}` builds every record type.
        yield doit_api.task(name=version, actions=[], task_dep=[f"{version}:*"])


def _clone_tasks(
    format_name: str,
    parent_version: VersionSpec,
    children: Sequence[VersionSpec],
    format_build_root: Path,
    already_handled: MutableMapping[VersionSpec, str],
) -> Iterator[doit_api.task]:
    """Create tasks that symlink/copy child version directories from a parent."""
    child_set = set(children)
    collisions = child_set & already_handled.keys()

    if collisions:
        raise ValueError(
            f"In {format_name!r} build rules, some versions are generated by multiple"
            " parents. This likely means the constraints are too lax.\n"
            f"Parent: {parent_version}\n"
            f"Children: {', '.join(map(str, children))}\n"
            "Collisions:\n - "
            + "\n - ".join(
                f"{v} already generated by {already_handled[v]}" for v in collisions
            )
        )

    parent_dir = format_build_root / str(parent_version)

    if len(children) <= 2:
        child_version_strings = ", ".join(map(str, children))
    else:
        # In all likelihood, child versions of a parent version will be one contiguous
        # range. Rather than flood the terminal with a full list of all versions, just
        # list the first and last.
        child_version_strings = f"{children[0]} through {children[-1]}"

    for child in children:
        child_dir = format_build_root / str(child)
        yield doit_api.task(
            name=f"{child}:_clone",
            doc=f"Clone {format_name} v{parent_version} to {child_version_strings}",
            actions=[(link_or_copy, [parent_dir, [child_dir]])],
            task_dep=[f"{format_name}:{parent_version}"],
            uptodate=[child_dir.exists()],
            targets=[str(child_dir)],
        )
        # No-op grouping task so `doit {format}:{child}` works uniformly with
        # non-cloned versions.
        yield doit_api.task(name=str(child), actions=[], task_dep=[f"{child}:*"])

    already_handled.update(dict.fromkeys(children, str(parent_version)))


def generate_tasks_for_format(
    format_name: str,
    source_path: Path,
    *,
    build_dir: Path,
    extra_task_dep: Collection[object] = (),
) -> Iterator[doit_api.task]:
    """Generate all doit tasks for a given file format."""
    build_rules_file = source_path / "build_rules.yaml"

    if not build_rules_file.exists():
        LOG.warning(
            "Format %r doesn't have the required build rules file. Ignoring for now,"
            " but this may become an error in the future.",
            format_name,
        )
        return

    rules = parse_build_rules(build_rules_file, source_path)

    target_root = build_dir / format_name
    already_handled: dict[VersionSpec, str] = {}
    built_versions: set[str] = set()

    # File tasks first. These also create per-version grouping tasks that
    # `_clone_tasks` needs in order to create the copying tasks.
    for version_dir in _iter_version_dirs(source_path):
        version_tasks = list(
            _version_tasks(
                format_name,
                version_dir,
                target_root,
                rules.file_dep_map,
                extra_task_dep=extra_task_dep,
            )
        )
        if version_tasks:
            built_versions.add(version_dir.name)
        yield from version_tasks

    for parent_version, children in rules.identical_versions.items():
        if str(parent_version) not in built_versions:
            LOG.debug(
                "Skipping identical-version rule for %s v%s: no file tasks found.",
                format_name,
                parent_version,
            )
            continue

        already_handled[parent_version] = "(Defined)"
        yield from _clone_tasks(
            format_name=format_name,
            parent_version=parent_version,
            children=children,
            format_build_root=target_root,
            already_handled=already_handled,
        )
