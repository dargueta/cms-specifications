# SPDX-License-Identifier: BSD-3-Clause

"""PCUG version definitions and constraint-matching logic."""

from __future__ import annotations

import dataclasses
import operator
import re
from typing import NamedTuple
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Hashable
    from collections.abc import Mapping
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
    *(VersionSpec(major, minor) for minor in range(4) for major in range(1, 15)),
    # 15 and 16 have minor versions 0-4.
    *(VersionSpec(major, minor) for minor in range(5) for major in (15, 16)),
    # 17 and 18 have minor versions 0-9. I can't find the PDF for 17.0, but every other
    # major version has a minor version 0 so I assume it exists.
    *(VersionSpec(major, minor) for minor in range(10) for major in (17, 18)),
    # 19.0 is the most recent version as of 2026-04-20.
    VersionSpec(19, 0),
]
ALL_PCUG_VERSIONS.remove(VersionSpec(7, 3))  # I can't find mention of v7.3 anywhere.


_VERSION_CONSTRAINT_CHECKS: dict[str, Callable[[VersionSpec, VersionSpec], bool]] = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}


@dataclasses.dataclass(frozen=True)
class VersionConstraint:
    """A specification for comparing versions against a single constraint."""

    comparator: Callable[[VersionSpec, VersionSpec], bool]
    version: VersionSpec

    @classmethod
    def from_spec_string(cls, spec: str) -> Self:
        """Parse a specification into a class that can compare versions."""
        spec = spec.strip()

        if spec == "*":
            return cls(lambda _a, _b: True, VersionSpec(0, 0))

        parts = re.match(r"^(?P<constraint>[><=!]+)?\s*(?P<version>\d+\.\d+)$", spec)
        if not parts:
            raise ValueError(f"Invalid constraint definition: {spec!r}")

        comparator = parts["constraint"] or "=="  # ("X.Y" is the same as "==X.Y")
        if comparator not in _VERSION_CONSTRAINT_CHECKS:
            raise ValueError(
                f"Invalid constraint definition {spec!r}: {comparator!r} not one of: "
                + ", ".join(sorted(_VERSION_CONSTRAINT_CHECKS))
            )

        return cls(
            comparator=_VERSION_CONSTRAINT_CHECKS[comparator],
            version=VersionSpec.from_string(parts["version"]),
        )

    def check(self, other_version: VersionSpec) -> bool:
        """Check the given version against this constraint."""
        return self.comparator(other_version, self.version)


def enumerate_versions_matching_constraints[T: Hashable](
    rules: Mapping[T, str],
) -> dict[T, list[VersionSpec]]:
    """Map keys to lists of PCUG versions matching the version constraint values.

    The returned dictionary is guaranteed to have all the same keys as ``rules``. This
    function doesn't examine the keys either, so the keys can be of any hashable type.
    """
    result = {}
    for key, child_version_spec in rules.items():
        constraints = [
            VersionConstraint.from_spec_string(s) for s in child_version_spec.split(",")
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
