import asyncio
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import auth, db, i18n, music
from raphson_mp.auth import PrivacyOption, StandardUser, User
from raphson_mp.decorators import route
from raphson_mp.response import template
from raphson_mp.theme import THEMES


@route("")
async def route_account(_request: web.Request, conn: Connection, user: User):
    """
    Account information page
    """
    from raphson_mp import lastfm

    sessions = user.sessions()

    result = conn.execute("SELECT name FROM user_lastfm WHERE user=?", (user.user_id,)).fetchone()
    if result:
        (lastfm_name,) = result
    else:
        lastfm_name = None

    playlists = music.playlists(conn)

    return await template(
        "account.jinja2",
        languages=i18n.ALL_LANGUAGE_CODES,
        sessions=sessions,
        lastfm_enabled=lastfm.is_configured(),
        lastfm_name=lastfm_name,
        lastfm_connect_url=lastfm.get_connect_url(),
        playlists=playlists,
        themes=THEMES.items(),
    )


@route("/change_settings", method="POST")
async def route_change_settings(request: web.Request, _conn: Connection, user: User):
    form = await request.post()
    nickname = form["nickname"]
    lang_code = form["language"]
    privacy = form["privacy"]
    playlist = form["playlist"]
    theme = form["theme"]

    if nickname == "":
        nickname = None
    if playlist == "":
        playlist = None
    if lang_code == "":
        lang_code = None
    if privacy == "":
        privacy = None

    if lang_code and lang_code not in i18n.ALL_LANGUAGE_CODES:
        raise web.HTTPBadRequest(reason="invalid language code")

    if privacy not in PrivacyOption:
        raise web.HTTPBadRequest(reason="invalid privacy option")

    if theme not in THEMES:
        raise web.HTTPBadRequest(reason="invalid theme")

    def thread():
        with db.connect() as writable_conn:
            writable_conn.execute(
                "UPDATE user SET nickname=?, language=?, privacy=?, primary_playlist=?, theme=? WHERE id=?",
                (nickname, lang_code, privacy, playlist, theme, user.user_id),
            )
    await asyncio.to_thread(thread)

    raise web.HTTPSeeOther("/account")


@route("/change_password", method="POST")
async def route_change_password(request: web.Request, conn: Connection, user: User):
    """
    Form target to change password, called from /account page
    """
    form = await request.post()
    current_password = cast(str, form["current_password"])
    new_password = cast(str, form["new_password"])

    if not await auth.verify_password(conn, user.user_id, current_password):
        raise web.HTTPBadRequest(reason="incorrect password.")

    with db.connect() as writable_conn:
        cast(StandardUser, user).conn = writable_conn
        await user.update_password(new_password)
    raise web.HTTPSeeOther("/")
