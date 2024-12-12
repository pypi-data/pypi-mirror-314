import asyncio
import logging
import tempfile
from pathlib import Path
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import downloader, music
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.response import template

_LOGGER = logging.getLogger(__name__)



@route("", redirect_to_login=True)
async def route_download(_request: web.Request, conn: Connection, user: User):
    """Download page"""
    playlists = [
        (playlist.name, playlist.write)
        for playlist in music.user_playlists(conn, user.user_id, all_writable=user.admin)
    ]

    return await template("download.jinja2", primary_playlist=user.primary_playlist, playlists=playlists)


@route("/search", method="POST")
async def route_search(request: web.Request, _conn: Connection, _user: User):
    """Search using yt-dlp"""
    query = cast(str, (await request.json())["query"])
    logger = downloader.YtdlLogger()
    results = await asyncio.to_thread(downloader.search, query, logger)
    return web.json_response({"results": results})


@route("/ytdl", method="POST")
async def route_ytdl(request: web.Request, conn: Connection, user: User):
    """
    Use yt-dlp to download the provided URL to a playlist directory
    """
    json = await request.json()
    directory: str = cast(str, json["directory"])
    url: str = cast(str, json["url"])

    playlist = music.playlist(conn, directory)
    if not playlist.has_write_permission(user):
        raise web.HTTPForbidden(reason="No write permission for this playlist")

    _LOGGER.info("ytdl %s %s", directory, url)

    return web.Response(body=downloader.download(playlist, url))


@route("/ephemeral")
async def route_ephemeral(request: web.Request, _conn: Connection):
    url = request.query.get("url")
    assert url
    with tempfile.TemporaryDirectory() as tempdir:
        temp_path = Path(tempdir)
        async for _log in downloader.download(temp_path, url):
            pass
        return web.FileResponse(next(temp_path.iterdir()))
