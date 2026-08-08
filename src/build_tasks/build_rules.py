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

    # --- identical-versions ---
    identical_versions: dict[VersionSpec, list[VersionSpec]] = {
        VersionSpec.from_string(str(parent)): versions_matching(constraint)
        for parent, constraint in raw.get("identical-versions", {}).items()
    }

    # --- file-dependencies + identical-files -> merged dep map ---
    dep_map: dict[Path, list[Path]] = {}

    # Iterate through file-dependencies first to get a list of all files that depend on
    # other files unconditionally.
    for parent_relpath, pattern_spec in raw.get("file-dependencies", {}).items():
        parent = (source_root / parent_relpath).resolve()
        for pattern in mi.always_iterable(pattern_spec):
            for f in source_root.glob(str(pattern).strip()):
                if f.resolve() != parent:
                    dep_map.setdefault(f.resolve(), []).append(parent)

    for group in raw.get("identical-files", []):
        source_dir = source_root / group["source"]
        for filename in group["files"]:
            upstream = (source_dir / filename).resolve()
            for version in versions_matching(group["versions"]):
                candidate = source_root / str(version) / "records" / filename
                if candidate.resolve() != upstream and candidate.exists():
                    dep_map.setdefault(candidate.resolve(), []).append(upstream)

    return ParsedBuildRules(identical_versions, dep_map)
