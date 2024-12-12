import asyncio
import os
import pickle
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from raphson_music_client import RaphsonMusicClient
from raphson_music_client.track import Track


@dataclass
class Settings:
    server: str
    token: str

    def save(self, path: Path) -> None:
        with path.open('wb') as fp:
            return pickle.dump(self, fp)

    @classmethod
    def load(cls, path: Path) -> 'Settings':
        with path.open('rb') as fp:
            return pickle.load(fp)

class Downloader:
    client: RaphsonMusicClient

    def __init__(self):
        self.client = RaphsonMusicClient()

    async def setup(self, settings: Settings):
        await self.client.setup(base_url=settings.server, token=settings.token, user_agent='Downloader')

    async def download_track(self, track: Track, local_path: Path):
        local_path.write_bytes(await track.download_mp3())

    async def download_playlist(self, playlist_name: str):
        tracks = await self.client.list_tracks(playlist_name)
        playlist_path = Path(playlist_name).resolve()
        all_local_paths: set[str] = set()

        for track in tracks:
            local_path = Path(track.path + '.mp3').resolve()
            all_local_paths.add(local_path.as_posix())
            # don't allow directory traversal by server
            if not local_path.resolve().is_relative_to(playlist_path):
                raise RuntimeError(f'Path: {track.path} not relative to {playlist_path}')

            if local_path.exists():
                mtime = int(local_path.stat().st_mtime)
                if mtime != track.mtime:
                    print('Out of date: ' + track.path)
                else:
                    print('OK: ' + track.path)
                    continue
            else:
                print('Missing: ' + track.path)
                local_path.parent.mkdir(exist_ok=True)

            await self.download_track( track, local_path)
            os.utime(local_path, (time.time(), track.mtime))

        # Prune deleted tracks
        for track_path in playlist_path.glob('**/*'):
            if track_path.resolve().as_posix() not in all_local_paths:
                print('Delete: ' + track_path.resolve().as_posix())
                track_path.unlink()


async def main():
    state_path = Path('download-state.json')

    if state_path.is_file():
        settings = Settings.load(state_path)
    else:
        print('Not configured, please log in')
        server = input('Server URL: ').rstrip('/')
        token = input('Token: ')
        settings = Settings(server, token)
        settings.save(state_path)

    downloader = Downloader()
    try:
        await downloader.setup(settings)
        await downloader.download_playlist(sys.argv[1])
    finally:
        await downloader.client.close()

if __name__ == '__main__':
    asyncio.run(main())
