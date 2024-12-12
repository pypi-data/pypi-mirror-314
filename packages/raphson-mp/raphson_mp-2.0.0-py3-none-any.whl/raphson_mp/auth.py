from __future__ import annotations
import asyncio
import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from sqlite3 import Connection, OperationalError
from typing import cast, override

from aiohttp import web

from raphson_mp import db, i18n, settings, theme

log = logging.getLogger(__name__)


def _hash_password(password: str):
    # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#scrypt
    salt_bytes = os.urandom(32)
    n = 2**14
    r = 8
    p = 5
    hash_bytes = hashlib.scrypt(password.encode(), salt=salt_bytes, n=n, r=r, p=p)
    return json.dumps(
        {
            "alg": "scrypt",
            "n": n,
            "r": r,
            "p": p,
            "salt": base64.b64encode(salt_bytes).decode(),
            "hash": base64.b64encode(hash_bytes).decode(),
        }
    )


def _verify_hash(hashed_password: str, password: str):
    hash_json = json.loads(hashed_password)
    if hash_json["alg"] == "scrypt":
        hash_bytes = hashlib.scrypt(
            password.encode(),
            salt=base64.b64decode(hash_json["salt"]),
            n=hash_json["n"],
            r=hash_json["r"],
            p=hash_json["p"],
        )
        return hmac.compare_digest(hash_bytes, base64.b64decode(hash_json["hash"]))

    raise ValueError("unsupported alg", hash_json)


async def verify_password(conn: Connection, user_id: int, password: str) -> bool:
    (hashed_password,) = conn.execute("SELECT password FROM user WHERE id = ?", (user_id,)).fetchone()

    def _verify_password():
        # Upgrade implemented 2024-08-26
        # TODO In a year, remove upgrade code and do not allow users to log in with bcrypt hashed password
        # The server administrator will have to give them a new password
        if hashed_password.startswith("$2b"):
            # Legacy bcrypt password
            log.warning("Upgrading legacy bcrypt password")
            import bcrypt  # only import bcrypt when actually required

            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                # Password is valid, update to modern hash
                new_hash = _hash_password(password)
                conn.execute("UPDATE user SET password = ? WHERE id = ?", (new_hash, user_id))
                return True
            else:
                return False

        return _verify_hash(hashed_password, password)

    return await asyncio.to_thread(_verify_password)


@dataclass
class Session:
    user_id: int
    token: str
    csrf_token: str
    creation_timestamp: int
    user_agent: str | None
    remote_address: str | None
    last_use: int

    @property
    def creation_date(self) -> str:
        """
        When session was created, formatted as time ago string
        """
        seconds_ago = self.creation_timestamp - int(time.time())
        return i18n.format_timedelta(seconds_ago, add_direction=True)

    @property
    def last_use_ago(self) -> str:
        """
        When account was last used, formatted as time ago string
        """
        seconds_ago = self.last_use - int(time.time())
        return i18n.format_timedelta(seconds_ago, add_direction=True)

    @property
    def last_device(self) -> str | None:
        """
        Last device string, based on user agent string
        """
        if self.user_agent is None:
            return "?"

        if "Music-Player-Android" in self.user_agent:
            return "Raphson Music Player, Android"

        if "raphson-music-player" in self.user_agent:
            return "Raphson Music Player"

        # old versions
        if "DanielKoomen/WebApp" in self.user_agent:
            return "Raphson Music Player"

        if self.user_agent == "rmp-playback-server":
            return "Raphson playback server"

        if "Werkzeug" in self.user_agent:
            return "Flask test client"

        browsers = ["Firefox", "Chromium", "Chrome", "Vivaldi", "Opera", "Safari"]
        systems = ["Windows", "macOS", "Android", "iOS", "Ubuntu", "Debian", "Fedora", "Linux"]

        for maybe_browser in browsers:
            if maybe_browser in self.user_agent:
                browser = maybe_browser
                break
        else:
            browser = "?"

        for maybe_system in systems:
            if maybe_system in self.user_agent:
                system = maybe_system
                break
        else:
            system = "?"

        return f"{browser}, {system}"

    def set_cookie(self, response: web.Response):
        response.set_cookie("token", self.token, max_age=3600 * 24 * 30, samesite="Strict")


class PrivacyOption(Enum):
    NONE = None
    AGGREGATE = "aggregate"
    HIDDEN = "hidden"


class User(ABC):
    user_id: int
    username: str
    nickname: str | None
    admin: bool
    primary_playlist: str | None
    language: str | None
    privacy: PrivacyOption
    theme: str

    # TODO make it a property
    @property
    @abstractmethod
    def csrf(self) -> str:
        """Get CSRF token for current session"""

    @abstractmethod
    def sessions(self) -> list[Session]:
        """Get all user sessions"""

    @abstractmethod
    async def update_password(self, new_password: str) -> None:
        """Change user password and delete all existing sessions."""

    @abstractmethod
    async def update_username(self, new_username: str) -> None:
        """Change username"""

    @staticmethod
    def get(conn: Connection, *, session: Session | None = None, user_id: int | None = None) -> User:
        if session is not None and user_id is None:
            real_user_id = session.user_id
        elif session is None and user_id is not None:
            real_user_id = user_id
        else:
            raise ValueError("either session or user_id must be provided")

        assert isinstance(real_user_id, int)

        if settings.offline_mode:
            assert real_user_id == 0
            return OFFLINE_DUMMY_USER
        else:
            username, nickname, admin, primary_playlist, language, privacy, theme = conn.execute(
                "SELECT username, nickname, admin, primary_playlist, language, privacy, theme FROM user WHERE id = ?",
                (real_user_id,),
            ).fetchone()
            return StandardUser(conn, session, real_user_id, username, nickname, admin == 1, primary_playlist, language, PrivacyOption(privacy), theme)

    @staticmethod
    async def create(username: str, password: str, admin: bool = False):
        assert not settings.offline_mode
        def thread():
            hashed_password = _hash_password(password)
            with db.connect() as writable_conn:
                writable_conn.execute("INSERT INTO user (username, password, admin) VALUES (?, ?, ?)", (username, hashed_password, admin))
        await asyncio.to_thread(thread)

@dataclass
class StandardUser(User):
    conn: Connection
    session: Session | None
    user_id: int
    username: str
    nickname: str | None
    admin: bool
    primary_playlist: str | None
    language: str | None
    privacy: PrivacyOption
    theme: str

    @override
    def sessions(self) -> list[Session]:
        results = self.conn.execute(
            """
            SELECT user, token, csrf_token, creation_date, user_agent, remote_address, last_use
            FROM session WHERE user=?
            """,
            (self.user_id,),
        ).fetchall()
        return [Session(*row) for row in results]

    @property
    @override
    def csrf(self) -> str:
        if not self.session:
            raise ValueError("No session is known for this user")
        return self.session.csrf_token

    @override
    async def update_password(self, new_password: str) -> None:

        def thread():
            password_hash = _hash_password(new_password)
            with db.connect() as conn:
                conn.execute("UPDATE user SET password=? WHERE id=?", (password_hash, self.user_id))
                conn.execute("DELETE FROM session WHERE user=?", (self.user_id,))

        await asyncio.to_thread(thread)

    @override
    async def update_username(self, new_username: str) -> None:
        def thread():
            with db.connect() as conn:
                conn.execute("UPDATE user SET username=? WHERE id=?", (new_username, self.user_id))

        await asyncio.to_thread(thread)


class OfflineUser(User):
    def __init__(self) -> None:
        self.user_id: int = 0
        self.username: str = "offline_user"
        self.nickname: str | None = None
        self.admin: bool = False
        self.primary_playlist: str | None = None
        self.language: str | None = None
        self.privacy: PrivacyOption = PrivacyOption.NONE
        self.theme: str = theme.DEFAULT_THEME
        self._csrf: str = secrets.token_urlsafe()

    @override
    def sessions(self) -> list[Session]:
        return []

    @property
    @override
    def csrf(self) -> str:
        return self._csrf

    @override
    async def update_password(self, new_password: str) -> None:
        raise NotImplementedError

    @override
    async def update_username(self, new_username: str) -> None:
        raise NotImplementedError


OFFLINE_DUMMY_USER = OfflineUser()


@unique
class AuthErrorReason(Enum):
    NO_TOKEN = 1
    INVALID_TOKEN = 2
    ADMIN_REQUIRED = 3
    MISSING_CSRF = 4
    INVALID_CSRF = 5

    @property
    def message(self):
        """
        Get translated message corresponding to auth error reason
        """
        if self is AuthErrorReason.NO_TOKEN:
            return i18n.gettext("You are not logged in, please log in.")
        elif self is AuthErrorReason.INVALID_TOKEN:
            return i18n.gettext("Your current session is invalid, please log in again.")
        elif self is AuthErrorReason.ADMIN_REQUIRED:
            return i18n.gettext("Your are not an administrator, but this page requires administrative privileges")
        elif self is AuthErrorReason.MISSING_CSRF:
            return i18n.gettext("Missing CSRF token from request.")
        elif self is AuthErrorReason.INVALID_CSRF:
            return i18n.gettext("Invalid CSRF token in request. Please refresh the page and try again.")

        return ValueError()


@dataclass
class AuthError(Exception):
    reason: AuthErrorReason
    redirect: bool


async def create_session(request: web.Request, user: int | User) -> Session:
    user_id = user if isinstance(user, int) else user.user_id
    token = secrets.token_urlsafe()
    csrf_token = secrets.token_urlsafe()
    remote_addr = request.remote
    user_agent = request.headers.get("User-Agent")

    def thread():
        with db.connect() as conn:
            conn.execute(
                """
                INSERT INTO session (user, token, csrf_token, creation_date, user_agent, remote_address, last_use)
                VALUES (?, ?, ?, unixepoch(), ?, ?, unixepoch())
                """,
                (user_id, token, csrf_token, user_agent, remote_addr),
            )
    await asyncio.to_thread(thread)

    return Session(user_id, token, csrf_token, int(time.time()), None, None, int(time.time()))


async def log_in(request: web.Request, conn: Connection, username: str, password: str) -> Session | None:
    """
    Log in using username and password.
    Args:
        conn: Read-write database connection
        username
        password
        user_agent
        remote_addr
    Returns: Session token, or None if the username+password combination is not valid
    """
    if settings.offline_mode:
        raise RuntimeError("Login not available in offline mode")

    result = conn.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone()

    if result is None:
        log.warning("Login attempt with non-existent username: '%s'", username)
        return None

    (user_id,) = result

    if not await verify_password(conn, user_id, password):
        log.warning("Failed login for user %s", username)
        return None

    session = await create_session(request, user_id)
    log.info("Successful login for user %s", username)
    return session


def _verify_token(request: web.Request, conn: Connection, token: str) -> Session | None:
    """
    Verify session token, and return corresponding user
    Args:
        conn: Read-only database connection
        token: Session token to verify
    Returns: User object if session token is valid, or None if invalid
    """
    result = conn.execute(
        """
        SELECT user, token, csrf_token, creation_date, user_agent, remote_address, last_use
        FROM session
        WHERE token=?
        """,
        (token,),
    ).fetchone()

    if result is None:
        log.warning("Invalid auth token: %s", token)
        return None

    session = Session(*result)

    try:
        remote_addr = request.remote
        user_agent = request.headers.get("User-Agent")
        conn.execute(
            """
                     UPDATE session
                     SET user_agent=?, remote_address=?, last_use=unixepoch()
                     WHERE token=?
                     """,
            (user_agent, remote_addr, session.token),
        )
    except OperationalError as ex:
        # Ignore error if database is read-only
        if ex.sqlite_errorname != "SQLITE_READONLY":
            raise ex

    return session


async def verify_auth_cookie(
    request: web.Request,
    conn: Connection,
    require_admin: bool = False,
    redirect_to_login: bool = False,
    require_csrf: bool = False,
) -> User:
    """
    Verify auth token sent as cookie, raising AuthError if missing or not valid.
    Args:
        conn: Read-only database connection
        require_admin: Whether logging in as a non-admin account should be treated as an authentication failure
        redirect_to_login: Whether the user should sent a redirect if authentication failed, instead
                           of showing a 403 page. Should be set to True for pages, and to False for API endpoints.
    """
    if settings.offline_mode:
        return OFFLINE_DUMMY_USER

    if (auth_header := request.headers.get("Authorization")) and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer ") :]
        require_csrf = False  # CSRF is only an issue with cookies
    elif "token" in request.cookies:
        token = request.cookies["token"]
    else:
        log.warning("No auth token")
        raise AuthError(AuthErrorReason.NO_TOKEN, redirect_to_login)

    session = _verify_token(request, conn, token)
    if session is None:
        raise AuthError(AuthErrorReason.INVALID_TOKEN, redirect_to_login)

    if require_csrf:
        if request.content_type == "application/json":
            csrf_token = cast(str, (await request.json())["csrf"])
        elif request.content_type == "application/x-www-form-urlencoded" or (
            request.content_type and request.content_type.startswith("multipart/form-data")
        ):
            csrf_token = cast(str, (await request.post())["csrf"])
        else:
            raise AuthError(AuthErrorReason.MISSING_CSRF, False)

        if not hmac.compare_digest(csrf_token, session.csrf_token):
            raise AuthError(AuthErrorReason.INVALID_CSRF, False)

    user = User.get(conn, session=session)

    if require_admin and not user.admin:
        raise AuthError(AuthErrorReason.ADMIN_REQUIRED, redirect_to_login)

    return user


def prune_old_session_tokens(conn: Connection) -> int:
    """
    Prune old session tokens
    Args:
        conn: Read-write database connection
    Returns: Number of deleted tokens
    """
    one_month_ago = int(time.time()) - 60 * 60 * 24 * 30
    return conn.execute("DELETE FROM session WHERE last_use < ?", (one_month_ago,)).rowcount
