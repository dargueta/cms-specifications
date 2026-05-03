# SPDX-License-Identifier: BSD-3-Clause

"""Constant values."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
BUILD_DIR = REPO_ROOT / "build"
SOURCE_DIR = REPO_ROOT / "src"
SCHEMAS_SOURCE_DIR = SOURCE_DIR / "schemas"
FORMATS_BASE_DIR = SCHEMAS_SOURCE_DIR / "file_formats"
COMMON_INCLUDE_DIR = FORMATS_BASE_DIR / "_common"

ALL_SCHEMA_SOURCE_DIRS = [
    p for p in FORMATS_BASE_DIR.iterdir() if p.is_dir() and not p.name.startswith("_")
]

#: Paths to the source directories of each supported PCUG file format, by format name.
#:
#: All subdirectories of `ALL_SCHEMA_SOURCE_DIRS` that are *not* the name of a PCUG file
#: format *must* start with an underscore.
FORMAT_SOURCE_DIRS_BY_NAME = {
    p.name: p for p in ALL_SCHEMA_SOURCE_DIRS if not p.name.startswith("_")
}
