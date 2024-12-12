import logging
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import auth
from raphson_mp.auth import AuthError, User
from raphson_mp.decorators import route
from raphson_mp.response import template

log = logging.getLogger(__name__)



@route("/login", public=True)
async def route_login_get(request: web.Request, conn: Connection):
    try:
        await auth.verify_auth_cookie(request, conn)
        # User is already logged in
        raise web.HTTPSeeOther("/")
    except AuthError:
        pass

    return await template("login.jinja2", invalid_password=False)


@route("/login", method="POST", public=True)
async def route_login_post(request: web.Request, conn: Connection):
    if request.content_type == "application/json":
        data = await request.json()
    else:
        data = await request.post()
    username: str = cast(str, data["username"])
    password: str = cast(str, data["password"])

    session = await auth.log_in(request, conn, username, password)

    if session is None:
        if request.content_type == "application/json":
            raise web.HTTPForbidden()

        return await template("login.jinja2", invalid_password=True)

    if request.content_type == "application/json":
        return web.json_response({"token": session.token, "csrf": session.csrf_token})

    response = web.HTTPSeeOther("/")
    session.set_cookie(response)
    raise response


@route("/get_csrf")
async def route_get_csrf(_request: web.Request, _conn: Connection, user: User):
    """
    Get CSRF token
    """
    return web.json_response({"token": user.csrf})
