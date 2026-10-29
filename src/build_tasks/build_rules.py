# SPDX-License-Identifier: BSD-3-Clause

"""Parsing of build_rules.yaml files."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

import more_itertools as mi
import ruamel.yaml

from .versions import versions_matching
from .versions import VersionSpec


if TYPE_CHECKING:
    from pathlib import Path


@dataclasses.dataclass
class ParsedBuildRules:
    """Fully resolved build rules for a single file format."""

    identical_versions: dict[VersionSpec, list[VersionSpec]]
    file_dep_map: dict[Path, list[Path]]


def parse_build_rules(config_path: Path, source_root: Path) -> ParsedBuildRules:
    """Load a ``build_rules.yaml`` and resolve all versions and paths."""
    yaml = ruamel.yaml.YAML(typ="safe")
    with config_path.open() as fh:
        raw = yaml.load(fh) or {}

    # --- identical_versions ---
    identical_versions: dict[VersionSpec, list[VersionSpec]] = {
        VersionSpec.from_string(str(parent)): versions_matching(constraint)
        for parent, constraint in raw.get("identical_versions", {}).items()
    }

    # --- file_dependencies + identical_files -> merged dep map ---
    dep_map: dict[Path, list[Path]] = {}

    # Iterate through file_dependencies first to get a list of all files that depend on
    # other files unconditionally.
    for pattern, upstream_relpaths in raw.get("file_dependencies", {}).items():
        for upstream_relpath in mi.always_iterable(upstream_relpaths):
            parent = (source_root / upstream_relpath).resolve()
            for f in source_root.glob(str(pattern).strip()):
                if f.resolve() != parent:
                    dep_map.setdefault(f.resolve(), []).append(parent)

    # Iterate through `identical_files` to build a list of all files that need to be
    # copied/symlinked from an ancestor file.
    for group in raw.get("identical_files", []):
        source_dir = source_root / group["source_version"]
        for path in group["files"]:
            upstream = (source_dir / path).resolve()
            for version in versions_matching(group["target_versions"]):
                candidate = source_root / str(version) / path
                if candidate.resolve() != upstream and candidate.exists():
                    dep_map.setdefault(candidate.resolve(), []).append(upstream)

    return ParsedBuildRules(identical_versions, dep_map)
