import asyncio
import difflib
import logging
import time
import urllib.parse
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from io import BytesIO, IOBase
from queue import Queue
from typing import Any, override

from aiohttp import web

_LOGGER = logging.getLogger(__name__)


def check_filename(name: str) -> None:
    """
    Ensure file name is valid, if not raise ValueError
    """
    if "/" in name or "\\" in name or name == "." or name == ".." or name == "...":
        raise ValueError("illegal name")


MOBILE_FLAGS = ["Android", "iPhone"]


def is_mobile(request: web.Request) -> bool:
    """
    Checks whether User-Agent looks like a mobile device (Android or iOS)
    """
    if "User-Agent" in request.headers:
        user_agent = request.headers["User-Agent"]
        for flag in MOBILE_FLAGS:
            if flag in user_agent:
                return True
    return False


class QueueIO(IOBase):
    queue: Queue[bytes | None]

    def __init__(self) -> None:
        self.queue = Queue(maxsize=32)

    @override
    def close(self):
        super().close()
        self.queue.put(None)

    @override
    def readable(self):
        return False

    @override
    def seekable(self):
        return False

    @override
    def write(self, data: bytes):
        self.queue.put(data)
        return len(data)

    def iterator(self) -> Iterator[bytes]:
        while True:
            data = self.queue.get(True)
            if data is None:
                return

            yield data


class AsyncQueueIO(IOBase):
    queue: asyncio.Queue[bytes | None]
    loop: asyncio.AbstractEventLoop
    buf: BytesIO

    def __init__(self) -> None:
        self.queue = asyncio.Queue(maxsize=32)
        self.loop = asyncio.get_running_loop()
        self.buf = BytesIO()

    @override
    def close(self):
        super().close()

        async def finish():
            pos = self.buf.tell()
            self.buf.seek(0)
            remaining_data = self.buf.read(pos)
            await self.queue.put(remaining_data)
            await self.queue.put(None)

        asyncio.run_coroutine_threadsafe(finish(), self.loop)

    @override
    def readable(self):
        return False

    @override
    def seekable(self):
        return False

    @override
    def write(self, data: bytes):
        written = self.buf.write(data)

        # thread-safe writing to the queue is an expensive operation
        # buffer writes locally up to 1MB
        pos = self.buf.tell()
        if pos > 1024 * 1024:
            self.buf.seek(0)
            bulk_data = self.buf.read(pos)
            self.buf.seek(0)
            asyncio.run_coroutine_threadsafe(self.queue.put(bulk_data), self.loop)

        return written

    async def iterator(self) -> AsyncIterator[bytes]:
        while True:
            data = await self.queue.get()
            if data is None:
                return

            yield data


def str_match(a: str, b: str) -> bool:
    if a == b:
        return True

    a = a.lower()
    b = b.lower()

    if a == b:
        return True

    diff = difflib.SequenceMatcher(None, a, b)
    # real_quick_ratio() provides an upper bound on quick_ratio(), which provides an upper bound on ratio()
    # ratio() is expensive so we must avoid it when possible
    return diff.real_quick_ratio() > 0.8 and diff.quick_ratio() > 0.8 and diff.ratio() > 0.8


def substr_keyword(text: str, start: str, end: str):
    start_i = text.index(start) + len(start)
    end_i = start_i + text[start_i:].index(end)
    return text[start_i:end_i]


def log_duration(func: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
    async def wrapper(*args: Any, **kwargs: Any):
        start_time = time.time()
        await func(*args, **kwargs)
        end_time = time.time()
        _LOGGER.info(f"{func.   __name__} took {end_time-start_time:.1f} seconds")

    return wrapper


def urlencode(text: str) -> str:
    return urllib.parse.quote(text, safe='')
