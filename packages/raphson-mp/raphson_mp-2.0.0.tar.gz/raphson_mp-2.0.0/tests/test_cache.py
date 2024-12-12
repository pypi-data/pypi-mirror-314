import secrets
from pathlib import Path

from raphson_mp import cache, settings


def setup_module(_module: str):
    settings.data_dir = Path('./data')


async def test_retrieve_missing():
    value = await cache.retrieve(secrets.token_urlsafe(30))
    assert value is None


async def test_store_retrieve():
    key = secrets.token_urlsafe(30)
    data = secrets.token_bytes(200)
    await cache.store(key, data, cache.HOUR)
    assert await cache.retrieve(key) == data


async def test_store_retrieve_json():
    key = secrets.token_urlsafe(30)
    data = {"hello": secrets.token_urlsafe(200)}
    await cache.store_json(key, data, cache.HOUR)
    assert await cache.retrieve_json(key) == data
