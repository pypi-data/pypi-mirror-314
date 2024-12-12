import asyncio
from dataclasses import dataclass
import logging
import time
from sqlite3 import Connection
from typing import Any, cast

from aiohttp import web

from raphson_mp import db, i18n
from raphson_mp.auth import PrivacyOption, StandardUser, User
from raphson_mp.decorators import route
from raphson_mp.metadata import Metadata
from raphson_mp.music import Track
from raphson_mp.response import template

log = logging.getLogger(__name__)


@dataclass
class NowPlaying:
    user_display_name: str
    update_time: int
    lastfm_update_timestamp: int
    paused: bool
    position: int
    duration: int
    track_path: str

    @property
    def corrected_position(self) -> int:
        if self.paused:
            return self.position

        corrected_position = self.position + int(time.time()) - self.update_time
        if corrected_position < self.duration:
            return corrected_position

        return self.duration


NOW_PLAYING: dict[str, NowPlaying] = {}


def get_file_changes_list(conn: Connection, limit: int) -> list[dict[str, str]]:
    """
    Helper function to get a list of file changes as a dictionary list. Used by route_data to
    provide a JSON API and by route_all to provide a static page with more history.
    """
    result = conn.execute(
        f"""
        SELECT timestamp, action, playlist, track
        FROM scanner_log
        ORDER BY timestamp DESC
        LIMIT {limit}
        """
    )

    action_translation = {
        "insert": i18n.gettext("Added"),
        "delete": i18n.gettext("Removed"),
        "update": i18n.gettext("Modified"),
    }

    return [
        {
            "timestamp": timestamp,
            "time_ago": i18n.format_timedelta(timestamp - int(time.time()), add_direction=True),
            "action": action_translation[action],
            "playlist": playlist,
            "track": track,
        }
        for timestamp, action, playlist, track in result
    ]


@route("", redirect_to_login=True)
async def route_activity(_request: web.Request, _conn: Connection, _user: User):
    """
    Main activity page, showing currently playing tracks and history of
    played tracks and modified files.
    """
    return await template("activity.jinja2")


@route("/data")
async def route_data(_request: web.Request, conn: Connection, _user: User):
    """
    Endpoint providing data for main activity page in JSON format.
    """
    now_playing: list[dict[str, str | int | list[str] | None]] = []
    current_time = int(time.time())
    for entry in NOW_PLAYING.values():
        if entry.update_time < current_time - 70:
            continue
        track = Track.by_relpath(conn, entry.track_path)
        if track is None:
            continue
        now_playing.append(
            {
                "username": entry.user_display_name,
                "paused": entry.paused,
                "position": entry.position,
                **track.info_dict(),
            }
        )

    result = conn.execute(
        """
        SELECT history.timestamp, user.username, user.nickname, history.track
        FROM history
            LEFT JOIN user ON history.user = user.id
        WHERE history.private = 0
        ORDER BY history.timestamp DESC
        LIMIT 10
        """
    )

    history: list[dict[str, str|int|list[str]|None]] = []
    for timestamp, username, nickname, relpath in result:
        track = Track.by_relpath(conn, relpath)
        if track is None:
            continue
        history.append({
            "time_ago": i18n.format_timedelta(timestamp - int(time.time()), add_direction=True),
            "username": nickname if nickname else username,
            **track.info_dict(),
        })

    file_changes = get_file_changes_list(conn, 10)

    return web.json_response({"now_playing": now_playing, "history": history, "file_changes": file_changes})


@route("/files")
async def route_files(_request: web.Request, conn: Connection, _user: User):
    """
    Page with long static list of changed files history, similar to route_all()
    """
    changes = get_file_changes_list(conn, 2000)

    return await template("activity_files.jinja2", changes=changes)


@route("/all")
async def route_all(_request: web.Request, conn: Connection, _user: User):
    """
    Page with long static list of playback history, similar to route_files()
    """
    result = conn.execute(
        """
        SELECT history.timestamp, user.username, user.nickname, history.playlist, history.track, track.path IS NOT NULL
        FROM history
            LEFT JOIN user ON history.user = user.id
            LEFT JOIN track ON history.track = track.path
        ORDER BY history.timestamp DESC
        LIMIT 5000
        """
    )
    history: list[dict[str, Any]] = []
    for timestamp, username, nickname, playlist, relpath, track_exists in result:
        if track_exists:
            title = cast(Track, Track.by_relpath(conn, relpath)).metadata().display_title()
        else:
            title = relpath

        history.append(
            {"time": timestamp, "username": nickname if nickname else username, "playlist": playlist, "title": title}
        )

    return await template("activity_all.jinja2", history=history)


def _get_meta(conn: Connection, relpath: str):
    track = Track.by_relpath(conn, relpath)
    if track is None:
        log.info('ignoring now_playing for track that does not exist')
        raise web.HTTPNoContent()
    return track.metadata()


@route("/now_playing", method="POST")
async def route_now_playing(request: web.Request, conn: Connection, user: User):
    """
    Send info about currently playing track. Sent frequently by the music player.
    POST body should contain a json object with:
     - csrf (str): CSRF token
     - track (str): Track relpath
     - paused (bool): Whether track is paused
     - progress (int): Track position, as a percentage
    """
    from raphson_mp import lastfm

    if user.privacy != PrivacyOption.NONE:
        log.info("Ignoring, user has enabled private mode")
        raise web.HTTPNoContent()

    json = await request.json()
    player_id = cast(str, json["player_id"])
    relpath = cast(str, json["track"])
    paused = cast(bool, json["paused"])
    position = cast(int, json["position"])
    username = user.nickname if user.nickname else user.username

    current_time = int(time.time())

    meta: Metadata | None = None

    if player_id in NOW_PLAYING:
        now_playing = NOW_PLAYING[player_id]

        now_playing.user_display_name = username
        now_playing.update_time = current_time
        now_playing.paused = paused
        now_playing.position = position

        if now_playing.track_path != relpath:
            meta = _get_meta(conn, relpath)
            now_playing.duration = meta.duration
            now_playing.track_path = relpath

        if not paused and now_playing.lastfm_update_timestamp < current_time - 60:
            user_key = lastfm.get_user_key(cast(StandardUser, user))
            if user_key:
                if not meta:
                    meta = _get_meta(conn, relpath)

                await lastfm.update_now_playing(user_key, meta)
                now_playing.lastfm_update_timestamp = current_time

    else:
        meta = _get_meta(conn, relpath)
        NOW_PLAYING[player_id] = NowPlaying(
            username, current_time, current_time, paused, position, meta.duration, relpath
        )

    raise web.HTTPNoContent()


@route("/played", method="POST")
async def route_played(request: web.Request, conn: Connection, user: User):
    """
    Route to submit an entry to played tracks history, optionally also
    scrobbling to last.fm. Used by web music player and also by offline
    sync to submit many previously played tracks.
    POST body:
     - track: relpath
     - timestamp: time at which track met played conditions (roughly)
     - csrf: csrf token (ignored in offline mode)
    """
    from raphson_mp import lastfm

    if user.privacy == PrivacyOption.HIDDEN:
        log.info("Ignoring because privacy==hidden")
        raise web.HTTPNoContent()

    json = await request.json()

    track = Track.by_relpath(conn, cast(str, json["track"]))
    if track is None:
        log.warning("skipping track that does not exist: %s", cast(str, json["track"]))
        raise web.HTTPNoContent()

    timestamp = int(cast(str, json["timestamp"]))
    private = user.privacy == PrivacyOption.AGGREGATE

    def thread():
        with db.connect() as writable_conn:
            writable_conn.execute(
                """
                INSERT INTO history (timestamp, user, track, playlist, private)
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, user.user_id, track.relpath, track.playlist, private),
            )
    await asyncio.to_thread(thread)

    # last.fm requires track length to be at least 30 seconds
    if not private and track.metadata().duration >= 30:
        lastfm_key = lastfm.get_user_key(cast(StandardUser, user))
        if lastfm_key:
            meta = track.metadata()
            await lastfm.scrobble(lastfm_key, meta, timestamp)

    raise web.HTTPNoContent()
