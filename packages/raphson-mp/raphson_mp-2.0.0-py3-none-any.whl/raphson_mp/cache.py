"""
Functions related to the cache (cache.db)
"""

import asyncio
import hashlib
import json
import logging
import random
import shutil
import time
from pathlib import Path
from typing import Any

from aiohttp import web

from raphson_mp import db, settings

log = logging.getLogger(__name__)

HOUR = 60 * 60
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY
HALFYEAR = 6 * MONTH
YEAR = 12 * MONTH

# Files larger than this size will be stored in external files. Can be changed without affecting existing cache.
EXTERNAL_SIZE = 10 * 1024 * 1024


def _external_path(name: str) -> Path:
    dir = Path(settings.data_dir, "cache")
    dir.mkdir(exist_ok=True)
    return dir / name


async def store(key: str, data: bytes | Path, duration: int) -> None:
    """
    Args:
        key: Cache key
        data: Data to cache
        duration: Suggested cache duration in seconds. Cache duration is varied by up to 25%, to
                  avoid high load when cache entries all expire at roughly the same time.
    """

    def thread():
        nonlocal duration, data
        with db.cache() as conn:
            # Vary cache duration so cached data doesn't expire all at once
            duration += random.randint(-duration // 4, duration // 4)

            external = False
            if isinstance(data, Path):
                if data.stat().st_size > EXTERNAL_SIZE:
                    file_name = hashlib.blake2s(key.encode()).hexdigest()
                    external_path = _external_path(file_name)
                    log.info("copy %s to external cache file: %s", data.as_posix(), external_path)
                    shutil.copyfile(data, external_path)
                    data = file_name.encode()  # cached data becomes file name
                    external = True
                else:
                    data = data.read_bytes()
            else:
                if len(data) > EXTERNAL_SIZE:
                    file_name = hashlib.blake2s(key.encode()).hexdigest()
                    external_path = _external_path(file_name)
                    log.info("write data to external file: %s", external_path)
                    _external_path(file_name).write_bytes(data)
                    data = file_name.encode()  # cached data becomes file name
                    external = True

            expire_time = int(time.time()) + duration
            conn.execute(
                """
                        INSERT OR REPLACE INTO cache (key, data, expire_time, external)
                        VALUES (?, ?, ?, ?)
                        """,
                (key, data, expire_time, external),
            )

    await asyncio.to_thread(thread)


async def retrieve(key: str, return_expired: bool = True) -> bytes | None:
    """
    Retrieve object from cache
    Args:
        key: Cache key
        partial: Return partial data in the specified range (start, length)
        return_expired: Whether to return the object from cache even when expired, but not cleaned
                        up yet. Should be set to False for short lived cache objects.
    """

    def thread():
        with db.cache(read_only=True) as conn:
            row = conn.execute("SELECT data, expire_time, external FROM cache WHERE key=?", (key,)).fetchone()

            if row is None:
                return None

            data, expire_time, external = row

            if not return_expired and expire_time < time.time():
                return None

            # Allow reading external cache files using standard retrieve(), but
            # since these files may be larger than memory, other methods should
            # be preferred instead.
            if external:
                external_path = _external_path(data.decode())
                log.warning("reading large external file into memory: %s", external_path.as_posix())
                data = external_path.read_bytes()

            return data

    return await asyncio.to_thread(thread)


async def retrieve_response(key: str, content_type: str, return_expired: bool = True) -> web.StreamResponse | None:
    with db.cache(read_only=True) as conn:
        row = conn.execute("SELECT data, expire_time, external FROM cache WHERE key=?", (key,)).fetchone()

        if row is None:
            return None

        data, expire_time, external = row

        if not return_expired and expire_time < time.time():
            return None

        if external:
            log.info("returning FileResponse directly")
            external_path = _external_path(data.decode())
            return web.FileResponse(external_path)

        log.info("not an external file, returning full data in response")
        return web.Response(body=data, content_type=content_type)


async def cleanup() -> None:
    """
    Remove any cache entries that are beyond their expire time.
    """

    # TODO clean up external cache entries
    def thread():
        with db.cache() as conn:
            count = conn.execute(
                "DELETE FROM cache WHERE expire_time < ? AND external = false", (int(time.time()),)
            ).rowcount
            # The number of vacuumed pages is limited to prevent this function
            # from blocking for too long. Max 65536 pages = 256MiB
            conn.execute("PRAGMA incremental_vacuum(65536)")
            log.info("Deleted %s entries from cache", count)

    await asyncio.to_thread(thread)


async def store_json(key: str, data: dict[Any, Any], duration: int) -> None:
    """
    Dump dict as json, encode as utf-8 and then use store()
    """
    await store(key, json.dumps(data).encode(), duration)


async def retrieve_json(key: str, return_expired: bool = True) -> dict[Any, Any] | None:
    """
    Retrieve bytes, if exists decode and return dict
    """
    data = await retrieve(key, return_expired=return_expired)
    if data is None:
        return None

    return json.loads(data.decode())
