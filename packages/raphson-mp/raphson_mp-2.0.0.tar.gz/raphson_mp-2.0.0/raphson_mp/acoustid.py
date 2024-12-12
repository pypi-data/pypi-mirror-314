import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path

import aiohttp

from raphson_mp import process, settings

if settings.offline_mode:
    # Module must not be imported to ensure no data is ever downloaded in offline mode.
    raise RuntimeError("Cannot use bing in offline mode")


log = logging.getLogger(__name__)


API_KEY = "rTTqI4IrbJ"


@dataclass
class Fingerprint:
    duration: int
    fingerprint_b64: str


async def lookup(fingerprint: Fingerprint) -> AsyncIterator[str]:
    """
    Returns: musicbrainz recording id
    """
    async with aiohttp.ClientSession(
        "https://api.acoustid.org/v2/", headers={"User-Agent": settings.user_agent}, raise_for_status=True
    ) as session:
        async with session.get(
            "lookup",
            params={
                "format": "json",
                "client": API_KEY,
                "duration": fingerprint.duration,
                "fingerprint": fingerprint.fingerprint_b64,
                "meta": "recordingids",
            },
        ) as response:
            json = await response.json()

    for result in json["results"]:
        if "recordings" in result:
            for recording in result["recordings"]:
                yield recording["id"]


async def get_fingerprint(path: Path):
    stdout, _stderr = await process.run_output("fpcalc", path.absolute().as_posix())

    split = stdout.splitlines()

    assert split[0].startswith(b"DURATION=")
    duration = int(split[0][9:].decode())

    assert split[1].startswith(b"FINGERPRINT=")
    fingerprint = split[1][12:].decode()

    return Fingerprint(duration, fingerprint)
