import logging
import time
from pathlib import Path
from sqlite3 import Connection
from tempfile import NamedTemporaryFile

from aiohttp import web

from raphson_mp import (acoustid, cache, db, image, lyrics, music, musicbrainz,
                        process, scanner, settings)
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.image import ImageFormat
from raphson_mp.lyrics import PlainLyrics, TimeSyncedLyrics
from raphson_mp.music import AudioType, Track

log = logging.getLogger(__name__)



def _track(conn: Connection, relpath: str) -> Track:
    track = Track.by_relpath(conn, relpath)
    if track is None:
        raise web.HTTPNotFound(reason="track not found")
    return track


@route("/{relpath}/info")
async def route_info(request: web.Request, conn: Connection, _user: User):
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)
    return web.json_response(track.info_dict())


@route("/{relpath}/video")
async def route_video(request: web.Request, conn: Connection, _user: User):
    """
    Return video stream
    """
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)
    meta = track.metadata()

    if meta.video == "vp9":
        output_format = "webm"
        output_media_type = "video/webm"
    elif meta.video == "h264":
        output_format = "mp4"
        output_media_type = "video/mp4"
    else:
        raise web.HTTPBadRequest(reason="file has no suitable video stream")

    cache_key: str = f"video{track.relpath}{track.mtime}"

    response = await cache.retrieve_response(cache_key, output_media_type)

    if response is None:
        with NamedTemporaryFile() as tempfile:
            await process.run(
                "ffmpeg",
                *settings.ffmpeg_flags(),
                "-y",
                "-i",
                track.path.as_posix(),
                "-c:v",
                "copy",
                "-map",
                "0:v",
                "-f",
                output_format,
                tempfile.name,
            )
            await cache.store(cache_key, Path(tempfile.name), cache.MONTH)
        response = await cache.retrieve_response(cache_key, output_media_type)
        if response is None:
            raise ValueError()

    return response


@route("/{relpath}/audio")
async def route_audio(request: web.Request, conn: Connection, _user: User):
    """
    Get transcoded audio for the given track path.
    """
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)

    last_modified = track.mtime_dt
    if request.if_modified_since and last_modified <= request.if_modified_since:
        raise web.HTTPNotModified()

    type_str = request.query["type"]
    if type_str == "webm_opus_high":
        audio_type = AudioType.WEBM_OPUS_HIGH
        media_type = "audio/webm"
    elif type_str == "webm_opus_low":
        audio_type = AudioType.WEBM_OPUS_LOW
        media_type = "audio/webm"
    elif type_str == "mp4_aac":
        audio_type = AudioType.MP4_AAC
        media_type = "audio/mp4"
    elif type_str == "mp3_with_metadata":
        audio_type = AudioType.MP3_WITH_METADATA
        media_type = "audio/mp3"
    else:
        raise web.HTTPBadRequest(reason="invalid audio type")

    audio = await track.transcoded_audio(audio_type)
    response = web.Response(body=audio, content_type=media_type)
    if audio_type == AudioType.MP3_WITH_METADATA:
        mp3_name = track.metadata().filename_title()
        response.headers["Content-Disposition"] = f'attachment; filename="{mp3_name}"'
    response.last_modified = last_modified
    response.headers['Cache-Control'] = 'no-cache'  # always verify last-modified
    return response


@route("/{relpath}/cover")
async def route_album_cover(request: web.Request, conn: Connection, _user: User):
    """
    Get album cover image for the provided track path.
    """
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)

    meme = "meme" in request.query and bool(int(request.query["meme"]))

    if request.query["quality"] == "high":
        quality = image.QUALITY_HIGH
    elif request.query["quality"] == "low":
        quality = image.QUALITY_LOW
    else:
        raise ValueError("invalid quality")

    last_modified = track.mtime_dt
    if request.if_modified_since and last_modified <= request.if_modified_since:
        raise web.HTTPNotModified()

    image_bytes = await track.get_cover(meme, quality, ImageFormat.WEBP)

    response = web.Response(body=image_bytes, content_type="image/webp")
    response.last_modified = last_modified
    response.headers['Cache-Control'] = 'no-cache'  # always verify last-modified
    return response


@route("/{relpath}/lyrics")
async def route_lyrics(request: web.Request, conn: Connection, _user: User):
    """
    Get lyrics for the provided track path.
    """
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)

    last_modified = track.mtime_dt
    if request.if_modified_since and last_modified <= request.if_modified_since:
        raise web.HTTPNotModified()

    lyr = await track.lyrics()

    if "type" in request.query:
        if request.query["type"] == "plain" and isinstance(lyr, TimeSyncedLyrics):
            lyr = lyr.to_plain()
        elif request.query["type"] == "synced" and isinstance(lyr, PlainLyrics):
            lyr = None

    response = web.json_response(lyrics.to_dict(lyr))
    response.last_modified = last_modified
    response.headers['Cache-Control'] = 'no-cache'  # always verify last-modified
    return response

@route("/{relpath}/update_metadata", method="POST")
async def route_update_metadata(request: web.Request, conn: Connection, user: User):
    """
    Endpoint to update track metadata
    """
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)

    playlist = music.playlist(conn, track.playlist)
    if not playlist.has_write_permission(user):
        raise web.HTTPForbidden(reason="No write permission for this playlist")

    meta = track.metadata()

    json = await request.json()
    meta.title = json["title"]
    meta.album = json["album"]
    meta.artists = json["artists"]
    meta.album_artist = json["album_artist"]
    meta.tags = json["tags"]
    meta.year = json["year"]
    meta.lyrics = json["lyrics"]

    await meta.save()

    with db.connect() as writable_conn:
        await scanner.scan_track(writable_conn, track.playlist, track.path, track.relpath)

    raise web.HTTPNoContent()


@route("/{relpath}/acoustid")
async def route_acoustid(request: web.Request, conn: Connection, _user: User):
    relpath = request.match_info["relpath"]
    track = _track(conn, relpath)
    fp = await acoustid.get_fingerprint(track.path)
    known_ids: set[str] = set()
    meta_list: list[musicbrainz.MBMeta] = []
    async for recording in acoustid.lookup(fp):
        log.info("found recording: %s", recording)
        async for meta in musicbrainz.get_recording_metadata(recording):
            if meta.id in known_ids:
                continue
            log.info("found possible metadata: %s", meta)
            meta_list.append(meta)
            known_ids.add(meta.id)

        if len(meta_list) > 0:
            break

        time.sleep(2)  # crude way of avoiding rate limits

    return web.json_response(meta_list)
