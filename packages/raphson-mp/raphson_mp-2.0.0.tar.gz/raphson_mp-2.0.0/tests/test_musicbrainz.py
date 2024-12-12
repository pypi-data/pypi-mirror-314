import asyncio

from raphson_mp import musicbrainz


async def test_correct_release():
    await asyncio.sleep(1)  # avoid rate limit
    rg_id = await musicbrainz._search_release_group("Red Hot Chili Peppers", "Californication")
    # should find album, not single
    assert rg_id == "ca5dfcc3-83fb-3eee-9061-c27296b77b2c"


async def test_cover():
    await asyncio.sleep(1)  # avoid rate limit
    cover = await musicbrainz.get_cover("SebastiAn", "Dancing By Night")
    assert cover
    assert len(cover) > 400000


async def test_metadata():
    await asyncio.sleep(1)  # avoid rate limit
    metas = musicbrainz.get_recording_metadata("a8fe7228-18fc-40d9-80c6-cbfb71d5d03e")
    async for meta in metas:
        assert meta.album in {"The Remixes", "Dancing By Night"}
        assert meta.year == 2023
        assert "London Grammar" in meta.artists
        assert "SebastiAn" in meta.artists
