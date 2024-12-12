from collections.abc import Awaitable
from dataclasses import dataclass
import logging
from sqlite3 import Connection
from typing import Callable

from aiohttp import web
from aiohttp.typedefs import Handler

from raphson_mp import auth, i18n
from raphson_mp.vars import APP_JINJA_ENV, CONN, JINJA_ENV, LOCALE, USER

PublicRouteCallable = Callable[[web.Request, Connection], Awaitable[web.StreamResponse]]
AuthRouteCallable = Callable[[web.Request, Connection, auth.User], Awaitable[web.StreamResponse]]
RouteCallable = PublicRouteCallable | AuthRouteCallable


_LOGGER = logging.getLogger(__name__)


@dataclass
class Route:
    routedef: web.AbstractRouteDef


def route(
    path: str,
    method: str = "GET",
    public: bool = False,
    require_admin: bool = False,
    skip_csrf_check: bool = False,
    redirect_to_login: bool = False,
) -> Callable[[RouteCallable], Route]:
    assert not (public and require_admin), "cannot be public if admin is required"

    def decorator(func: RouteCallable) -> Route:
        async def handler(request: web.Request) -> web.StreamResponse:
            conn = request.config_dict[CONN]
            JINJA_ENV.set(request.config_dict[APP_JINJA_ENV])
            USER.set(None)
            LOCALE.set(i18n.locale_from_request(request))

            if public:
                return await func(request, conn)  # pyright: ignore[reportCallIssue]

            require_csrf = not skip_csrf_check and request.method == "POST"
            user = await auth.verify_auth_cookie(
                request,
                conn,
                require_admin=require_admin,
                require_csrf=require_csrf,
                redirect_to_login=redirect_to_login,
            )
            USER.set(user)
            LOCALE.set(i18n.locale_from_request(request))
            return await func(request, conn, user)  # pyright: ignore[reportCallIssue]

        return Route(web.route(method, path, handler))

    return decorator


def simple_route(
    path: str,
    method: str = "GET",
) -> Callable[[Handler], Route]:
    def decorator(handler: Handler) -> Route:
        return Route(web.route(method, path, handler))
    return decorator
