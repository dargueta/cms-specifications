# SPDX-License-Identifier: BSD-3-Clause

"""File operations used as doit task actions: link, copy, touch, cleanup."""

from __future__ import annotations

import contextlib
import pathlib
import shutil
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterable


try:
    _SUPPRESS_PATHLIB_EXCEPTIONS = pathlib.UnsupportedOperation, NotImplementedError
except AttributeError:  # pragma: no cover (>=py313)
    _SUPPRESS_PATHLIB_EXCEPTIONS = (NotImplementedError,)


def link_or_copy(parent: Path, children: Iterable[Path]) -> None:
    """Link one or more "children" to point to a "parent", or copy if not possible.

    This works with both files and directories.
    """
    for child in children:
        if parent.is_dir():
            _link_or_copy_directory(child, parent)
        else:
            _link_or_copy_file(child, parent)


def _link_or_copy_directory(link: Path, existing: Path) -> None:
    with contextlib.suppress(*_SUPPRESS_PATHLIB_EXCEPTIONS):
        link.symlink_to(existing)
        return
    shutil.copytree(existing, link)


def _link_or_copy_file(link: Path, existing: Path) -> None:
    with contextlib.suppress(*_SUPPRESS_PATHLIB_EXCEPTIONS):
        link.hardlink_to(existing)
        return
    with contextlib.suppress(*_SUPPRESS_PATHLIB_EXCEPTIONS):
        link.symlink_to(existing)
        return
    shutil.copyfile(existing, link)


def touch_files(paths: Iterable[Path]) -> None:
    """Update the "last modified" timestamp to the current date and time."""
    for path in paths:
        path.touch()


def cleanup_intermediate(path: Path) -> None:
    """Delete a file if it exists."""
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)
