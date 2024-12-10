from __future__ import annotations
from typing_extensions import TypeVar, TypeIs, TypeAlias

_T = TypeVar("_T")


def exist(value: _T | None) -> TypeIs[_T]:
    return value is not None


PartialList: TypeAlias = list[_T] | list[None] | list[_T | None]


def count_exist(values: PartialList[_T]) -> int:
    return sum(1 for value in values if exist(value))


def count_none(values: PartialList[_T]) -> int:
    return sum(1 for value in values if not exist(value))


def exist_all(values: PartialList[_T]) -> TypeIs[list[_T]]:
    if len(values) == 0:
        return True
    return count_exist(values) == len(values)


def exist_some(values: PartialList[_T]) -> bool:
    if len(values) == 0:
        return True
    return count_exist(values) > 0
