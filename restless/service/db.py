"""SQLite3 database abstraction layer for service."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

import sqlite3
from enum import Enum
from pathlib import Path


class Queries(Enum):
    """SQLite3 Query enumeration."""

    CREATE_SERVICES_TABLE = """CREATE TABLE IF NOT EXISTS services(
        name TEXT NOT NULL UNIQUE,
        directory TEXT NOT NULL UNIQUE,
        active INTEGER NOT NULL
    )"""
    INSERT_SERVICE = """INSERT INTO services VALUES(?, ?, ?)"""
    SELECT_SERVICE = """SELECT * FROM services WHERE name = ?"""
    SELECT_SERVICES = """SELECT * FROM services"""
    SET_ACTIVE = """UPDATE services SET active = ? WHERE name = ?"""
    DELETE_SERVICE = """DELETE FROM services WHERE name = ?"""


def create_services_table(db_conn: sqlite3.Connection) -> None:
    """
    Create the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    with db_conn:
        db_conn.execute(Queries.CREATE_SERVICES_TABLE.value)


def insert_service(
    db_conn: sqlite3.Connection,
    name: str,
    directory: str | Path,
    active: bool,
) -> None:
    """
    Insert a service into the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): service name
        directory (str | Path): service directory
        active (bool): service active status
    """
    with db_conn:
        db_conn.execute(
            Queries.INSERT_SERVICE.value, (name, directory, active)
        )


def select_service(
    db_conn: sqlite3.Connection, name: str
) -> tuple[str, str, int]:
    """
    Select a service from the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): service name

    Returns:
        tuple[str, str, int]: service data
    """
    with db_conn:
        return db_conn.execute(
            Queries.SELECT_SERVICE.value, (name,)
        ).fetchone()


def select_services(db_conn: sqlite3.Connection) -> list[tuple[str, str, int]]:
    """
    Select all services from the services table.

    Args:
        db_conn (sqlite3.Connection): database connection

    Returns:
        list[tuple[str, str, int]]: service data
    """
    with db_conn:
        return db_conn.execute(Queries.SELECT_SERVICES.value).fetchall()


def update_service(
    db_conn: sqlite3.Connection, name: str, active: bool
) -> None:
    """
    Update a service in the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): service name
        active (bool): service active status
    """
    with db_conn:
        db_conn.execute(Queries.SET_ACTIVE.value, (active, name))


def delete_service(db_conn: sqlite3.Connection, name: str) -> None:
    """
    Delete a service from the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): service name
    """
    with db_conn:
        db_conn.execute(Queries.DELETE_SERVICE.value, (name,))
