import logging
import sys

from aiohttp import web
from aiohttp.typedefs import Handler
from multidict import CIMultiDictProxy

from raphson_mp import auth, response, settings


_LOGGER = logging.getLogger(__name__)


@web.middleware
async def auth_error(request: web.Request, handler: Handler):
    """
    Display permission denied error page with reason, or redirect to login page
    """
    try:
        return await handler(request)
    except auth.AuthError as err:
        if err.redirect:
            raise web.HTTPSeeOther("/auth/login")
        resp = await response.template("403.jinja2", reason=err.reason.message)
        resp.set_status(403)
        return resp


@web.middleware
async def unhandled_error(request: web.Request, handler: Handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        raise ex
    except Exception as ex:
        _LOGGER.error("Unhandled exception: %s", str(ex), exc_info=True)
        raise web.HTTPInternalServerError(
            text="Sorry! Cannot continue due to an unhandled exception. The error has been logged. Please contact the server administrator."
        )


@web.middleware
async def profiler(request: web.Request, handler: Handler):
    import yappi  # pyright: ignore[reportMissingTypeStubs]

    columns = {0: ("name", 50), 1: ("ncall", 5), 2: ("tsub", 8), 3: ("ttot", 8), 4: ("tavg", 8)}

    print("test")

    yappi.set_clock_type("cpu")  # pyright: ignore[reportUnknownMemberType]
    yappi.start()
    try:
        return await handler(request)
    finally:
        func_stats = yappi.get_func_stats().sort("ttot")  # pyright: ignore[reportUnknownMemberType]
        func_stats._print_header(sys.stdout, columns)  # pyright: ignore[reportUnknownMemberType,reportPrivateUsage]
        for i, stat in enumerate(func_stats):  # pyright: ignore[reportUnknownVariableType]
            stat._print(sys.stdout, columns)  # pyright: ignore[reportUnknownMemberType]
            if i > 10:
                break
        yappi.stop()


"""
proxy_fix middleware based on https://github.com/pgjones/hypercorn/blob/main/src/hypercorn/middleware/proxy_fix.py

Copyright P G Jones 2018.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


@web.middleware
async def proxy_fix(request: web.Request, handler: Handler):
    if settings.proxy_count > 0:
        client: str | None = None
        headers = request.headers
        if (value := _get_trusted_value("forwarded", headers)) is not None:
            for part in value.split(";"):
                if part.startswith("for="):
                    client = part[4:].strip()

        if client is None:
            client = _get_trusted_value("x-forwarded-for", headers)

        if client is not None:
            request = request.clone(remote=client)

    return await handler(request)


def _get_trusted_value(name: str, headers: CIMultiDictProxy[str]) -> str | None:
    trusted_hops = settings.proxy_count
    values: list[str] = []
    for header_name, header_value in headers.items():
        if header_name.lower() == name:
            values.extend([value.strip() for value in header_value.split(",")])

    if len(values) >= trusted_hops:
        return values[-trusted_hops]

    return None
