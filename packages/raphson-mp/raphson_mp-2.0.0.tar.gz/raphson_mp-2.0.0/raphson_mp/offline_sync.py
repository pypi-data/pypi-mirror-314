import asyncio
from collections.abc import AsyncIterator
import json
import logging
import random
import time
from abc import ABC, abstractmethod
from sqlite3 import Connection
from threading import Event, Thread
from typing import override

from aiohttp import web
from raphson_music_client import RaphsonMusicClient
from raphson_music_client.track import DownloadableTrack

from raphson_mp import db, settings

log = logging.getLogger(__name__)


class SyncProgress(ABC):
    @abstractmethod
    def task_start(self, task: str):
        pass

    @abstractmethod
    def task_done(self, task: str):
        pass

    @abstractmethod
    def all_done(self):
        pass


class CommandLineSyncProgress(SyncProgress):
    start_time: dict[str, int] = {}

    @override
    def task_start(self, task: str):
        self.start_time[task] = time.time_ns()
        log.info("start: %s", task)

    @override
    def task_done(self, task: str):
        duration = (time.time_ns() - self.start_time[task]) // 1_000_000
        del self.start_time[task]
        log.info("done: %s (%sms)", task, duration)

    @override
    def all_done(self):
        pass


class FlaskResponseProgress(SyncProgress):
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop: asyncio.AbstractEventLoop

    def __init__(self):
        self.loop = asyncio.get_running_loop()

    @override
    def task_start(self, task: str):
        asyncio.run_coroutine_threadsafe(self.queue.put(json.dumps({"task": task, "done": False}) + "\n"), self.loop)

    @override
    def task_done(self, task: str):
        asyncio.run_coroutine_threadsafe(self.queue.put(json.dumps({"task": task, "done": True}) + "\n"), self.loop)

    @override
    def all_done(self):
        asyncio.run_coroutine_threadsafe(self.queue.put(None), self.loop)

    def response(self) -> web.Response:
        async def generator() -> AsyncIterator[bytes]:
            while entry := await self.queue.get():
                if entry:
                    yield entry.encode()
                else:
                    break

        return web.Response(body=generator(), content_type="text/plain")


class SyncError(Exception):
    pass


class SyncStop(Exception):
    pass


class OfflineSync(Thread):
    progress: SyncProgress
    client: RaphsonMusicClient
    stop_event: Event
    force_resync: float

    def __init__(self, progress: SyncProgress, force_resync: float):
        super().__init__(daemon=True)
        self.progress = progress
        self.client = RaphsonMusicClient()
        self.stop_event = Event()
        self.force_resync = force_resync

    async def setup(self, db_offline: Connection):
        row = db_offline.execute("SELECT base_url, token FROM settings").fetchone()
        if row:
            base_url, token = row
        else:
            # log.info('Server is not configured')
            # base_url = input('Enter server URL (https://example.com): ')
            # token = input(f'Enter token (visit {base_url}/token to get a token): ')
            # self.db_offline.execute('INSERT INTO settings (base_url, token) VALUES (?, ?)', (base_url, token))
            raise SyncError("Sync server not configured")

        await self.client.setup(base_url=base_url, user_agent=settings.user_agent, token=token)

    async def _download_track_content(self, db_offline: Connection, track: DownloadableTrack) -> None:
        """
        Download audio, album cover and lyrics for a track and store in the 'content' database table.
        """
        download = await track.download()

        db_offline.execute(
            """
            INSERT INTO content (path, music_data, cover_data, lyrics_json)
            VALUES(:path, :music_data, :cover_data, :lyrics_json)
            ON CONFLICT (path) DO UPDATE SET
                music_data = :music_data, cover_data = :cover_data, lyrics_json = :lyrics_json
            """,
            {
                "path": track.path,
                "music_data": download.audio,
                "cover_data": download.image,
                "lyrics_json": download.lyrics_json,
            },
        )

    async def _update_track(self, db_offline: Connection, db_music: Connection, track: DownloadableTrack) -> None:
        self.progress.task_start("update " + track.path)

        await self._download_track_content(db_offline, track)

        db_music.execute(
            "UPDATE track SET duration=?, title=?, album=?, album_artist=?, year=?, mtime=? WHERE path=?",
            (
                track.duration,
                track.title,
                track.album,
                track.album_artist,
                track.year,
                track.mtime,
                track.path,
            ),
        )
        db_music.execute("DELETE FROM track_artist WHERE track=?", (track.path,))
        db_music.executemany(
            "INSERT INTO track_artist (track, artist) VALUES (?, ?)",
            [(track.path, artist) for artist in track.artists],
        )

        self.progress.task_done("update " + track.path)

    async def _insert_track(
        self,
        db_offline: Connection,
        db_music: Connection,
        playlist: str,
        track: DownloadableTrack,
    ) -> None:
        self.progress.task_start("download " + track.path)

        await self._download_track_content(db_offline, track)

        db_music.execute(
            """
            INSERT INTO track (path, playlist, duration, title, album,
                               album_artist, year, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                track.path,
                playlist,
                track.duration,
                track.title,
                track.album,
                track.album_artist,
                track.year,
                track.mtime,
            ),
        )
        db_music.executemany(
            "INSERT INTO track_artist (track, artist) VALUES (?, ?)",
            [(track.path, artist) for artist in track.artists],
        )

        self.progress.task_done("download " + track.path)

    def _prune_tracks(self, db_offline: Connection, db_music: Connection, track_paths: set[str]):
        rows = db_music.execute("SELECT path FROM track").fetchall()
        for (path,) in rows:
            if path not in track_paths:
                log.info("Delete: %s", path)
                db_offline.execute("DELETE FROM content WHERE path=?", (path,))
                db_music.execute("DELETE FROM track WHERE path=?", (path,))

    def _prune_playlists(self, db_music: Connection):
        # Remove empty playlists
        rows = db_music.execute(
            """
            SELECT path
            FROM playlist
            WHERE (SELECT COUNT(*) FROM track WHERE track.playlist=playlist.path) = 0
            """
        ).fetchall()

        for (name,) in rows:
            log.info("Delete empty playlist: %s", name)
            db_music.execute("DELETE FROM playlist WHERE path=?", (name,))

    async def _sync_tracks_for_playlist(
        self,
        db_offline: Connection,
        db_music: Connection,
        playlist: str,
        dislikes: set[str],
        all_track_paths: set[str],
    ) -> None:
        log.info("Syncing playlist: %s", playlist)

        db_music.execute("INSERT INTO playlist VALUES (?) ON CONFLICT (path) DO NOTHING", (playlist,))

        tracks = await self.client.list_tracks(playlist)

        for track in tracks:
            if track.path in dislikes:
                continue

            all_track_paths.add(track.path)

            row = db_music.execute("SELECT mtime FROM track WHERE path=?", (track.path,)).fetchone()
            if row:
                (mtime,) = row
                if mtime != track.mtime:
                    log.info("Out of date: %s", track.path)
                    await self._update_track(db_offline, db_music, track)
                elif self.force_resync > 0 and random.random() < self.force_resync:
                    log.info("Force resync: %s", track.path)
                    await self._update_track(db_offline, db_music, track)
            else:
                log.info("Missing: %s", track.path)
                await self._insert_track(db_offline, db_music, playlist, track)

            db_offline.commit()
            db_music.commit()

            if self.stop_event.is_set():
                raise SyncStop()

    async def sync_tracks(self, db_offline: Connection, db_music: Connection) -> None:
        """
        Download added or modified tracks from the server, and delete local tracks that were deleted on the server
        """
        # TODO don't keep writable database connection open for a long time, other tasks may be blocked
        result = db_offline.execute("SELECT name FROM playlists")
        enabled_playlists: list[str] = [row[0] for row in result]

        if len(enabled_playlists) == 0:
            # log.info('No playlists selected. Fetching favorite playlists...')
            self.progress.task_start("fetching favorite playlists")
            playlists = await self.client.playlists()
            enabled_playlists = [playlist.name for playlist in playlists if playlist.favorite]
            self.progress.task_done("fetching favorite playlists")

        self.progress.task_start("fetching disliked tracks")
        dislikes: set[str] = set()  # TODO implement retrieving dislikes
        # dislikes = set(self.request_get('/dislikes/json').json()['tracks'])
        self.progress.task_done("fetching disliked tracks")

        all_track_paths: set[str] = set()

        for playlist in enabled_playlists:
            await self._sync_tracks_for_playlist(db_offline, db_music, playlist, dislikes, all_track_paths)

        self._prune_tracks(db_offline, db_music, all_track_paths)
        self._prune_playlists(db_music)

    async def sync_history(self, db_offline: Connection):
        """
        Send local playback history to server
        """
        rows = db_offline.execute("SELECT rowid, timestamp, track FROM history ORDER BY timestamp ASC")
        for rowid, timestamp, track in rows:
            self.progress.task_start("submit played " + track)
            await self.client.submit_played(track, timestamp)
            db_offline.execute("DELETE FROM history WHERE rowid=?", (rowid,))
            db_offline.commit()
            self.progress.task_done("submit played " + track)

    async def do_sync(self) -> None:
        try:
            with db.offline() as db_offline:
                await self.setup(db_offline)
                log.info("Sync history")
                await self.sync_history(db_offline)
                with db.connect() as db_music:
                    log.info("Sync tracks")
                    await self.sync_tracks(db_offline, db_music)
                self.progress.task_start("cleanup")
                db_offline.execute("PRAGMA incremental_vacuum")
                self.progress.task_done("cleanup")
        except SyncStop:
            self.progress.task_done("stop")
            pass
        finally:
            if self.client:
                await self.client.close()

    @override
    def run(self):
        asyncio.run(self.do_sync())

        self.progress.all_done()

    def stop(self) -> None:
        if not self.stop_event.is_set():
            self.progress.task_start("stop")
            self.stop_event.set()


def do_sync(force_resync: float = 0):
    if not settings.offline_mode:
        log.warning("Refusing to sync, music player is not in offline mode")
        return

    sync = OfflineSync(CommandLineSyncProgress(), force_resync)
    sync.run()


def change_playlists(playlists: list[str]) -> None:
    if len(playlists) == 0:
        log.info("Resetting enabled playlists")
    else:
        log.info("Changing playlists: %s", ",".join(playlists))

    with db.offline() as conn:
        conn.execute("BEGIN")
        conn.execute("DELETE FROM playlists")
        conn.executemany("INSERT INTO playlists VALUES (?)", [(playlist,) for playlist in playlists])
        conn.execute("COMMIT")
