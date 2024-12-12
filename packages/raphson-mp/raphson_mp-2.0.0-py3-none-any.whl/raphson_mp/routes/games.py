from sqlite3 import Connection

from aiohttp import web

from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.response import template


@route("/guess", redirect_to_login=True)
async def route_guess(_request: web.Request, _conn: Connection, _user: User):
    return await template("games_guess.jinja2")


@route("/chairs", redirect_to_login=True)
async def route_chairs(_request: web.Request, _conn: Connection, _user: User):
    return await template("games_chairs.jinja2")
