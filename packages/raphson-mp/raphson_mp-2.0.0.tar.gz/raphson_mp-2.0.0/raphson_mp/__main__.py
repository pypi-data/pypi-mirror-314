import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from collections.abc import Coroutine
from pathlib import Path
from typing import Any

from raphson_mp import auth, db, logconfig, settings

log = logging.getLogger(__name__)


def handle_start(args: Any) -> None:
    """
    Handle command to start server
    """
    from raphson_mp.server import Server

    settings.proxy_count = args.proxy_count

    if not os.getenv("MUSIC_HAS_RELOADED"):
        db.migrate()

    server = Server(args.dev, enable_tasks=True)

    server.start(args.host, args.port)


async def handle_useradd(args: Any) -> None:
    """
    Handle command to add user
    """
    username = args.username
    admin = bool(args.admin)
    password = input("Enter password:")

    await auth.User.create(username, password, admin=admin)

    log.info("User added successfully")


def handle_userdel(args: Any) -> None:
    """
    Handle command to delete user
    """
    from raphson_mp import db

    with db.connect() as conn:
        deleted = conn.execute("DELETE FROM user WHERE username=?", (args.username,)).rowcount
        if deleted == 0:
            log.warning("No user deleted, does the user exist?")
        else:
            log.info("User deleted successfully")


def handle_userlist(_args: Any) -> None:
    """
    Handle command to list users
    """
    from raphson_mp import db

    with db.connect() as conn:
        result = conn.execute("SELECT username, admin FROM user")
        if result.rowcount == 0:
            log.info("No users")
            return

        log.info("Users:")

        for username, is_admin in result:
            if is_admin:
                log.info("- %s (admin)", username)
            else:
                log.info("- %s", username)


async def handle_passwd(args: Any) -> None:
    """
    Handle command to change a user's password
    """
    from raphson_mp import db

    with db.connect(read_only=True) as conn:
        result = conn.execute("SELECT id FROM user WHERE username=?", (args.username,)).fetchone()
        if result is None:
            print("No user exists with the provided username")
            return

        user_id = result[0]
        target_user = auth.User.get(conn, user_id=user_id)

        new_password = input("Enter new password:")
        await target_user.update_password(new_password)

        print("Password updated successfully.")


async def handle_scan(_args: Any) -> None:
    """
    Handle command to scan playlists
    """
    from raphson_mp import scanner

    await scanner.scan()


def handle_migrate(_args: Any) -> None:
    """
    Handle command for database migration
    """
    from raphson_mp import db

    db.migrate()


def handle_vacuum(_args: Any) -> None:
    """
    Handle command for database vacuuming
    """
    from raphson_mp import db

    log.info("Going to vacuum databases. This will take a long time if you have large databases. Do not abort.")

    log.info("Vacuuming music.db")
    with db.connect() as conn:
        conn.execute("VACUUM")

    log.info("Vacuuming cache.db")
    with db.cache() as conn:
        conn.execute("VACUUM")

    log.info("Vacuuming offline.db")
    with db.offline() as conn:
        conn.execute("VACUUM")


def handle_sync(args: Any) -> None:
    """
    Handle command for offline mode sync
    """
    from raphson_mp import offline_sync

    if args.playlists is not None:
        if args.playlists == "favorite":
            offline_sync.change_playlists([])
            return

        playlists = args.playlists.split(",")
        offline_sync.change_playlists(playlists)
        return

    offline_sync.do_sync(args.force_resync)


async def handle_cover(args: Any) -> None:
    from raphson_mp import music

    cover_bytes = await anext(music.get_possible_covers(args.artist, args.title, args.meme))
    Path("cover.jpg").write_bytes(cover_bytes)


async def handle_acoustid(args: Any) -> None:
    from raphson_mp import acoustid, musicbrainz

    fp = await acoustid.get_fingerprint(Path(args.path))
    log.info("duration: %s", fp.duration)
    log.info("fingerprint: %s", fp.fingerprint_b64)

    recordings = acoustid.lookup(fp)

    async for recording in recordings:
        async for meta in musicbrainz.get_recording_metadata(recording):
            log.info("possible metadata for recording %s: %s", recording, meta)


async def handle_lyrics(args: Any) -> None:
    from raphson_mp.lyrics import PlainLyrics, TimeSyncedLyrics, find

    lyrics = await find(args.title, args.artist, args.album, args.duration)

    if isinstance(lyrics, PlainLyrics):
        print(lyrics.text)
    elif isinstance(lyrics, TimeSyncedLyrics):
        print(lyrics.to_lrc())
    elif lyrics is None:
        print("No lyrics found")
        sys.exit(1)
    else:
        raise ValueError(lyrics)


async def handle_bing(args: Any) -> None:
    from raphson_mp import bing

    results = await bing.image_search(args.query)
    Path("bing_result").write_bytes(results[0])
    log.info("saved to bing_result file")


def _strenv(name: str, default: str | None = None) -> str | None:
    return os.getenv("MUSIC_" + name, default)


def _intenv(name: str, default: int | None = None) -> int | None:
    text = _strenv(name, str(default) if default else None)
    if text is None:
        return default
    return int(text)


def _boolenv(name: str) -> bool:
    val = _strenv(name, "")
    return val == "1" or bool(val)


def split_by_comma(inp: str | None) -> list[str]:
    if inp is None:
        return []
    return [s.strip() for s in inp.split(",") if s.strip() != ""]


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--log-level",
        default=_strenv("LOG_LEVEL", settings.log_level),
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="set log level for Python loggers",
    )
    parser.add_argument(
        "--short-log-format", action="store_true", default=_boolenv("SHORT_LOG_FORMAT"), help="use short log format"
    )
    parser.add_argument(
        "--data-dir",
        default=_strenv("DATA_DIR", _strenv("DATA_PATH", "./data")),
        help="path to directory where program data is stored",
    )
    parser.add_argument(
        "--music-dir", default=_strenv("MUSIC_DIR", "./music"), help="path to directory where music files are stored"
    )
    # error level by default to hide unfixable "deprecated pixel format used" warning
    parser.add_argument(
        "--ffmpeg-log-level",
        default=_strenv("FFMPEG_LOG_LEVEL"),
        choices=("quiet", "fatal", "error", "warning", "info", "verbose", "debug"),
        help="log level for ffmpeg",
    )
    parser.add_argument("--track-max-duration-seconds", type=int, default=_intenv("TRACK_MAX_DURATION_SECONDS"))
    parser.add_argument(
        "--radio-playlists",
        default=_strenv("RADIO_PLAYLISTS"),
        help="comma-separated list of playlists to use for radio",
    )
    parser.add_argument("--lastfm-api-key", default=_strenv("LASTFM_API_KEY"))
    parser.add_argument("--lastfm-api-secret", default=_strenv("LASTFM_API_SECRET"))
    parser.add_argument("--spotify-api-id", default=_strenv("SPOTIFY_API_ID"))
    parser.add_argument("--spotify-api-secret", default=_strenv("SPOTIFY_API_SECRET"))
    parser.add_argument(
        "--offline",
        action="store_true",
        default=_boolenv("OFFLINE_MODE"),
        help="run in offline mode, using music synced from a primary music server",
    )
    parser.add_argument(
        "--news-server",
        help="news server url: https://github.com/Derkades/news-scraper",
        default=_strenv("NEWS_SERVER"),
    )

    subparsers = parser.add_subparsers(required=True)

    cmd_start = subparsers.add_parser("start", help="start app in debug mode")
    cmd_start.add_argument("--host", default="127.0.0.1", type=str)
    cmd_start.add_argument("--port", default=8080, type=int)
    cmd_start.add_argument("--dev", action="store_true")
    cmd_start.add_argument(
        "--proxy-count",
        type=int,
        default=_intenv("PROXY_COUNT", _intenv("PROXIES_X_FORWARDED_FOR", settings.proxy_count)),
    )
    cmd_start.set_defaults(func=handle_start)

    cmd_useradd = subparsers.add_parser("useradd", help="create new user")
    cmd_useradd.add_argument("username")
    cmd_useradd.add_argument("--admin", action="store_true", help="created user should have administrative rights")
    cmd_useradd.set_defaults(func=handle_useradd)

    cmd_userdel = subparsers.add_parser("userdel", help="delete a user")
    cmd_userdel.add_argument("username")
    cmd_userdel.set_defaults(func=handle_userdel)

    cmd_userlist = subparsers.add_parser("userlist", help="list users")
    cmd_userlist.set_defaults(func=handle_userlist)

    cmd_passwd = subparsers.add_parser("passwd", help="change password")
    cmd_passwd.add_argument("username")
    cmd_passwd.set_defaults(func=handle_passwd)

    cmd_scan = subparsers.add_parser("scan", help="scan playlists for changes")
    cmd_scan.set_defaults(func=handle_scan)

    cmd_migrate = subparsers.add_parser("migrate", help="run database migrations")
    cmd_migrate.set_defaults(func=handle_migrate)

    cmd_vacuum = subparsers.add_parser("vacuum", help="issue vacuum command to clean up sqlite databases")
    cmd_vacuum.set_defaults(func=handle_vacuum)

    cmd_sync = subparsers.add_parser("sync", help="sync tracks from main server (offline mode)")
    cmd_sync.add_argument(
        "--force-resync",
        type=float,
        default=0.0,
        help="Ratio of randomly selected tracks to redownload even if up to date",
    )
    cmd_sync.add_argument(
        "--playlists",
        type=str,
        help="Change playlists to sync. Specify playlists as comma separated list without spaces. Enter 'favorite' to sync favorite playlists (default).",
    )
    cmd_sync.set_defaults(func=handle_sync)

    cmd_cover = subparsers.add_parser("debug-cover", help="Download cover image")
    cmd_cover.add_argument("artist")
    cmd_cover.add_argument("title")
    cmd_cover.add_argument("--meme", action="store_true")
    cmd_cover.set_defaults(func=handle_cover)

    cmd_cover = subparsers.add_parser("debug-acoustid")
    cmd_cover.add_argument("path")
    cmd_cover.set_defaults(func=handle_acoustid)

    cmd_cover = subparsers.add_parser("debug-lyrics")
    cmd_cover.add_argument("--title", required=True)
    cmd_cover.add_argument("--artist", required=True)
    cmd_cover.add_argument("--album")
    cmd_cover.add_argument("--duration", type=int)
    cmd_cover.set_defaults(func=handle_lyrics)

    cmd_cover = subparsers.add_parser("debug-bing")
    cmd_cover.add_argument("query")
    cmd_cover.set_defaults(func=handle_bing)

    args = parser.parse_args()

    settings.log_level = args.log_level
    settings.log_short = args.short_log_format
    settings.data_dir = Path(args.data_dir).absolute()
    assert settings.data_dir.exists(), "data dir does not exist: " + settings.data_dir.as_posix()
    if args.ffmpeg_log_level:
        settings.ffmpeg_log_level = args.ffmpeg_log_level
    if args.track_max_duration_seconds:
        settings.track_max_duration_seconds = args.track_max_duration_seconds
    settings.radio_playlists = split_by_comma(args.radio_playlists)
    settings.lastfm_api_key = args.lastfm_api_key
    settings.lastfm_api_secret = args.lastfm_api_secret
    settings.spotify_api_id = args.spotify_api_id
    settings.spotify_api_secret = args.spotify_api_secret
    settings.offline_mode = args.offline
    if args.news_server:
        settings.news_server = args.news_server

    settings.log_warnings_to_file = True
    logconfig.apply()

    if settings.offline_mode:
        settings.music_dir = Path("/dev/null")
    else:
        if not args.music_dir:
            log.error("music dir must be set when not running in offline mode")
            sys.exit(1)
        settings.music_dir = Path(args.music_dir).resolve()
        if not settings.music_dir.exists():
            log.error("music dir does not exist: " + settings.music_dir.resolve().as_posix())
            sys.exit(1)

    log.info("music=%s data=%s", settings.music_dir.as_posix(), settings.data_dir.as_posix())

    if isinstance(aw := args.func(args), Coroutine):
        asyncio.run(aw)


if __name__ == "__main__":
    main()
