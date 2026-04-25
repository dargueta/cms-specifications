# SPDX-License-Identifier: BSD-3-Clause

"""A Makefile for use with `pymake`.

You must install the pymake command with `pip3 install hayeah-pymake`. Do not install
the myriad of other Python packages that have `pymake` in the name.
"""

from __future__ import annotations

import configparser
import contextlib
import dataclasses
import functools
import logging
import operator
import pathlib
import re
import shutil
import typing
from pathlib import Path
from typing import ClassVar
from typing import NamedTuple

from pymake import sh
from pymake import task


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Container
    from collections.abc import Iterable
    from collections.abc import Mapping
    from typing import Self


LOG = logging.getLogger(__name__)

HERE = Path(__file__).parent
BUILD_DIR = HERE / "build"
SOURCE_DIR = HERE / "src"
SCHEMAS_SOURCE_DIR = SOURCE_DIR / "schemas"
FORMATS_BASE_DIR = SCHEMAS_SOURCE_DIR / "file_formats"


class VersionSpec(NamedTuple):
    major: int
    minor: int

    @classmethod
    def from_string(cls, spec: str) -> Self:
        major, _, minor = spec.partition(".")
        return cls(int(major), int(minor))


ALL_PCUG_VERSIONS: list[VersionSpec] = [
    # Versions 5 through 14 all have minor versions 0-3, except "7.3" may not exist.
    *(VersionSpec(major, minor) for minor in range(4) for major in range(1, 15)),
    # 15 and 16 have minor versions 0-4.
    *(VersionSpec(major, minor) for minor in range(5) for major in (15, 16)),
    # 17 and 18 have minor versions 0-9.I can't find the PDF for 17.0, but every other
    # major version has a minor version 0 so I assume it exists.
    *(VersionSpec(major, minor) for minor in range(10) for major in (17, 18)),
    # 19.0 is the most recent version as of 2026-04-20.
    VersionSpec(19, 0),
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

    comparator: Callable[[VersionSpec, VersionSpec], bool]
    version: VersionSpec

    CHECKS: ClassVar[dict[str, Callable[[VersionSpec, VersionSpec], bool]]] = {
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
        spec = spec.strip()

        if spec == "*":
            return cls(lambda _a, _b: True, VersionSpec(0, 0))

        parts = re.match(r"^(?P<constraint>[><=!]+)?\s*(?P<version>\d+\.\d+)$", spec)
        if not parts:
            raise ValueError(f"Invalid constraint definition: {spec!r}")

        comparator = parts["constraint"]
        if comparator not in cls.CHECKS:
            raise ValueError(
                f"Invalid constraint definition {spec!r}: {comparator!r} not one of: "
                + ", ".join(sorted(cls.CHECKS))
            )

        return cls(
            comparator=cls.CHECKS[comparator],
            version=VersionSpec.from_string(parts["version"]),
        )

    def check(self, version: tuple[int, int]) -> bool:
        """Check the given version against this constraint."""
        return self.comparator(self.version, version)


@dataclasses.dataclass
class FileDependency:
    file_path: Path
    source_version: VersionSpec | None = None
    target_versions: Container[VersionSpec] = ()


def _generic_symlink_task(parent: Path, children: Iterable[Path]) -> None:
    for child in children:
        if parent.is_dir():
            _link_or_copy_directory(child, parent)
        else:
            _link_or_copy_file(child, parent)


def _link_or_copy_directory(link: Path, existing: Path) -> None:
    """Try linking a directory, falling back to copying if that doesn't work."""
    # Hard links to a directory generally aren't allowed, so we won't bother trying. Go
    # for a symlink first instead.
    with contextlib.suppress(pathlib.UnsupportedOperation, NotImplementedError):
        link.symlink_to(existing)
        return

    # Symlink didn't work, we have to copy.
    shutil.copytree(existing, link)


def _link_or_copy_file(link: Path, existing: Path) -> None:
    """Try linking a file, falling back to copying if that doesn't work."""
    # Try a hard link first.
    with contextlib.suppress(pathlib.UnsupportedOperation, NotImplementedError):
        link.hardlink_to(existing)
        return

    # Hard links not supported, try symlinking.
    with contextlib.suppress(pathlib.UnsupportedOperation, NotImplementedError):
        link.symlink_to(existing)
        return

    shutil.copyfile(existing, link)


def generate_tasks_for_format(format_name: str, source_path: Path) -> None:
    """Register tasks to generate all output files for the given format."""
    # A file named build_rules.ini will tell us how to generate versions.
    build_rules_file = source_path / "build_rules.ini"
    if not build_rules_file.exists():
        LOG.warning(
            "Format %r doesn't define required build rules file %r. Ignoring for now,"
            " but this may become an error in the future.",
            format_name,
            str(source_path),
        )
        return

    build_rules = configparser.ConfigParser().read(build_rules_file)

    target_root = BUILD_DIR / format_name
    parent_targets = []

    # Create tasks that will symlink the build directories of identical versions to a
    # concrete parent version. This lets us reproduce the output of entire versions with
    # one command, rather than having to symlink or copy each file separately.
    identical_versions = enumerate_identical_versions(build_rules)
    for parent_version, children in identical_versions.items():
        parent_output_dir = Path(target_root / str(parent_version))
        parent_targets.append(parent_output_dir)
        child_output_dirs = [Path(target_root / str(v)) for v in children]

        task.register(
            functools.partial(
                _generic_symlink_task,
                parent=parent_output_dir,
                children=child_output_dirs,
            ),
            name=f"{format_name}_{parent_version.major}_{parent_version.minor}",
            inputs=[parent_output_dir],
            outputs=child_output_dirs,
        )

    # identical_files = enumerate_identical_files(build_rules)


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

    result = enumerate_versions_matching_constraints(identical_versions)
    return {VersionSpec.from_string(k): v for k, v in result.items()}


def enumerate_identical_files(
    build_rules: Mapping[str, Mapping[str, str]],
) -> list[FileDependency]:
    """Get a mapping of individual files derived from another version.

    Most formats have entire versions that are identical to each other, not individual
    files. Usually, this only happens when a format has multiple record types, and only
    a subset of them change between versions.

    BQN4 is an example, where the detail record changed multiple times between v5.0 and
    v9.1, but the header and trailer records were always the same.
    """
    identical_files = build_rules.get("identical-files")

    if not identical_files:
        return []

    matching_versions = enumerate_versions_matching_constraints(identical_files)

    result = []
    for raw_path, dependent_versions in matching_versions:
        # If the file path starts with what appears to be a version number, record that
        # as the "source version".
        match = re.match(r"^(\d+\.\d+)")
        source_version = VersionSpec.from_string(match[1]) if match else None

        result.append(
            FileDependency(
                file_path=Path(raw_path),
                source_version=source_version,
                target_versions=dependent_versions,
            )
        )
    return result


def enumerate_versions_matching_constraints(
    rules: Mapping[str, str],
) -> dict[str, list[VersionSpec]]:
    """Map keys to lists of PCUG versions matching the version constraint values.

    .. python::
        >>> enumerate_versions_matching_constraints({"abc": ">=5.0, <6.2, !=5.3"})
        ... {
        ...     "abc": [
        ...         VersionSpec(5, 0),
        ...         VersionSpec(5, 1),
        ...         VersionSpec(5, 2),
        ...         VersionSpec(6, 0),
        ...         VersionSpec(6, 1),
        ...     ]
        ... }
    """
    result = {}
    for key, child_version_spec in rules.items():
        constraints = [
            VersionConstraint.from_spec_string(s)
            for s in child_version_spec.split(",", 1)
        ]

        if not constraints:
            raise ValueError(
                f"Version constraint lists cannot be empty. Offender: {key!r}"
            )

        result[key] = [
            pcug_version
            for pcug_version in ALL_PCUG_VERSIONS
            if all(c.check(pcug_version) for c in constraints)
        ]

    return result


main()
