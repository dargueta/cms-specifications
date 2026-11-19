# SPDX-License-Identifier: BSD-3-Clause

"""PCUG version definitions and constraint-matching logic."""

from __future__ import annotations

from typing import NamedTuple
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Self


class VersionSpec(NamedTuple):
    """A version number that can be compared directly.

    Versions that are left as strings can't be reliably compared, because "2.0" would
    sort higher than "10.0".
    """

    major: int
    minor: int

    @classmethod
    def from_string(cls, spec: str) -> Self:
        """Parse a string like `5.0` into a VersionSpec."""
        major, _, minor = spec.strip().partition(".")
        return cls(int(major), int(minor))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"


ALL_PCUG_VERSIONS: list[VersionSpec] = [
    # Versions 5 through 14 all have minor versions 0-3, except "7.3" may not exist.
    *(VersionSpec(major, minor) for major in range(1, 15) for minor in range(4)),
    # 15 and 16 have minor versions 0-4.
    *(VersionSpec(major, minor) for major in (15, 16) for minor in range(5)),
    # 17 and 18 have minor versions 0-9. I can't find the PDF for 17.0, but every other
    # major version has a minor version 0 so I assume it exists.
    *(VersionSpec(major, minor) for major in (17, 18) for minor in range(10)),
    # 19.4 is the most recent version as of August 2026.
    *(VersionSpec(19, minor) for minor in range(5)),
]
ALL_PCUG_VERSIONS.remove(VersionSpec(7, 3))  # I can't find mention of v7.3 anywhere.
