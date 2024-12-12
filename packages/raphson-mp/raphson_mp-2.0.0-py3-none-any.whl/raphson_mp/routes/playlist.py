import asyncio
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import db, metadata, music, scanner, settings, spotify, util
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.metadata import normalize_title
from raphson_mp.music import PlaylistStats, TagMode
from raphson_mp.response import template
from raphson_mp.spotify import SpotifyTrack


# TODO change URL to simply /playlists instead of /playlists/manage
@route("/manage")
async def route_playlists(_request: web.Request, conn: Connection, user: User):
    """
    Playlist management page
    """
    user_playlists = music.user_playlists(conn, user.user_id)
    (primary_playlist,) = conn.execute("SELECT primary_playlist FROM user WHERE id=?", (user.user_id,)).fetchone()

    playlists_stats: list[PlaylistStats] = []
    for playlist in user_playlists:
        await asyncio.sleep(0)  # yield to event loop
        playlists_stats.append(playlist.stats())

    spotify_available = settings.spotify_api_id and settings.spotify_api_secret

    return await template(
        "playlists.jinja2",
        user_is_admin=user.admin,
        playlists=user_playlists,
        primary_playlist=primary_playlist,
        playlists_stats=playlists_stats,
        spotify_available=spotify_available,
    )


@route("/favorite", method="POST")
async def route_favorite(request: web.Request, _conn: Connection, user: User):
    """
    Form target to mark a playlist as favorite.
    """
    form = await request.post()
    playlist = cast(str, form["playlist"])
    is_favorite = cast(str, form["favorite"])
    with db.connect() as writable_conn:
        if is_favorite == "1":
            writable_conn.execute(
                """
                INSERT INTO user_playlist_favorite
                VALUES (?, ?)
                ON CONFLICT DO NOTHING
                """,
                (user.user_id, playlist),
            )
        else:
            writable_conn.execute(
                """
                DELETE FROM user_playlist_favorite
                WHERE user=? AND playlist=?
                """,
                (user.user_id, playlist),
            )

    raise web.HTTPSeeOther("/playlist/manage")


@route("/create", method="POST")
async def route_create(request: web.Request, _conn: Connection, user: User):
    """
    Form target to create playlist, called from /playlist/manage page
    """
    name = cast(str, (await request.post())["name"])

    util.check_filename(name)

    path = settings.music_dir / name

    if path.exists():
        raise web.HTTPBadRequest(reason="Playlist path already exists")

    path.mkdir()

    with db.connect() as writable_conn:
        scanner.scan_playlists(writable_conn)  # This creates a row for the playlist in the playlist table

        # New playlist should be writable for user who created it
        writable_conn.execute("INSERT INTO user_playlist_write VALUES (?, ?)", (user.user_id, name))

    raise web.HTTPSeeOther("/playlist/manage")


@route("/share")
async def route_share_get(request: web.Request, conn: Connection, _user: User):
    """
    Page to select a username to share the provided playlist with
    """
    usernames = [row[0] for row in conn.execute("SELECT username FROM user")]
    csrf = request.query["csrf"]
    playlist_relpath = request.query["playlist"]
    return await template("playlists_share.jinja2", csrf=csrf, playlist=playlist_relpath, usernames=usernames)


@route("/share", method="POST")
async def route_share_post(request: web.Request, conn: Connection, user: User):
    """
    Form target to submit the selected username
    """
    form = await request.post()
    playlist_relpath = cast(str, form["playlist"])
    username = cast(str, form["username"])

    (target_user_id,) = conn.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone()

    # Verify playlist exists and user has write access
    playlist = music.user_playlist(conn, playlist_relpath, user.user_id)

    if not playlist.write and not user.admin:
        raise web.HTTPForbidden(reason="Cannot share playlist if you do not have write permission")

    with db.connect() as writable_conn:
        writable_conn.execute(
            "INSERT INTO user_playlist_write VALUES(?, ?) ON CONFLICT DO NOTHING", (target_user_id, playlist_relpath)
        )

    raise web.HTTPSeeOther("/playlist/manage")


@route("/list")
async def route_list(_request: web.Request, conn: Connection, user: User):
    user_playlists = music.user_playlists(conn, user.user_id, all_writable=user.admin)
    json = [
        {
            "name": playlist.name,
            "track_count": playlist.track_count,
            "favorite": playlist.favorite,
            "write": playlist.write,
        }
        for playlist in user_playlists
        if playlist.track_count > 0
    ]
    return web.json_response(json)


@route("/{playlist}/choose_track", method="POST")
async def route_track(request: web.Request, conn: Connection, user: User):
    """
    Choose random track from the provided playlist directory.
    """
    playlist_name = request.match_info["playlist"]
    playlist = music.playlist(conn, playlist_name)
    json = await request.json()
    require_metadata: bool = cast(bool, json["require_metadata"]) if "require_metadata" in json else False

    if "tag_mode" in json:
        tag_mode = TagMode.from_value(cast(str, json["tag_mode"]))
        tags = cast(list[str], json["tags"])
        chosen_track = await playlist.choose_track(
            user, require_metadata=require_metadata, tag_mode=tag_mode, tags=tags
        )
    else:
        chosen_track = await playlist.choose_track(user, require_metadata=require_metadata)

    if chosen_track is None:
        raise web.HTTPNotFound(reason="no track found")

    chosen_track.conn = conn
    return web.json_response(chosen_track.info_dict())


def _fuzzy_match_track(
    spotify_normalized_title: str, local_track_key: tuple[str, tuple[str]], spotify_track: SpotifyTrack
) -> bool:
    (local_track_normalized_title, local_track_artists) = local_track_key
    if not util.str_match(spotify_normalized_title, local_track_normalized_title):
        return False

    # Title matches, now check if artist matches (more expensive)
    for artist_a in spotify_track.artists:
        for artist_b in local_track_artists:
            if util.str_match(artist_a, artist_b):
                return True

    return False


@route("/{playlist}/compare_spotify")
async def route_compare_spotify(request: web.Request, conn: Connection, _user: User):
    playlist_name = request.match_info["playlist"]

    local_tracks: dict[tuple[str, tuple[str]], tuple[str, list[str]]] = {}

    for title, artists in conn.execute(
        """
        SELECT title, GROUP_CONCAT(artist, ';') AS artists
        FROM track JOIN track_artist ON track.path = track_artist.track
        WHERE track.playlist = ?
        GROUP BY track.path
        """,
        (playlist_name,),
    ):
        local_track = (title, artists.split(";"))
        key = (normalize_title(title), tuple(local_track[1]))
        local_tracks[key] = local_track

    playlist_id = request.query["playlist_id"]

    client = spotify.SpotifyClient()
    duplicate_check: set[str] = set()
    duplicates: list[SpotifyTrack] = []
    both: list[tuple[tuple[str, list[str]], SpotifyTrack]] = []
    only_spotify: list[SpotifyTrack] = []
    only_local: list[tuple[str, list[str]]] = []

    i = 0
    async for spotify_track in client.get_playlist(playlist_id):
        i += 1
        if i % 10 == 0:
            await asyncio.sleep(0)  # yield to event loop

        normalized_title = metadata.normalize_title(spotify_track.title)

        # Spotify duplicates
        duplicate_check_entry = spotify_track.display
        if duplicate_check_entry in duplicate_check:
            duplicates.append(spotify_track)
        duplicate_check.add(duplicate_check_entry)

        # Try to find fast exact match
        local_track_key = (normalized_title, tuple(spotify_track.artists))
        if local_track_key in local_tracks:
            local_track = local_tracks[local_track_key]
        else:
            # Cannot find exact match, look for partial match
            for local_track_key in local_tracks.keys():
                if _fuzzy_match_track(normalized_title, local_track_key, spotify_track):
                    break
            else:
                # no match found
                only_spotify.append(spotify_track)
                continue

        # match found, present in both
        both.append((local_tracks[local_track_key], spotify_track))
        del local_tracks[local_track_key]

    # any local tracks still left in the dict must have no matching spotify track
    only_local.extend(local_tracks.values())

    return await template(
        "spotify_compare.jinja2", duplicates=duplicates, both=both, only_local=only_local, only_spotify=only_spotify
    )
