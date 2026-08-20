# SPDX-License-Identifier: BSD-3-Clause

"""Constant values."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
DEFAULT_BUILD_DIR = REPO_ROOT / "build"
SOURCE_DIR = REPO_ROOT / "src"
SCHEMAS_SOURCE_DIR = SOURCE_DIR / "schemas"
FORMATS_BASE_DIR = SCHEMAS_SOURCE_DIR / "file_formats"
COMMON_INCLUDE_DIR = FORMATS_BASE_DIR / "_common"

#: Paths to all directories defining schemas for a file type.
#:
#: These are detected by searching for a file named "build_rules.yaml" inside the
#: directory.
ALL_SCHEMA_SOURCE_DIRS = [p.parent for p in FORMATS_BASE_DIR.glob("*/build_rules.yaml")]

#: Paths to the source directories of each supported PCUG file format, by format name.
FORMAT_SOURCE_DIRS_BY_NAME = {p.name: p for p in ALL_SCHEMA_SOURCE_DIRS}
