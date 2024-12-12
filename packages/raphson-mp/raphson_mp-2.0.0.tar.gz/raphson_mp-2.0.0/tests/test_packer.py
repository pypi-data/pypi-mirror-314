import os
import random
from pathlib import Path
from tempfile import TemporaryDirectory

from raphson_mp import packer


def test_packer():
    with TemporaryDirectory() as tempdir:
        a = os.urandom(random.randint(0, 1000))
        b = os.urandom(random.randint(0, 1000))
        Path(tempdir, 'a').write_bytes(a)
        Path(tempdir, 'b').write_bytes(b)
        result = packer.pack(Path(tempdir))
        assert result == a + b
