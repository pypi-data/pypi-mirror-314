import random
import secrets

from raphson_mp import auth


def test_hash():
    password = secrets.token_urlsafe(random.randint(0, 100))
    notpassword = secrets.token_urlsafe(random.randint(0, 100))
    hash = auth._hash_password(password)  # pyright: ignore[reportPrivateUsage]
    assert auth._verify_hash(hash, password)  # pyright: ignore[reportPrivateUsage]
    assert not auth._verify_hash(hash, notpassword)  # pyright: ignore[reportPrivateUsage]
