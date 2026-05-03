# SPDX-License-Identifier: BSD-3-Clause

"""Parsing of build_rules.ini files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .versions import enumerate_versions_matching_constraints
from .versions import VersionSpec


if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path


def enumerate_identical_versions(
    build_rules: Mapping[str, Mapping[str, str]],
) -> dict[VersionSpec, list[VersionSpec]]:
    """Find all versions declared to be identical to another version.

    In the "identical-versions" section of the ``build_rules.ini`` file, all keys
    indicate a concrete defined version, and all values are versions generated from this
    concrete version.
    """
    if "identical-versions" not in build_rules:
        return {}

    result = enumerate_versions_matching_constraints(build_rules["identical-versions"])
    return {VersionSpec.from_string(k): v for k, v in result.items()}


def enumerate_identical_files(
    build_rules: Mapping[str, Mapping[str, str]], source_root: Path
) -> dict[Path, list[Path]]:
    """Get a list of individual files derived from another.

    Most formats have entire versions that are identical to each other, not individual
    files. Usually, this only happens when a format has multiple record types, and only
    a subset of them change between versions.
    """
    result = {}
    if "identical-files" not in build_rules:
        return result

    for upstream_file_relpath, raw_constraint_spec in build_rules[
        "identical-files"
    ].items():
        upstream_file_path = (source_root / upstream_file_relpath).resolve()

        version_constraints = enumerate_versions_matching_constraints(
            {"_": raw_constraint_spec}
        )["_"]

        downstream_files = []
        for version in version_constraints:
            candidate = source_root / str(version) / "records" / upstream_file_path.name
            if candidate.resolve() != upstream_file_path and candidate.exists():
                downstream_files.append(candidate.resolve())

        if downstream_files:
            result[upstream_file_path] = downstream_files

    return result


def enumerate_file_dependencies(
    build_rules: Mapping[str, Mapping[str, str]], source_root: Path
) -> dict[Path, list[Path]]:
    """Parse the [file-dependencies] section.

    Returns a mapping from parent template paths to the downstream files that depend on
    them (resolved via glob patterns).
    """
    result = {}
    if "file-dependencies" not in build_rules:
        return result

    for parent_relpath, glob_pattern in build_rules["file-dependencies"].items():
        parent_path = (source_root / parent_relpath).resolve()
        dependents = [
            f.resolve()
            for f in source_root.glob(glob_pattern.strip())
            if f.resolve() != parent_path
        ]
        if dependents:
            result[parent_path] = dependents

    return result
