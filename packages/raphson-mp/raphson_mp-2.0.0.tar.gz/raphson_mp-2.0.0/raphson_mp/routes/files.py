import asyncio
from pathlib import Path
from sqlite3 import Connection
from typing import cast

from aiohttp import web

from raphson_mp import auth, db, music, scanner, settings, util
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.music import Playlist
from raphson_mp.response import directory_as_zip, file_attachment, template
from raphson_mp.util import urlencode


@route("", redirect_to_login=True)
async def route_files(request: web.Request, conn: Connection, user: User):
    """
    File manager
    """
    path = request.query.get("path", ".")
    browse_path = music.from_relpath(path)

    show_trashed = "trash" in request.query

    if browse_path.resolve() == settings.music_dir.resolve():
        parent_path = None
        write_permission = user.admin
    else:
        parent_path = music.to_relpath(browse_path.parent)
        # If the base directory is writable, all paths inside it will be, too.
        playlist = Playlist.from_path(conn, browse_path)
        write_permission = playlist.has_write_permission(user)

    def thread():
        with db.connect(read_only=True) as conn:
            children: list[dict[str, str]] = []

            for path in browse_path.iterdir():
                if music.is_trashed(path) != show_trashed:
                    continue

                relpath = music.to_relpath(path)

                file_info = {
                    "path": relpath,
                    "name": path.name,
                    "type": "dir" if path.is_dir() else "file",
                }
                children.append(file_info)

                if path.is_dir():
                    continue

                row = conn.execute(
                    """
                    SELECT title, (SELECT GROUP_CONCAT(artist, ",") FROM track_artist WHERE track = path GROUP BY track)
                    FROM track
                    WHERE path = ?
                    """,
                    (relpath,),
                ).fetchone()

                if row:
                    title, artists = row
                    file_info["type"] = "music"
                    file_info["title"] = title if title else ""
                    file_info["artist"] = artists if artists else ""

        # Sort directories first, and ignore case for file name
        def sort_name(obj: dict[str, str]) -> str:
            return ("a" if obj["type"] == "dir" else "b") + obj["name"].lower()

        return sorted(children, key=sort_name)

    # iterdir() is slow and blocking, so must be run in a separate thread
    children = await asyncio.to_thread(thread)

    return await template(
        "files.jinja2",
        base_path=music.to_relpath(browse_path),
        parent_path=parent_path,
        write_permission=write_permission,
        files=children,
        music_extensions=",".join(music.MUSIC_EXTENSIONS),
        show_trashed=show_trashed,
    )


@route("/upload", method="POST")
async def route_upload(request: web.Request, conn: Connection, user: User):
    """
    Form target to upload file, called from file manager
    """
    form = await request.post()

    upload_dir = music.from_relpath(cast(str, form["dir"]))

    playlist = Playlist.from_path(conn, upload_dir)
    if not playlist.has_write_permission(user):
        raise web.HTTPForbidden(reason="No write permission for this playlist")

    if len(form.getall("upload")) == 0:
        raise web.HTTPBadRequest(reason="No files provided.")

    for uploaded_file in cast(list[web.FileField], form.getall("upload")):
        if uploaded_file.filename == "":
            raise web.HTTPBadRequest(reason="Blank file name. Did you select a file?")

        util.check_filename(uploaded_file.filename)
        Path(upload_dir, uploaded_file.filename).write_bytes(uploaded_file.file.read())

    with db.connect() as writable_conn:
        await scanner.scan_tracks(writable_conn, playlist.name)

    raise web.HTTPSeeOther("/files?path=" + urlencode(music.to_relpath(upload_dir)))


@route("/rename")
async def route_rename_get(request: web.Request, _conn: Connection, _user: User):
    path = music.from_relpath(request.query["path"])
    back_url = request.query["back_url"]
    return await template("files_rename.jinja2", path=music.to_relpath(path), name=path.name, back_url=back_url)


@route("/rename", method="POST")
async def route_rename_post(request: web.Request, conn: Connection, user: User):
    if request.content_type == "application/json":
        json = await request.json()
        relpath = cast(str, json["path"])
        new_name = cast(str, json["new_name"])
    else:
        form = await request.post()
        relpath = cast(str, form["path"])
        new_name = cast(str, form["new-name"])

    path = music.from_relpath(relpath)
    util.check_filename(new_name)

    playlist = Playlist.from_path(conn, path)
    if not playlist.has_write_permission(user):
        raise web.HTTPForbidden(reason="No write permission for this playlist")

    path.rename(Path(path.parent, new_name))

    with db.connect() as writable_conn:
        # TODO use scanner.scan_track to only scan the two changed tracks
        await scanner.scan_tracks(writable_conn, playlist.name)

    if request.content_type == "application/json":
        raise web.HTTPNoContent()

    raise web.HTTPSeeOther("/files?path=" + util.urlencode(music.to_relpath(path.parent)))


@route("/mkdir", method="POST")
async def route_mkdir(request: web.Request, conn: Connection, user: auth.User):
    """
    Create directory, then enter it
    """
    form = await request.post()
    relpath = cast(str, form["path"])
    dirname = cast(str, form["dirname"])

    path = music.from_relpath(relpath)

    playlist = Playlist.from_path(conn, path)
    if not playlist.has_write_permission(user):
        raise web.HTTPForbidden(reason="No write permission for this playlist")

    util.check_filename(dirname)
    Path(path, dirname).mkdir()
    raise web.HTTPSeeOther("/files?path=" + urlencode(music.to_relpath(path)))


@route("/download")
async def route_download(request: web.Request, _conn: Connection, _user: User):
    """
    Download single file
    """
    path = music.from_relpath(request.query["path"])
    return file_attachment(path)


@route("/download_zip")
async def route_download_zip(request: web.Request, _conn: Connection, _user: User):
    """
    Download directory as zip file
    """
    path = music.from_relpath(request.query["path"])
    return directory_as_zip(path)
