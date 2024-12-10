from __future__ import annotations
from typing_extensions import Callable, Awaitable, TypeVar
import asyncio

_T = TypeVar("_T")
_U = TypeVar("_U", default=None)


async def apply_parallel(cb: Callable[[_T], Awaitable[_U]], data: list[_T]):
    return await asyncio.gather(*[cb(item) for item in data])


async def run_parallel(*args: Callable[[], Awaitable[None]]):
    return await asyncio.gather(*[cb() for cb in args])
