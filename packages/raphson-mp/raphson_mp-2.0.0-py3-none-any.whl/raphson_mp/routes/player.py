import asyncio
import shutil
import time
from pathlib import Path
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db, music, scanner, settings, util
from raphson_mp.auth import StandardUser, User
from raphson_mp.decorators import route
from raphson_mp.music import Track
from raphson_mp.response import template


@route("", redirect_to_login=True)
async def route_player(request: web.Request, _conn: Connection, user: User):
    """
    Main player page. Serves player.jinja2 template file.
    """
    response = await template(
        "player.jinja2",
        mobile=util.is_mobile(request),
        primary_playlist=user.primary_playlist,
        load_timestamp=int(time.time()),
        offline_mode=settings.offline_mode,
    )

    # Refresh token cookie
    if isinstance(user, StandardUser):
        assert user.session
        user.session.set_cookie(response)

    return response


@route("/copy_track", method="POST")
async def route_copy_track(request: web.Request, conn: Connection, user: User):
    """
    Endpoint used by music player to copy a track to the user's primary playlist
    """
    json = await request.json()
    playlist_name = cast(str, json["playlist"])

    playlist = music.user_playlist(conn, playlist_name, user.user_id)
    if not user.admin and not playlist.write:
        raise web.HTTPForbidden(reason="no write access")

    track = Track.by_relpath(conn, cast(str, json["track"]))

    if track is None:
        raise web.HTTPBadRequest(reason="track does not exist")

    if track.playlist == playlist.name:
        raise web.HTTPBadRequest(reason="track already in playlist")

    def thread():
        shutil.copy(track.path, playlist.path)
    await asyncio.to_thread(thread)

    with db.connect() as writable_conn:
        await scanner.scan_track(writable_conn, playlist_name, Path(playlist.path, track.path.name))

    raise web.HTTPNoContent()
