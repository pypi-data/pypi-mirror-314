from __future__ import annotations
from typing_extensions import (
    TypeVar,
    ParamSpec,
    Generic,
    Any,
    Callable,
    Awaitable,
    Literal,
    TypeAlias,
)
from abc import ABC, abstractmethod


from .async_utils import apply_parallel

_T = TypeVar("_T", default=Any)
_P = ParamSpec("_P")


class UniqueList(list[_T]):
    def __init__(self, iterable: list[_T] | None = None) -> None:
        super().__init__()
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def append(self, object: _T) -> None:
        if object not in self:
            return super().append(object)


CallbackType = Callable[_P, None]
AsyncCallbackType = Callable[_P, Awaitable[None]]


class AbstractCallbackable(ABC, Generic[_P]):

    @abstractmethod
    def call(self, *args: _P.args, **kwargs: _P.kwargs) -> None: ...

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        self.call(*args, **kwargs)


class MultipleCallbackList(list[CallbackType[_P]]):
    def __init__(self) -> None:
        super().__init__()

    def call(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        for cb in self:
            cb(*args, **kwargs)

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        self.call(*args, **kwargs)


class UniqueCallbackList(UniqueList[CallbackType[_P]], MultipleCallbackList[_P]):
    pass


AsyncCallbackMode: TypeAlias = Literal["sequential", "parallel"]


class AsyncMultipleCallbackList(list[AsyncCallbackType[_P]]):
    __call_mode: AsyncCallbackMode

    def __init__(self, mode: AsyncCallbackMode = "sequential") -> None:
        super().__init__()
        self.__call_mode = mode

    @property
    def default_call_mode(self) -> AsyncCallbackMode:
        return self.__call_mode

    @default_call_mode.setter
    def default_call_mode(self, mode: AsyncCallbackMode) -> None:
        self.__call_mode = mode

    async def sequential_call(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        for cb in self:
            await cb(*args, **kwargs)

    async def pararallel_call(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        def handle_cb(cb: AsyncCallbackType[_P]) -> Awaitable[None]:
            return cb(*args, **kwargs)

        await apply_parallel(self, handle_cb)

    async def call(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        if self.__call_mode == "parallel":
            await self.pararallel_call(*args, **kwargs)
        else:
            await self.sequential_call(*args, **kwargs)

    async def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        await self.call(*args, **kwargs)


class AsyncUniqueCallbackList(
    UniqueList[AsyncCallbackType[_P]], AsyncMultipleCallbackList[_P]
):
    pass


CallbackList = UniqueCallbackList
AsyncCallbackList = AsyncUniqueCallbackList
