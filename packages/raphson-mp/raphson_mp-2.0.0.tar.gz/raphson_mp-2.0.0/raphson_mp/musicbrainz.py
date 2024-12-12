import asyncio
import logging
import re
import traceback
from collections.abc import AsyncIterator
from dataclasses import dataclass

import aiohttp

from raphson_mp import settings

if settings.offline_mode:
    # Module must not be imported to ensure no data is ever downloaded in offline mode.
    raise RuntimeError("Cannot use musicbrainz in offline mode")


log = logging.getLogger(__name__)


# https://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Escaping_Special_Characters
# https://github.com/alastair/python-musicbrainzngs/blob/1638c6271e0beb9560243c2123d354461ec9f842/musicbrainzngs/musicbrainz.py#L27
LUCENE_SPECIAL = re.compile(r'([+\-&|!(){}\[\]\^"~*?:\\\/])')


def lucene_escape(text: str) -> str:
    """Escape string for MB"""
    return re.sub(LUCENE_SPECIAL, r"\\\1", text)


def _mb_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(
        "https://musicbrainz.org/ws/2/",
        headers={"User-Agent": settings.user_agent},
        raise_for_status=True,
    )


def _caa_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(
        "https://coverartarchive.org",
        headers={"User-Agent": settings.user_agent},
        raise_for_status=True,
    )


async def _get_release_group_cover(release_group: str) -> bytes | None:
    url = f"/release-group/{release_group}/front-1200"
    log.info("downloading from CAA: %s", url)
    async with _caa_session() as session:
        async with session.get(
            url, allow_redirects=True, raise_for_status=False
        ) as response:
            if response.status == 404:
                log.info("release group has no image")
                return None
            response.raise_for_status()
            return await response.content.read()


async def _search_release_group(artist: str, title: str) -> str | None:
    """
    Search for a release group id using the provided search query
    """
    for query in [
        f'artist:"{lucene_escape(artist)}" AND releasegroup:"{lucene_escape(title)}" AND primarytype:Album',
        f'artist:"{lucene_escape(artist)}" AND releasegroup:"{lucene_escape(title)}"',
    ]:
        log.info("Performing MB search for query: %s", query)
        async with _mb_session() as session:
            async with session.get(
                "release-group", params={"query": query, "limit": "1", "fmt": "json"}
            ) as response:
                result = await response.json()
        groups = result["release-groups"]
        if groups:
            group = groups[0]
            log.info(
                "Found release group: %s: %s (%s)",
                group["id"],
                group["title"],
                group["primary-type"],
            )
            return group["id"]

        await asyncio.sleep(1)  # avoid rate limit

    log.info("No release group found")
    return None


async def get_cover(artist: str, album: str) -> bytes | None:
    """
    Get album cover for the given artist and album
    Returns: Image bytes, or None of no album cover was found.
    """
    try:
        release_group = await _search_release_group(artist, album)
        if release_group is None:
            return None

        image_bytes = await _get_release_group_cover(release_group)
        if image_bytes is None:
            return None

        return image_bytes
    except Exception as ex:
        log.info("Error retrieving album art from musicbrainz: %s", ex)
        traceback.print_exc()
        return None


@dataclass
class MBMeta:
    id: str
    title: str
    album: str
    artists: list[str]
    album_artist: str
    year: int | None
    release_type: str
    packaging: str


async def get_recording_metadata(recording_id: str) -> AsyncIterator[MBMeta]:
    async with _mb_session() as session:
        async with session.get(
            "recording/" + recording_id,
            params={"inc": "artists+releases+release-groups", "fmt": "json"},
            raise_for_status=False,
        ) as response:
            if response.status == 404:
                log.warning("got 404 for recording %s", recording_id)
                return
            response.raise_for_status()
            result = await response.json()

    title = result["title"]
    artists = [artist["name"] for artist in result["artist-credit"]]

    for release in result["releases"]:
        if "Compilation" in release["release-group"]["secondary-types"]:
            log.info("ignoring compilation release: %s", release["id"])
            continue

        release_type = release["release-group"]["primary-type"]

        album = release["title"]

        # Ideally we'd get the correct artist from the release group, but that would require many API requests.
        album_artist = artists[0]

        if "date" in release and len(release["date"]) >= 4:
            year = int(release["date"][:4])
        else:
            year = None

        packaging = release["packaging"]
        if packaging is None or packaging == "None":
            packaging = "Digital"

        yield MBMeta(
            release["id"],
            title,
            album,
            artists,
            album_artist,
            year,
            release_type,
            packaging,
        )
