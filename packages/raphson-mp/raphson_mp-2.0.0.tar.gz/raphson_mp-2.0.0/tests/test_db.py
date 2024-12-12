import shutil
from pathlib import Path
from tempfile import mkdtemp, mktemp
from threading import Thread
import time

from raphson_mp import db, settings


def test_create_database():
    settings.data_dir = Path(mkdtemp())
    try:
        # Test if it completes without errors (e.g. no SQL syntax errors)
        db.migrate()
    finally:
        shutil.rmtree(settings.data_dir)


def test_write_read():
    """
    This tests whether a read-only database connection sees changes made by a
    different connection, without needing to re-open the read-only database connection.
    """
    test_db = mktemp()

    with db._connect(test_db, False, should_exist=False) as conn:  # pyright: ignore[reportPrivateUsage]
        conn.execute("CREATE TABLE test (test TEXT)")

    def reader():
        with db._connect(test_db, True) as conn:  # pyright: ignore[reportPrivateUsage]
            for i in range(10):
                row = conn.execute("SELECT * FROM test").fetchone()
                if row:
                    assert row[0] == "hello"
                    return
                time.sleep(0.5)

        raise ValueError("did not read value")

    thread = Thread(target=reader)
    thread.start()
    time.sleep(1)
    with db._connect(test_db, False) as conn:
        conn.execute('INSERT INTO test VALUES ("hello")')
    thread.join()
