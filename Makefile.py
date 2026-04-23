# SPDX-License-Identifier: BSD-3-Clause

"""A Makefile for use with `pymake`.

You must install the pymake command with `pip3 install hayeah-pymake`. Do not install
the myriad of other Python packages that have `pymake` in the name.
"""

from __future__ import annotations

import configparser
import dataclasses
import logging
import operator
import re
import typing
from pathlib import Path
from typing import ClassVar
from typing import TypeAlias

from pymake import sh
from pymake import task


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping
    from typing import Self


VersionSpec: TypeAlias = tuple[int, int]


LOG = logging.getLogger(__name__)

HERE = Path(__file__).parent
BUILD_DIR = HERE / "build"
SOURCE_DIR = HERE / "src"
SCHEMAS_SOURCE_DIR = SOURCE_DIR / "schemas"
FORMATS_BASE_DIR = SCHEMAS_SOURCE_DIR / "file_formats"

ALL_PCUG_VERSIONS: list[VersionSpec] = [
    # Versions 5 through 14 all have minor versions 0-3, except "7.3" may not exist.
    *((major, minor) for minor in range(4) for major in range(1, 15)),
    # 15 and 16 have minor versions 0-4.
    *((major, minor) for minor in range(5) for major in (15, 16)),
    # 17 and 18 have minor versions 0-9.I can't find the PDF for 17.0, but every other
    # major version has a minor version 0 so I assume it exists.
    *((major, minor) for minor in range(10) for major in (17, 18)),
    # 19.0 is the most recent version as of 2026-04-20.
    (19, 0),
]
ALL_PCUG_VERSIONS.remove((7, 3))  # I can't find mention of v7.3 anywhere.


ALL_SCHEMA_SOURCE_DIRS = [
    p for p in FORMATS_BASE_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")
]

#: Paths to the source directories of each supported PCUG file format, by format name.
#:
#: All subdirectories of `ALL_SCHEMA_SOURCE_DIRS` that are *not* the name of a PCUG file
#: format *must* start with an underscore.
FORMAT_SOURCE_DIRS_BY_NAME = {
    p.name: p for p in ALL_SCHEMA_SOURCE_DIRS if not p.name.startswith("_")
}

#: Like FORMAT_SOURCE_DIRS_BY_NAME, but these point to the build directories.
FORMAT_BUILD_DIRS_BY_NAME = {
    name: BUILD_DIR / name for name in FORMAT_SOURCE_DIRS_BY_NAME
}


def main() -> None:
    """Initialization code to run upon import."""
    for format_name, source_path in FORMAT_SOURCE_DIRS_BY_NAME.items():
        generate_tasks_for_format(format_name, source_path)


@task(outputs=[BUILD_DIR])
def create_build_dir() -> None:
    """Create the build directory."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)


@dataclasses.dataclass(frozen=True)
class VersionConstraint:
    """A specification for comparing versions against a single constraint."""

    comparison: str
    major: int
    minor: int

    CHECKS: ClassVar[dict[str, Callable[..., bool]]] = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "!=": operator.ne,
    }

    @classmethod
    def from_spec_string(cls, spec: str) -> Self:
        """Parse a specification into a class that can compare versions."""
        parts = re.match(
            r"^(?P<constraint>[><=!]+)?(?P<major>\d+)\.(?P<minor>)\d+)$",
            spec.replace(" ", ""),
        )
        if not parts:
            raise ValueError(f"Invalid constraint definition: {spec!r}")

        return cls(
            comparison=parts["constraint"] or "==",
            major=int(parts["major"]),
            minor=int(parts["minor"]),
        )

    def check(self, version: tuple[int, int]) -> bool:
        """Check the given version against this constraint."""
        comparator = self.CHECKS.get(self.comparison)
        if not comparator:
            raise ValueError(f"Unexpected version check: {self.comparison!r}")
        return comparator((self.major, self.minor), version)

    def __post_init__(self) -> None:
        if self.comparison not in self.CHECKS:
            raise ValueError(
                f"Invalid comparator: {self.comparison!r} not one of "
                + ", ".join(self.CHECKS.keys())
            )


def generate_tasks_for_format(format_name: str, source_path: Path) -> None:
    """Register tasks to generate all output files for the given format."""
    # A file named build_rules.ini will tell us how to generate versions.
    build_rules_file = source_path / "build_rules.ini"
    if not build_rules_file.exists():
        LOG.error()
        return

    build_rules = configparser.ConfigParser().read(build_rules_file)

    identical_versions = enumerate_identical_versions(build_rules)
    identical_files = enumerate_identical_files(build_rules)


def enumerate_identical_versions(
    build_rules: Mapping[str, Mapping[str, str]],
) -> dict[VersionSpec, list[VersionSpec]]:
    """Find all versions declared to be identical to another version.

    In the "identical-versions" section of the `build_rules.ini` file, all keys indicate
    a concrete defined version, and all values are versions generated from this concrete
    version.

    For example, if we have "5.0: >=5.1, <=8.0" that means that version 5.0 must exist
    in the source tree, and all PCUG versions from 5.1 through 8.0 are identical to it.

    Arguments:
        build_rules:
            The build rules associated with this file format. If the
            `identical-versions` section is missing or empty, this is taken to mean that
            no supported version has any derived versions.

    Returns:
        A mapping of versions to a list of all versions identical to it. This list is
        guaranteed to be in ascending order.
    """
    identical_versions = build_rules.get("identical-versions")

    # Some formats don't have any versions that are identical to another. This is fine.
    if not identical_versions:
        return {}

    result = {}
    for parent_version_string, child_version_spec in identical_versions.items():
        parent_version = tuple(parent_version_string.split("."))
        constraints = [
            VersionConstraint.from_spec_string(s) for s in child_version_spec.split(",")
        ]

        # If there are no constraints, it's just an explicit way of stating that this
        # version has no versions identical to it.
        if not constraints:
            continue

        for pcug_version in ALL_PCUG_VERSIONS:
            if all(c.check(pcug_version) for c in constraints):
                result.setdefault(parent_version, []).append(pcug_version)

    return result


def enumerate_identical_files(
    build_rules: Mapping[str, Mapping[str, str]],
) -> dict[VersionSpec, dict[VersionSpec, Path]]:
    """Get a mapping of individual files derived from another version.

    Most formats have entire versions that are identical to each other, not individual
    files. That's usually only the case when a format has multiple record types and
    only a subset of them changed between versions.

    BQN4 is an example, where the detail record changed multiple times between v5.0 and
    9.1, but the header and trailer records were always the same.
    """
    identical_files = build_rules.get("identical-files")

    if not identical_files:
        return {}

    result = {}
    # TODO
    return result


main()
