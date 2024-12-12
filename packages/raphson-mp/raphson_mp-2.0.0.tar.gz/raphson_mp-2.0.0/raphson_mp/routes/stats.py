import asyncio
from sqlite3 import Connection

from aiohttp import web

from raphson_mp import charts
from raphson_mp.auth import User
from raphson_mp.charts import StatsPeriod
from raphson_mp.decorators import route
from raphson_mp.response import template


@route("", redirect_to_login=True)
async def route_stats(_request: web.Request, _conn: Connection, _user: User):
    return await template("stats.jinja2")


@route("/data")
async def route_stats_data(request: web.Request, _conn: Connection, _user: User):
    period = StatsPeriod.from_str(request.query["period"])
    data = await asyncio.to_thread(charts.get_data, period)
    return web.json_response(data)
