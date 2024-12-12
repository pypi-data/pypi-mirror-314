from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db
from raphson_mp.auth import User
from raphson_mp.decorators import route


@route("/now_playing", method="POST")
async def route_now_playing(_request: web.Request, _conn: Connection, _user: User):
    raise web.HTTPNoContent()


@route("/played", method="POST")
async def route_played(request: web.Request, _conn: Connection, _user: User):
    with db.offline() as conn:
        json = await request.json()
        track = cast(str, json["track"])
        timestamp = cast(int, json["timestamp"])
        conn.execute("INSERT INTO history VALUES (?, ?)", (timestamp, track))
    raise web.HTTPNoContent()
