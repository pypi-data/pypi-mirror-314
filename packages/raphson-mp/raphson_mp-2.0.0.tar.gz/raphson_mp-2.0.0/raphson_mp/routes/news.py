import tempfile
from sqlite3 import Connection

import aiohttp
from aiohttp import web

from raphson_mp import process, settings
from raphson_mp.auth import User
from raphson_mp.decorators import route


@route("/audio")
async def audio(_request: web.Request, _conn: Connection, _user: User):
    with tempfile.NamedTemporaryFile() as temp_input, tempfile.NamedTemporaryFile() as temp_output:
        if not settings.news_server:
            raise web.HTTPServiceUnavailable(reason="news server not configured")

        # TODO can ffmpeg read wav from stdin? no temp_input necessary, stream response body to subprocess

        # Download wave audio to temp file
        async with aiohttp.ClientSession(settings.news_server, headers={"User-Agent": settings.user_agent}) as session:
            async with session.get("/news.wav") as response:
                if response.status == 503:
                    raise web.HTTPServiceUnavailable(reason="news server not configured")

                response.raise_for_status()

                while chunk := await response.content.read(1024 * 1024):
                    temp_input.write(chunk)

        temp_input.flush()

        # Transcode wave PCM audio to opus
        await process.run(
            "ffmpeg",
            "-y",  # overwriting file is required, because the created temp file already exists
            "-hide_banner",
            "-nostats",
            "-loglevel",
            settings.ffmpeg_log_level,
            "-i",
            temp_input.name,
            "-f",
            "webm",
            "-c:a",
            "libopus",
            "-b:a",
            "64k",
            "-vbr",
            "on",
            "-filter:a",
            settings.loudnorm_filter,
            temp_output.name,
        )

        audio_bytes = temp_output.read()

    return web.Response(body=audio_bytes, content_type="audio/webm")
