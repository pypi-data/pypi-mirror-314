import asyncio
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict, cast

from yt_dlp import DownloadError, YoutubeDL  # pyright: ignore[reportMissingTypeStubs]

from raphson_mp import db, music, scanner, settings

log = logging.getLogger(__name__)


if settings.offline_mode:
    # Module must not be imported to ensure no data is ever downloaded in offline mode.
    raise RuntimeError("Cannot use downloader in offline mode")


OPTIONS = {
    "cachedir": "/tmp/yt-dlp-cache",
    "paths": {"temp": "/tmp/yt-dlp-temp"},
    "color": {"stdout": "never", "stderr": "never"},
}


@dataclass
class YtDone:
    status_code: int


class YtError(Exception):
    status_code: int

    def __init__(self, status_code: int):
        super().__init__()
        self.status_code = status_code


class YtdlLogger:
    loop: asyncio.AbstractEventLoop
    queue: asyncio.Queue[str | YtDone]  # contains log strings or YtDone object to indicate yt-dlp has finished

    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.queue = asyncio.Queue()

    def debug(self, msg: str) -> None:
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)

    def info(self, msg: str) -> None:
        if self.loop and self.queue:
            asyncio.run_coroutine_threadsafe(self.queue.put(msg + "\n"), self.loop)
        log.info(msg)

    def warning(self, msg: str) -> None:
        if self.loop and self.queue:
            asyncio.run_coroutine_threadsafe(self.queue.put(msg + "\n"), self.loop)
        log.warning(msg)

    def error(self, msg: str) -> None:
        if self.loop and self.queue:
            asyncio.run_coroutine_threadsafe(self.queue.put(msg + "\n"), self.loop)
        log.error(msg)

    def done(self, status_code: int) -> None:
        if self.loop and self.queue:
            asyncio.run_coroutine_threadsafe(self.queue.put(YtDone(status_code)), self.loop)


async def download(dest: music.Playlist | Path, url: str) -> AsyncIterator[bytes]:
    dest_path = dest if isinstance(dest, Path) else dest.path
    logger = YtdlLogger()
    yt_opts = {
        **OPTIONS,
        "format": "bestaudio",
        "noplaylist": True,
        "postprocessors": [{"key": "FFmpegVideoRemuxer", "preferedformat": "webm>ogg/mp3>mp3/mka"}],
        "logger": logger,
        "outtmpl": dest_path.as_posix() + "/%(uploader)s - %(title)s.%(ext)s",
    }

    def download_thread():
        with YoutubeDL(yt_opts) as ytdl:
            try:
                status_code = ytdl.download([url])  # pyright: ignore[reportUnknownMemberType]
                logger.done(status_code)
            except DownloadError:
                logger.done(1)

    asyncio.create_task(asyncio.to_thread(download_thread))

    while not isinstance(log := await logger.queue.get(), YtDone):
        yield log.encode()
        logger.queue.task_done()

    if log.status_code == 0:
        yield b"Done\n"
    else:
        yield f"Failed with status code {log.status_code}".encode()

    if isinstance(dest, music.Playlist):
        yield "Scanning playlist\n".encode()
        with db.connect() as writable_conn:
            await scanner.scan_tracks(writable_conn, dest.name)
        yield "Done".encode()


class SearchResult(TypedDict):
    url: str
    title: str
    channel_name: str
    channel_subscribers: int
    view_count: int
    duration: int
    duration_string: str
    upload_date: str


def search(search_query: str, logger: YtdlLogger, search_type: str = "ytsearch") -> list[SearchResult]:
    with YoutubeDL({**OPTIONS, "default_search": search_type, "logger": logger}) as ytdl:
        info: Any = ytdl.extract_info(search_query, download=False)  # pyright: ignore[reportUnknownMemberType]
        results: list[SearchResult] = []
        for entry in info["entries"]:
            result: SearchResult
            result = {
                "url": cast(str, entry["original_url"]),
                "title": cast(str, entry["title"]),
                "channel_name": cast(str, entry["uploader"]),
                "channel_subscribers": cast(int, entry["channel_follower_count"]),
                "view_count": cast(int, entry["view_count"]),
                "duration": cast(int, entry["duration"]),
                "duration_string": cast(str, entry["duration_string"]),
                "upload_date": cast(str, entry["upload_date"]),
            }
            results.append(result)

        return results
