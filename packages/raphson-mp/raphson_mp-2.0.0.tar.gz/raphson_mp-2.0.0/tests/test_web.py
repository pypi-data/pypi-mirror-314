import random
import secrets
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, cast

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from raphson_mp import auth, db, logconfig, settings, theme
from raphson_mp.server import Server
from raphson_mp.util import urlencode

T_client = TestClient[web.Request, web.Application]

TEST_USERNAME: str = "autotest"
TEST_PASSWORD: str = secrets.token_urlsafe()


def setup_module(module):
    settings.data_dir = Path("./data").resolve()
    settings.music_dir = Path("./music").resolve()
    logconfig.apply_debug()


@pytest.fixture()
async def client() -> AsyncIterator[T_client]:

    server = Server(False)
    test_server = TestServer(server.app)
    await test_server.start_server()
    client = TestClient(test_server)
    async with client.post(
        "/auth/login", data={"username": TEST_USERNAME, "password": TEST_PASSWORD}, allow_redirects=False
    ) as response:
        assert response.status == 303
    yield client
    await client.close()


async def get_csrf(client: T_client):
    async with client.get("/auth/get_csrf") as response:
        assert response.status == 200, await response.text()
        return (await response.json())["token"]


# --------------- LOGIN --------------- #


async def test_create_user():
    """
    Not an actual test, but ensures a test user exists to be used by later tests
    """
    with db.connect() as conn:
        conn.execute("DELETE FROM user WHERE username = ?", (TEST_USERNAME,))

    await auth.User.create(TEST_USERNAME, TEST_PASSWORD)


async def test_failed_login(client: T_client):
    async with client.post(
        "/auth/login", json={"username": TEST_USERNAME, "password": TEST_PASSWORD + "a"}, allow_redirects=False
    ) as response:
        assert response.status == 403


# --------------- ACCOUNT --------------- #


# def _db_nickname() -> None:
#     with db.connect(read_only=True) as conn:
#         return conn.execute("SELECT nickname FROM user WHERE username=?", (TEST_USERNAME,)).fetchone()[0]


# def test_change_nickname(self):
#     response = self.client.post('/account/change_nickname', data={'nickname': '🐢', 'csrf': self.csrf})
#     assert response.status_code == 303, (response.status_code, response.text)
#     assert self._db_nickname() == '🐢'


def _db_password_hash() -> str:
    with db.connect(read_only=True) as conn:
        return conn.execute("SELECT password FROM user WHERE username=?", (TEST_USERNAME,)).fetchone()[0]


async def test_change_password(client: T_client):
    initial_hash = _db_password_hash()
    csrf = await get_csrf(client)

    # wrong current_password
    async with client.post(
        "/account/change_password",
        data={
            "current_password": TEST_PASSWORD + "a",
            "new_password": "new_password",
            "repeat_new_password": "new_password",
            "csrf": csrf,
        },
    ) as response:
        assert response.status == 400, await response.text()
        assert _db_password_hash() == initial_hash  # password should not have changed

    # correct
    async with client.post(
        "/account/change_password",
        data={
            "current_password": TEST_PASSWORD,
            "new_password": "new_password",
            "repeat_new_password": "new_password",
            "csrf": csrf,
        },
        allow_redirects=False,
    ) as response:
        assert response.status == 303, await response.text()
        assert _db_password_hash() != initial_hash  # password should not have changed

    # restore initial password hash
    with db.connect() as conn:
        conn.execute(
            "UPDATE user SET password = ? WHERE username = ?",
            (
                initial_hash,
                TEST_USERNAME,
            ),
        )


# --------------- AUTH --------------- #


async def test_login_fail(client: T_client):
    async with client.post(
        "/auth/login", json={"username": TEST_USERNAME, "password": secrets.token_urlsafe(random.randint(1, 100))}
    ) as response:
        assert response.status == 403, await response.text()


async def test_login_json(client: T_client):
    async with client.post("/auth/login", json={"username": TEST_USERNAME, "password": TEST_PASSWORD}) as response:
        assert response.status == 200
        token = cast(str, (await response.json())["token"])
        assert len(token) > 10


# --------------- PLAYLIST --------------- #


async def test_playlist_list(client: T_client):
    async with client.get("/playlist/list", raise_for_status=True) as response:
        playlists = await response.json()
        playlist = playlists[0]
        assert type(playlist["name"]) == str, playlist
        assert type(playlist["track_count"]) == int, playlist
        assert type(playlist["favorite"]) == bool, playlist
        assert type(playlist["write"]) == bool, playlist


def _assert_track(track: Any):
    assert isinstance(track["playlist"], str)
    assert isinstance(track["path"], str)
    assert isinstance(track["mtime"], int)
    assert isinstance(track["duration"], int)
    assert isinstance(track["title"], str | None)
    assert isinstance(track["album"], str | None)
    assert isinstance(track["album_artist"], str | None)
    assert isinstance(track["year"], int | None)
    assert isinstance(track["artists"], list)
    assert isinstance(track["tags"], list)
    assert isinstance(track["video"], str | None)
    assert isinstance(track["display"], str)


async def _choose_playlist(client: T_client) -> str:
    async with client.get("/playlist/list", raise_for_status=True) as response:
        playlists = await response.json()
        return random.choice(playlists)["name"]


async def test_user():
    with db.connect(read_only=True) as conn:
        user_id, = conn.execute("SELECT id FROM user WHERE username=?", (TEST_USERNAME,)).fetchone()
        user = auth.User.get(conn, user_id=user_id)
        assert isinstance(user, auth.StandardUser)
        assert user.conn is conn
        assert user.user_id == user_id
        assert user.username == TEST_USERNAME
        assert user.nickname is None
        assert user.admin == False
        assert user.primary_playlist is None
        assert user.language is None
        assert user.privacy is auth.PrivacyOption.NONE
        assert user.theme == theme.DEFAULT_THEME


# this test is at the end, because it takes a while
async def test_choose_track(client: T_client):
    playlist = await _choose_playlist(client)
    async with client.post(
        f"/playlist/{urlencode(playlist)}/choose_track", json={"csrf": await get_csrf(client)}, raise_for_status=True
    ) as response:
        track_info = await response.json()
        _assert_track(track_info)
        relpath = cast(str, track_info["path"])

    async with client.get(f"/track/{urlencode(relpath)}/info", raise_for_status=True) as response:
        track_info_2 = await response.json()
        assert track_info == track_info_2

    for audio_type in ["webm_opus_high", "webm_opus_low", "mp3_with_metadata"]:
        async with client.get(f"/track/{urlencode(relpath)}/audio?type={audio_type}", raise_for_status=True):
            pass
