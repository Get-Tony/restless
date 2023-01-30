"""SQLite3 database context manager for Restless."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def db_connect(db_file: str | Path | None = None):
    """
    Yield a database connection.

    Args:
        db_file (str | Path | None): database file
            Defaults to ":memory:".
    """
    conn = sqlite3.connect(db_file or ":memory:")
    yield conn
    conn.close()
