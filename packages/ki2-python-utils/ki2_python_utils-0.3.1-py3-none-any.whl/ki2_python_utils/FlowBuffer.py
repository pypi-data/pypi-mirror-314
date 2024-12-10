from __future__ import annotations
from typing import TYPE_CHECKING, overload
from typing_extensions import TypeVar, Any, SupportsIndex, Generic, Self
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    pass

_T = TypeVar("_T", default=Any)


class AbstractFlowBuffer(ABC, Generic[_T]):
    __data: list[_T]
    __max_length: int

    def __init__(self, max_length: int) -> None:
        self.__max_length = max_length
        self.__data = []

    def __len__(self) -> int:
        return len(self.__data)

    def append(self, object: _T) -> Self:
        if len(self) >= self.__max_length:
            self.__data.pop(0)
        self.__data.append(object)
        return self

    def extend(self, objects: list[_T]) -> Self:
        for object in objects:
            self.append(object)
        return self

    def clear(self) -> Self:
        self.__data.clear()
        return self

    def __iter__(self):
        return iter(self.__data)

    @property
    def raw_data(self) -> list[_T]:
        return self.__data

    @property
    def max_size(self) -> int:
        return self.__max_length

    @property
    def current_size(self) -> int:
        return len(self.__data)

    @property
    def is_full(self):
        return len(self.__data) == self.__max_length

    @property
    def last_item(self) -> _T:
        return self.__data[-1]

    @overload
    def get_raw(self, index: SupportsIndex, /) -> _T: ...

    @overload
    def get_raw(self, index: slice, /) -> list[_T]: ...

    def get_raw(self, key: SupportsIndex | slice, /) -> _T | list[_T]:
        return self.__data[key]

    def get_raw_reverse(self, index: SupportsIndex, /) -> _T:
        return self.__data[-index.__index__() - 1]

    @abstractmethod
    def get(self, index: SupportsIndex, /) -> _T: ...

    def __getitem__(self, index: SupportsIndex, /) -> _T:
        return self.get(index)

    def __bool__(self) -> bool:
        return self.is_full


class ForwardFlowBuffer(AbstractFlowBuffer[_T]):

    def get(self, index: SupportsIndex, /) -> _T:
        return self.get_raw(index)


class ReverseFlowBuffer(AbstractFlowBuffer[_T]):

    def get(self, index: SupportsIndex, /) -> _T:
        return self.get_raw_reverse(index)


FlowBuffer = ReverseFlowBuffer


class IndexedFlowBuffer(AbstractFlowBuffer[_T]):
    __total_len: int

    def __init__(self, max_length: int) -> None:
        super().__init__(max_length)
        self.__total_len = 0

    def append(self, object: _T) -> Self:
        super().append(object)
        self.__total_len += 1
        return self

    def clear(self) -> Self:
        self.__total_len = 0
        return super().clear()

    def get(self, index: SupportsIndex, /) -> _T:
        idx = index.__index__()
        ridx = self.current_size - len(self) + idx
        if ridx < 0 or ridx >= self.current_size:
            raise IndexError("Index out of buffer range")
        return self.get_raw(ridx)

    def __len__(self) -> int:
        return self.__total_len
