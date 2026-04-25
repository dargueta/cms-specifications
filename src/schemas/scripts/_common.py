from __future__ import annotations

import typing
from collections.abc import Mapping
from collections.abc import MutableSequence
from collections.abc import MutableSet
from collections.abc import Sequence
from collections.abc import Set as AbstractSet
from typing import overload
from typing import TypeVar

import deep_chainmap


if typing.TYPE_CHECKING:
    from typing import Any

T = TypeVar("T")


@overload
def deep_to_dict(item: Mapping[str, T]) -> dict[str, T]: ...


@overload
def deep_to_dict(item: MutableSequence[T]) -> list[T]: ...


@overload
def deep_to_dict(item: Sequence[T]) -> tuple[T, ...]: ...


@overload
def deep_to_dict(item: MutableSet[T]) -> set[T]: ...


@overload
def deep_to_dict(item: AbstractSet[T]) -> frozenset[T]: ...


@overload
def deep_to_dict(item: T) -> T: ...


def deep_to_dict(item: Any) -> Any:
    """Recursively convert all mappings to vanilla `dict`."""
    if isinstance(item, Mapping):
        return {k: deep_to_dict(v) for k, v in item.items()}
    if isinstance(item, MutableSequence):
        return [deep_to_dict(v) for v in item]
    if isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
        return tuple(deep_to_dict(v) for v in item)
    if isinstance(item, MutableSet):
        return {deep_to_dict(v) for v in item}
    if isinstance(item, AbstractSet):
        return frozenset(deep_to_dict(v) for v in item)
    return item


def deep_merge_dicts(*dicts: Mapping[str, Any]) -> dict[str, Any]:
    """Deeply merge keys in dictionaries."""
    return deep_to_dict(deep_chainmap.DeepChainMap(*dicts))
