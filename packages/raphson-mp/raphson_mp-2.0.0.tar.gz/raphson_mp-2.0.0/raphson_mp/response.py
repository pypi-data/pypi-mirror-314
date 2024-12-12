# allow only one template to render at a time
import asyncio
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from aiohttp import web

from raphson_mp.vars import JINJA_ENV, USER
from raphson_mp.util import AsyncQueueIO

# template_lock = asyncio.Lock()


async def template(template_name: str, *args: Any, **kwargs: Any) -> web.Response:
    template = JINJA_ENV.get().get_or_select_template(template_name)
    html_str = template.generate_async(*args, user=USER.get(), **kwargs)

    async def encoder():
        async for part in html_str:
            yield part.encode()

    return web.Response(body=encoder(), status=200, content_type="text/html")


def _directory_as_zip(queue_io: AsyncQueueIO, path: Path):
    try:
        with ZipFile(queue_io, "w") as zf:
            for subpath in path.glob("**/*"):
                zf.write(subpath, arcname=subpath.relative_to(path))
    finally:
        queue_io.close()


def directory_as_zip(path: Path) -> web.Response:
    if not path.is_dir():
        raise NotADirectoryError(path)
    queue_io = AsyncQueueIO()
    asyncio.create_task(asyncio.to_thread(_directory_as_zip, queue_io, path))
    return web.Response(
        body=queue_io.iterator(),
        content_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{path.name}.zip"'},
    )


def file_attachment(path: Path) -> web.StreamResponse:
    return web.FileResponse(path, headers={"Content-Disposition": f'attachment; filename="{path.name}"'})
