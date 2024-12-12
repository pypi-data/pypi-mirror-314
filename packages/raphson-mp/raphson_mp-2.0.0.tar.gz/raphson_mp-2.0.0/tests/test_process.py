import asyncio
import pytest

from raphson_mp import process


async def test_run():
    await asyncio.gather(*[process.run("true", input=b"a") for i in range(100)])

    with pytest.raises(process.ProcessStatusError):
        await process.run("false")


async def test_output():
    stdout, stderr = await process.run_output("cat", input=b"hello")
    assert stdout == b"hello"
    assert stderr == b""

    with pytest.raises(process.ProcessStatusError):
        await process.run_output("python3", "--WRONGFLAG")

    stdout, stderr = await process.run_output("ffmpeg", "--help")
    assert stdout.startswith(b"Universal media converter")
    assert stderr.startswith(b"ffmpeg version")
