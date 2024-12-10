from __future__ import annotations
from typing import TYPE_CHECKING, overload
from typing_extensions import TypeVar, Any

from .exist import exist

if TYPE_CHECKING:
    from .exist import PartialList

_T = TypeVar("_T", default=Any)
_U = TypeVar("_U", default=Any)


def filter_exist_list(items: PartialList[_T]) -> list[_T]:
    return [item for item in items if exist(item)]


def filter_exist_object(item: dict[_T, _U | None]) -> dict[_T, _U]:
    return {k: v for k, v in item.items() if exist(v)}


@overload
def filter_exist(value: PartialList[_T]) -> list[_T]: ...


@overload
def filter_exist(value: dict[_T, _U | None]) -> dict[_T, _U]: ...


@overload
def filter_exist(
    value: PartialList[_U] | dict[_T, _U | None]
) -> list[_U] | dict[_T, _U]: ...


def filter_exist(
    value: PartialList[_U] | dict[_T, _U | None]
) -> list[_U] | dict[_T, _U]:
    if isinstance(value, list):
        return filter_exist_list(value)
    return filter_exist_object(value)


def first_exist(items: PartialList[_T]) -> _T | None:
    for item in items:
        if exist(item):
            return item
    return None


def last_exist(items: PartialList[_T]) -> _T | None:
    for item in reversed(items):
        if exist(item):
            return item
    return None
