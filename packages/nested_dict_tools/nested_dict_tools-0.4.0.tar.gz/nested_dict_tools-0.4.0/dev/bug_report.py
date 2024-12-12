"""."""

from collections.abc import Iterator, Mapping
from typing import Any, cast, overload, reveal_type

# Recursive types:
type NestedMapping[K, V] = Mapping[K, NestedMappingNode[K, V]]
type NestedMappingNode[K, V] = V | NestedMapping[K, V]

type NestedDict[K, V] = dict[K, NestedDictNode[K, V]]
type NestedDictNode[K, V] = V | NestedDict[K, V]


# Full error message, when this is the only overload:
# Argument of type "dict[str, dict[str, dict[str, int]]]" cannot be assigned to parameter "nested_dict" of type "NestedDict[K@iter_leaf_containers, V@iter_leaf_containers]" in function "iter_leaf_containers"
# "dict[str, dict[str, dict[str, int]]]" is not assignable to "dict[str, NestedDictNode[str, dict[str, dict[str, int]]]]"
# Type parameter "_VT@dict" is invariant, but "dict[str, dict[str, int]]" is not the same as "NestedDictNode[str, dict[str, dict[str, int]]]"
# Consider switching from "dict" to "Mapping" which is covariant in the value type
@overload
def iter_leaf_containers[K, V](
    nested_dict: NestedDict[K, V],
) -> Iterator[tuple[dict[K, V], K]]: ...


# Overload 2 for "iter_leaf_containers" will never be used because its parameters overlap overload 1
@overload
def iter_leaf_containers[K](
    nested_dict: NestedDict[K, Any],
) -> Iterator[tuple[dict[K, Any], K]]: ...


# Somewhat unexpected: no parameter overlap is detected with either overload 1
@overload
def iter_leaf_containers[V](
    nested_dict: NestedDict[Any, V],
) -> Iterator[tuple[dict[Any, V], Any]]: ...

# As expected: Overload 4 for "iter_leaf_containers" will never be used because its parameters overlap overload 3
@overload
def iter_leaf_containers(
    nested_dict: NestedDict[Any, Any],
) -> Iterator[tuple[dict[Any, Any], Any]]: ...


@overload
def iter_leaf_containers[K, V](
    nested_dict: NestedMapping[K, V],
) -> Iterator[tuple[Mapping[K, V], K]]: ...


def iter_leaf_containers[K, V](
    nested_dict: NestedMapping[K, V],
) -> Iterator[tuple[Mapping[K, V], K]]:
    for key, value in nested_dict.items():
        if isinstance(value, Mapping):
            yield from iter_leaf_containers(cast(NestedMapping[K, V], value))
        else:
            yield cast(Mapping[K, V], nested_dict), key


nested = {"a": {"b": 42}}

# Despite the error message, compatibility is detected with the overload 2
leaf_refs = iter_leaf_containers(nested)
reveal_type(leaf_refs)  # Iterator[tuple[dict[str, Any], str]]
