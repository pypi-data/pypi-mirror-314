from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.music import Track
from raphson_mp.response import template


@route("/add", method="POST")
async def route_add(request: web.Request, _conn: Connection, user: User):
    """Used by music player"""
    json = await request.json()
    track_path = cast(str, json["track"])
    with db.connect() as writable_conn:
        writable_conn.execute("INSERT OR IGNORE INTO dislikes (user, track) VALUES (?, ?)", (user.user_id, track_path))
    raise web.HTTPNoContent()


@route("/remove", method="POST")
async def route_remove(request: web.Request, _conn: Connection, user: User):
    """Used by form on dislikes page"""
    form = await request.post()
    relpath = cast(str, form["track"])
    with db.connect() as writable_conn:
        writable_conn.execute("DELETE FROM dislikes WHERE user=? AND track=?", (user.user_id, relpath))
    raise web.HTTPSeeOther("/dislikes")


@route("")
async def route_dislikes(_request: web.Request, conn: Connection, user: User):
    """
    Page showing a table with disliked tracks, with buttons to undo disliking each trach.
    """
    rows = conn.execute(
        """
        SELECT playlist, track
        FROM dislikes JOIN track on dislikes.track = track.path
        WHERE user=?
        """,
        (user.user_id,),
    ).fetchall()
    tracks = [
        {
            "path": path,
            "playlist": playlist,
            "title": cast(Track, Track.by_relpath(conn, path)).metadata().display_title(),
        }
        for playlist, path in rows
    ]

    return await template("dislikes.jinja2", tracks=tracks)


@route("/json")
async def route_json(_request: web.Request, conn: Connection, user: User):
    """
    Return disliked track paths in json format, for offline mode sync
    """
    rows = conn.execute("SELECT track FROM dislikes WHERE user=?", (user.user_id,)).fetchall()

    return web.json_response({"tracks": [row[0] for row in rows]})
