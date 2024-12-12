import html
import json
from sqlite3 import Connection

from aiohttp import web

from raphson_mp import auth, db, lyrics
from raphson_mp.decorators import route
from raphson_mp.lyrics import PlainLyrics
from raphson_mp.music import Track


@route("/{relpath}/info")
async def route_info(request: web.Request, conn: Connection, _user: auth.User):
    relpath = request.match_info["relpath"]
    track = Track.by_relpath(conn, relpath)
    if track is None:
        raise web.HTTPNotFound(reason="track not found")
    return web.json_response(track.info_dict())


@route("/{relpath}/audio")
async def route_audio(request: web.Request, _conn: Connection, _user: auth.User):
    relpath = request.match_info["relpath"]
    with db.offline(read_only=True) as conn_offline:
        music_data: bytes = conn_offline.execute(
            """SELECT music_data FROM content WHERE path=?""", (relpath,)
        ).fetchone()[0]
        return web.Response(body=music_data, content_type="audio/webm")


@route("/{relpath}/cover")
async def route_album_cover(request: web.Request, _conn: Connection, _user: auth.User):
    relpath = request.match_info["relpath"]
    with db.offline(read_only=True) as conn_offline:
        cover_data: bytes = conn_offline.execute(
            """SELECT cover_data FROM content WHERE path=?""", (relpath,)
        ).fetchone()[0]
        return web.Response(body=cover_data, content_type="image/webp")


@route("/{relpath}/lyrics")
async def route_lyrics(request: web.Request, _conn: Connection, _user: auth.User):
    """
    Get lyrics for the provided track path.
    """
    relpath = request.match_info["relpath"]
    with db.offline(read_only=True) as conn_offline:
        lyrics_json_str: str = conn_offline.execute(
            "SELECT lyrics_json FROM content WHERE path=?", (relpath,)
        ).fetchone()[0]
        lyrics_json = json.loads(lyrics_json_str)
        if "found" in lyrics_json and lyrics_json["found"]:
            # Legacy HTML lyrics, best effort conversion from HTML to plain text
            text = html.unescape(lyrics_json["html"].replace("\n", "").replace("<br>", "\n"))
            lyr = PlainLyrics(lyrics_json["source"], text)
        elif (
            "lyrics" in lyrics_json
            and "source_url" in lyrics_json
            and lyrics_json["lyrics"] is not None
            and lyrics_json["source_url"] is not None
        ):
            # Legacy plaintext lyrics
            lyr = PlainLyrics(lyrics_json["source_url"], lyrics_json["lyrics"])
        elif "type" in lyrics_json:
            # Modern lyrics
            lyr = lyrics.from_dict(lyrics_json)
        else:
            lyr = None
        return web.json_response(lyrics.to_dict(lyr))
