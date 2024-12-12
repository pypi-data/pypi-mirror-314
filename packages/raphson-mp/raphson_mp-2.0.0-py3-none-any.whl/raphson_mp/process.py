import asyncio
import logging
from typing import cast

_LOGGER = logging.getLogger(__name__)


class ProcessStatusError(Exception):
    pass


async def _write(process: asyncio.subprocess.Process, data: bytes | None):
    if data is not None:
        stdin = cast(asyncio.StreamWriter, process.stdin)
        try:
            stdin.write(data)
            await stdin.drain()
        except ConnectionResetError:
            pass
        stdin.close()


async def run(*command: str, input: bytes | None = None) -> None:
    _LOGGER.info("running subprocess: %s", command)
    process = await asyncio.subprocess.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE if input is not None else None,
    )

    status, _none = await asyncio.gather(process.wait(), _write(process, input))

    if status != 0:
        raise ProcessStatusError("Process ended with status code " + str(status))


async def run_output(*command: str, input: bytes | None = None) -> tuple[bytes, bytes]:
    _LOGGER.info("running subprocess: %s", command)
    process = await asyncio.subprocess.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE if input is not None else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr, status, _none = await asyncio.gather(
        cast(asyncio.StreamReader, process.stdout).read(),
        cast(asyncio.StreamReader, process.stderr).read(),
        process.wait(),
        _write(process, input),
    )

    if status != 0:
        raise ProcessStatusError("Process ended with status code " + str(status))

    return stdout, stderr
