from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db, metadata
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.offline_sync import FlaskResponseProgress, OfflineSync
from raphson_mp.response import template

sync_thread: OfflineSync | None = None


@route("/sync")
async def route_sync(_request: web.Request, _conn: Connection, _user: User):
    with db.offline(read_only=True) as offline:
        row = offline.execute("SELECT base_url, token FROM settings").fetchone()
        server, token = row if row else ("", "")

        rows = offline.execute("SELECT name FROM playlists")
        playlists = metadata.join_meta_list([row[0] for row in rows])

    return await template("offline_sync.jinja2", server=server, token=token, playlists=playlists)


@route("/settings", method="POST")
async def route_settings(request: web.Request, _conn: Connection, _user: User):
    form = await request.post()
    server = cast(str, form["server"])
    token = cast(str, form["token"])
    playlists = metadata.split_meta_list(cast(str, form["playlists"]))
    with db.offline() as offline:
        if offline.execute("SELECT base_url FROM settings").fetchone():
            offline.execute("UPDATE settings SET base_url=?, token=?", (server, token))
        else:
            offline.execute("INSERT INTO settings (base_url, token) VALUES (?, ?)", (server, token))

        offline.execute("DELETE FROM playlists")
        offline.executemany("INSERT INTO playlists VALUES (?)", [(playlist,) for playlist in playlists])
    raise web.HTTPSeeOther("/offline/sync")


@route("/stop", method="POST")
async def route_stop(_request: web.Request, _conn: Connection, _user: User) -> web.Response:
    if sync_thread:
        sync_thread.stop()
    raise web.HTTPNoContent()


@route("/start", method="POST")
async def route_start(_request: web.Request, _conn: Connection, _user: User) -> web.Response:
    global sync_thread

    if not sync_thread or not sync_thread.is_alive():
        progress = FlaskResponseProgress()
        sync_thread = OfflineSync(progress, 0)
        sync_thread.start()

    raise web.HTTPNoContent()


@route("/monitor")
async def route_monitor(_request: web.Request, _conn: Connection, _user: User) -> web.Response:
    global sync_thread

    if sync_thread and sync_thread.is_alive():
        progress = cast(FlaskResponseProgress, sync_thread.progress)
        return progress.response()

    raise web.HTTPNoContent()
