# SPDX-License-Identifier: BSD-3-Clause

"""A Makefile for use with `pymake`.

You must install the pymake command with `pip3 install hayeah-pymake`. Do not install
the myriad of other Python packages that have `pymake` in the name.
"""

from __future__ import annotations

import configparser
from pathlib import Path

from pymake import sh
from pymake import task


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


def generate_tasks_for_format(format_name: str, source_path: Path) -> None:
    """Register tasks to generate all output files for the given format."""
    # A file named build_rules.ini will tell us how to generate versions.
    build_rules_file = source_path / "build_rules.ini"
    if not build_rules_file.exists():
        return

    parser = configparser.ConfigParser()
    build_rules = parser.read(build_rules_file)

    # In [generated-versions], all keys indicate a concrete defined version, and all
    # values are versions generated from this concrete version. For example, if we have
    # "5.0: >=5.1, <=8.0" that means that version 5.0 must exist in the source tree, and
    # all PCUG versions from 5.1 through 8.0 are identical to it.
    for parent_version, child_version_spec in build_rules["generated-versions"].items():
        child_version_rules = [
            p.replace(" ", "") for p in child_version_spec.split(",")
        ]


main()
