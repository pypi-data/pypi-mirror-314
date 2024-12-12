from sqlite3 import Connection

from aiohttp import web

from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.response import template


@route("")
async def route_info(_request: web.Request, _conn: Connection, _user: User):
    """
    Information/manual page
    """
    return await template("info.jinja2")
