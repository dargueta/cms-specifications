# SPDX-License-Identifier: BSD-3-Clause

"""A Makefile for use with `pymake`.

You must install the pymake command with `pip3 install hayeah-pymake`. Do not install
the myriad of other Python packages that have `pymake` in the name.
"""

from __future__ import annotations

import dataclasses as dc
import fnmatch
import re
from collections.abc import Set as AbstractSet
from pathlib import Path
from typing import NamedTuple

from pymake import sh
from pymake import task
from pymake import tree_digest


HERE = Path(__file__).parent
BUILD_DIR = HERE / "build"
SOURCE_DIR = HERE / "src"
SCHEMAS_SOURCE_DIR = SOURCE_DIR / "schemas"
FORMATS_BASE_DIR = SCHEMAS_SOURCE_DIR / "file_formats"

ALL_PCUG_VERSIONS = [
    # Versions 5 through 14 all have minor versions 0-3, except "7.3" may not exist.
    *((major, minor) for minor in range(4) for major in range(1, 15)),
    # 15 and 16 have minor versions 0-4.
    *((major, minor) for minor in range(5) for major in (15, 16)),
    # 17 and 18 have minor versions 0-9 (I can't find the PDF for 17.0 though.)
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


class FileFormatVersion(NamedTuple):
    major: int
    minor: int
    dependencies: AbstractSet[Path]


@dc.dataclass(frozen=True)
class FileFormatInfo:
    format_name: str
    min_supported_version: tuple[int, int]
    max_explicit_version: tuple[int, int]
    explicit_versions: dict[tuple[int, int], FileFormatVersion]
    common_dependencies: AbstractSet[Path] = dc.field(default_factory=set)


@task(
    inputs=[BUILD_DIR, tree_digest(FORMAT_SOURCE_DIRS_BY_NAME.values()).changed],
    outputs=list(FORMAT_BUILD_DIRS_BY_NAME.values()),
)
def schemas() -> None:
    """Create all schema definitions for PCUG file formats."""
    sh(["pymake", "-C", str(SCHEMAS_SOURCE_DIR), "run", *FORMAT_BUILD_DIRS_BY_NAME])


@task(outputs=[BUILD_DIR])
def create_build_dir() -> None:
    """Create the build directory."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Initialization code to run upon import."""
    for format_name, source_path in FORMAT_SOURCE_DIRS_BY_NAME.items():

        def _build_format() -> None:
            pass

        determine_source_files(source_path)

        task.register(
            _build_format,
            inputs=determine_source_files(source_path),
            outputs=[FORMAT_BUILD_DIRS_BY_NAME[format_name]],
        )


def determine_source_files(format_dir: Path) -> FileFormatInfo:
    """Return a list of all source files for the given file format."""
    templates: set[Path] = set()
    yaml_files: set[Path] = set()
    other_sources: set[Path] = set()

    # All records are defined in YAML files, or templatized YAML files.
    for here, _dirnames, filenames in format_dir.walk():
        templates.update(here / f for f in fnmatch.filter(filenames, "*.liquid"))
        yaml_files.update(here / f for f in fnmatch.filter(filenames, "*.yaml"))

    # Pull in any layout file.
    if (layout := format_dir / "layout.mmd").exists():
        other_sources.append(layout)

    # For most file formats, the layout will be described in the README.md file as a
    # fenced Mermaid diagram. Include the README as a dependency if and only if we
    # detect a Mermaid diagram in there.
    if (
        readme := format_dir / "README.md"
    ).exists() and "```mermaid" in readme.read_text():
        other_sources.append(readme)

    # All template files that render to another file have at least two extensions. For
    # any artifact `X.Y`, the template to render it is named `X.Y.liquid`. We  need to
    # ignore all files named `X.Y` just in case they happen to already exist (e.g. if
    # resuming a previous failed build).
    exclude = {f.with_suffix("") for f in fnmatch.filter(templates, "*.liquid")}
    yaml_files -= exclude
    other_sources -= exclude

    # Get a list of all directories that look like a PCUG version. These are explicitly
    # supported PCUG versions. If this file format supports any other versions, they'll
    # be derived from one of these.
    version_dirs = [p for p in format_dir.iterdir() if re.match(r"\d+\.\d+", p.name)]
    explicit_versions = sorted(tuple(p.stem.split(".")) for p in version_dirs)


main()
