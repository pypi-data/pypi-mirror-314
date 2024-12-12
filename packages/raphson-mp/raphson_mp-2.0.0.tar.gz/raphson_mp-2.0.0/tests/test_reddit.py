from raphson_mp import reddit


async def test_search():
    image_url = await reddit.search("test")
    assert image_url
    assert image_url.startswith("https://"), image_url
