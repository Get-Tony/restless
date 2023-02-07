"""SQLite3 database abstraction layer for role."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

import sqlite3
from contextlib import contextmanager
from enum import Enum
from pathlib import Path


class RolesQueries(Enum):
    """SQLite3 Query enumeration."""

    CREATE_ROLES_TABLE = """CREATE TABLE IF NOT EXISTS roles(
        name TEXT NOT NULL UNIQUE,
        directory TEXT NOT NULL UNIQUE,
        repo_url TEXT,
        active INTEGER NOT NULL
    )"""
    INSERT_ROLE = """INSERT INTO roles VALUES(?, ?, ?, ?)"""
    SELECT_ROLE = """SELECT * FROM roles WHERE name = ?"""
    SELECT_REPO_URL = """SELECT * FROM roles WHERE repo_url = ?"""
    SELECT_ROLES = """SELECT * FROM roles"""
    SET_ACTIVE = """UPDATE roles SET active = ? WHERE name = ?"""
    DELETE_ROLE = """DELETE FROM roles WHERE name = ?"""


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


def create_roles_table(db_conn: sqlite3.Connection) -> None:
    """
    Create the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    with db_conn:
        db_conn.execute(RolesQueries.CREATE_ROLES_TABLE.value)


def insert_role(
    db_conn: sqlite3.Connection,
    name: str,
    directory: str | Path,
    repo_url: str | None,
    active: bool = True,
) -> None:
    """
    Insert a role into the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name
        directory (str | Path): role directory
        repo_url (str): role repository URL
        active (bool): role active status
    """
    with db_conn:
        db_conn.execute(
            RolesQueries.INSERT_ROLE.value,
            (name, directory, repo_url or "", active),
        )


def select_role(
    db_conn: sqlite3.Connection, name: str
) -> dict[str, str | int]:
    """
    Select a role from the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name

    Returns:
        dict[str, str, str, str | int]: {name, directory, repo_url, active}
    """
    with db_conn:
        result = db_conn.execute(
            RolesQueries.SELECT_ROLE.value, (name,)
        ).fetchone()
        if result:
            result_dict = {
                "name": result[0],
                "directory": result[1],
                "repo_url": result[2],
                "active": result[3],
            }
            return result_dict
        return {}


def select_roles(
    db_conn: sqlite3.Connection,
) -> list[dict[str, str | int]]:
    """
    Select all roles from the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection

    Returns:
        list[dict[str, str | int]]: list of roles
    """
    with db_conn:
        results = db_conn.execute(RolesQueries.SELECT_ROLES.value).fetchall()
        if results:
            results_dict = [
                {
                    "name": result[0],
                    "directory": result[1],
                    "repo_url": result[2],
                    "active": result[3],
                }
                for result in results
            ]
            return results_dict
        return []


def select_roles_by_repo_url(
    db_conn: sqlite3.Connection, repo_url: str
) -> list[dict[str, str | int]]:
    """
    Select all roles from the roles table by repo_url.

    Args:
        db_conn (sqlite3.Connection): database connection
        repo_url (str): role repository URL

    Returns:
        list[dict[str, str, str | int]]: [{name, directory, repo_url, active}}]
    """
    with db_conn:
        results = db_conn.execute(
            RolesQueries.SELECT_REPO_URL.value, (repo_url,)
        ).fetchall()
        if results:
            results_dict = [
                {
                    "name": result[0],
                    "directory": result[1],
                    "repo_url": result[2],
                    "active": result[3],
                }
                for result in results
            ]
            return results_dict
        return []


def activate_role(
    db_conn: sqlite3.Connection, name: str, active: bool
) -> None:
    """
    Activate a role in the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name
        active (bool): role active status
    """
    with db_conn:
        db_conn.execute(RolesQueries.SET_ACTIVE.value, (active, name))


def delete_role(db_conn: sqlite3.Connection, name: str) -> None:
    """
    Delete a role from the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name
    """
    with db_conn:
        db_conn.execute(RolesQueries.DELETE_ROLE.value, (name,))
