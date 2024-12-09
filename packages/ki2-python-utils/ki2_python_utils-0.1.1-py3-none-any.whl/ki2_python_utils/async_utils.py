from __future__ import annotations
from typing_extensions import Callable, Awaitable, TypeVar
import asyncio

_T = TypeVar("_T")


async def apply_parallel(data: list[_T], cb: Callable[[_T], Awaitable[None]]):
    return asyncio.gather(*[cb(item) for item in data])


async def run_parallel(*args: Callable[[], Awaitable[None]]):
    return asyncio.gather(*[cb() for cb in args])
