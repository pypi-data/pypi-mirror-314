from aiohttp import web

from raphson_mp import packer, settings
from raphson_mp.decorators import Route, simple_route


@simple_route("/js/player.js")
async def route_player_js(_request: web.Request):
    return web.Response(body=packer.pack(settings.static_dir / "js" / "player"), content_type="application/javascript")


static = Route(web.static("/", settings.static_dir))
