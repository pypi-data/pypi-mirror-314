import logging
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass

import aiohttp

from raphson_mp import settings
from raphson_mp.util import urlencode

log = logging.getLogger(__name__)


@dataclass
class SpotifyTrack:
    title: str
    artists: list[str]

    @property
    def display(self) -> str:
        return ", ".join(self.artists) + " - " + self.title


class SpotifyClient:

    _access_token: str | None = None
    _access_token_expiry: int = 0

    async def get_access_token(self) -> str:
        if self._access_token is not None:
            if self._access_token_expiry > int(time.time()):
                return self._access_token

        async with aiohttp.ClientSession(headers={"User-Agent": settings.user_agent}, raise_for_status=True) as session:
            async with session.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.spotify_api_id,
                    "client_secret": settings.spotify_api_secret,
                },
            ) as response:
                json = await response.json()

        access_token: str = json["access_token"]
        self._access_token = access_token
        self._access_token_expiry = int(time.time()) + json["expires_in"]
        return access_token

    async def get_playlist(self, playlist_id: str) -> AsyncIterator[SpotifyTrack]:
        url = "https://api.spotify.com/v1/playlists/" + urlencode(playlist_id) + "/tracks"

        access_token = await self.get_access_token()

        async with aiohttp.ClientSession(
            headers={
                "User-Agent": settings.user_agent,
                "Authorization": "Bearer " + access_token,
            },
            raise_for_status=True,
        ) as session:
            while url:
                log.info("making request to: %s", url)

                async with session.get(url, params={"fields": "next,items(track(name,artists(name)))"}) as response:
                    json = await response.json()

                for track in json["items"]:
                    title = track["track"]["name"]
                    artists = [artist["name"] for artist in track["track"]["artists"]]
                    yield SpotifyTrack(title, artists)

                url = json["next"]
