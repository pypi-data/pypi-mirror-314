import asyncio
import os
import time
from base64 import b32encode
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.image import QUALITY_HIGH, ImageFormat
from raphson_mp.lyrics import PlainLyrics, TimeSyncedLyrics
from raphson_mp.music import AudioType, Track
from raphson_mp.response import template


def gen_share_code() -> str:
    """
    Generate new random share code
    """
    return b32encode(os.urandom(8)).decode().lower().rstrip("=")


def track_by_code(conn: Connection, code: str) -> Track:
    """
    Find track using a provided share code
    """
    row = conn.execute("SELECT track FROM shares WHERE share_code=?", (code,)).fetchone()
    if row is None:
        raise web.HTTPNotFound(reason="no share was found with the given code")

    track = Track.by_relpath(conn, row[0])
    if track is None:
        raise ValueError("track cannot be null, foreign key broken?")
    return track


@route("/create", method="POST")
async def create(request: web.Request, conn: Connection, user: User):
    """
    Endpoint to create a share link, called from web music player.
    """
    json = await request.json()
    relpath = cast(str, json["track"])
    track = Track.by_relpath(conn, relpath)
    if track is None:
        raise web.HTTPBadRequest(reason="track does not exist")

    code = gen_share_code()

    def thread():
        with db.connect() as writable_conn:
            writable_conn.execute(
                "INSERT INTO shares (share_code, user, track, create_timestamp) VALUES (?, ?, ?, ?)",
                (code, user.user_id, track.relpath, int(time.time())),
            )
    await asyncio.to_thread(thread)

    return web.json_response({"code": code})


@route("/{code}/cover", public=True)
async def cover(request: web.Request, conn: Connection):
    """
    Route providing a WEBP album cover image
    """
    code = request.match_info["code"]
    track = track_by_code(conn, code)
    cover_bytes = await track.get_cover(meme=False, img_quality=QUALITY_HIGH, img_format=ImageFormat.WEBP)
    return web.Response(body=cover_bytes, content_type="image/webp")


@route("/{code}/audio", public=True)
async def audio(request: web.Request, conn: Connection):
    """
    Route to stream opus audio.
    """
    code = request.match_info["code"]
    track = track_by_code(conn, code)
    audio_bytes = await track.transcoded_audio(AudioType.WEBM_OPUS_HIGH)

    return web.Response(body=audio_bytes, content_type="audio/webm")


@route("/{code}/download/{file_format}", public=True)
async def download(request: web.Request, conn: Connection):
    """
    Route to download an audio file.
    """
    code = request.match_info["code"]
    file_format = request.match_info["file_format"]
    track = track_by_code(conn, code)

    if file_format == "original":
        response = web.FileResponse(track.path)
        response.headers["Content-Disposition"] = f'attachment; filename="{track.path.name}"'
    elif file_format == "mp3":
        audio_bytes = await track.transcoded_audio(AudioType.MP3_WITH_METADATA)
        response = web.Response(body=audio_bytes, content_type="audio/mp3")
        download_name = track.metadata().download_name() + ".mp3"
        response.headers["Content-Disposition"] = f'attachment; filename="{download_name}"'
    else:
        raise web.HTTPBadRequest(reason="invalid format")

    return response


@route("/{code}", public=True)
async def show(request: web.Request, conn: Connection):
    """
    Web page displaying a shared track.
    """
    code = request.match_info["code"]
    track = track_by_code(conn, code)

    (shared_by,) = conn.execute(
        """
        SELECT username
        FROM shares JOIN user ON shares.user = user.id
        WHERE share_code=?
        """,
        (code,),
    ).fetchone()

    lyrics = await track.lyrics()
    meta = track.metadata()

    if lyrics is None:
        lyrics_text = None
    elif isinstance(lyrics, PlainLyrics):
        lyrics_text = lyrics.text
    elif isinstance(lyrics, TimeSyncedLyrics):
        lyrics_text = lyrics.to_plain().text
    else:
        raise ValueError(lyrics)

    return await template(
        "share.jinja2", code=code, shared_by=shared_by, track=meta.display_title(), lyrics=lyrics_text
    )
