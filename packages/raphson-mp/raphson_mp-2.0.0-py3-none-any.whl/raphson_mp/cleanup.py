import asyncio
import logging
import time

from raphson_mp import auth, db, music, settings

log = logging.getLogger(__name__)


def delete_old_trashed_files() -> int:
    """
    Delete trashed files after 30 days.
    """
    count = 0
    for path in music.list_tracks_recursively(settings.music_dir, trashed=True):
        if path.stat().st_ctime < time.time() - 60 * 60 * 24 * 30:
            log.info("Permanently deleting: %s", path.absolute().as_posix())
            path.unlink()
            count += 1
    return count


async def cleanup() -> None:
    """
    Invokes other cleanup functions
    """
    def thread():
        with db.connect() as conn:
            count = auth.prune_old_session_tokens(conn)
            log.info("Deleted %s session tokens", count)

        count = delete_old_trashed_files()
        log.info("Deleted %s trashed files", count)

    await asyncio.to_thread(thread)
