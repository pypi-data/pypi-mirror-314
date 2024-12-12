# pylint: disable=invalid-name

from importlib.metadata import PackageNotFoundError, version
from os import getenv
from pathlib import Path

try:
    _version = version(__name__.split(".")[0])
except PackageNotFoundError:
    _version = "dev"

# Hardcoded settings
csrf_validity_seconds = 3600
app_dir = Path(__file__).parent.resolve()
static_dir = app_dir / "static"
migration_sql_dir = app_dir / "migrations"
init_sql_dir = app_dir / "sql"
raphson_png = static_dir / "img" / "raphson.png"
user_agent = f"raphson-music-player/{_version} (https://github.com/Derkades/raphson-music-player)"
webscraping_user_agent = getenv(
    "MUSIC_WEBSCRAPING_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
)  # https://useragents.me
loudnorm_filter = "loudnorm=I=-16"
access_log_format = '%a %r %s %Tfs "%{User-Agent}i"'
log_warnings_to_file = False

# User configurable settings
log_level: str = "INFO"
log_short: bool = False
music_dir: Path = None  # pyright: ignore[reportAssignmentType]
data_dir: Path = None  # pyright: ignore[reportAssignmentType]
ffmpeg_log_level: str = "warning"
track_max_duration_seconds: int = 1200
radio_playlists: list[str] = []
lastfm_api_key: str | None = None
lastfm_api_secret: str | None = None
spotify_api_id: str | None = None
spotify_api_secret: str | None = None
offline_mode: bool = False
news_server: str | None = None
proxy_count: int = 0


def ffmpeg_flags():
    return ["-hide_banner", "-nostats", "-loglevel", ffmpeg_log_level]
