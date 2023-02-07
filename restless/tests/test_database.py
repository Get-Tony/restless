"""Tests for the role module DB."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

import pytest

from restless import database as db


@pytest.fixture(scope="function")
def db_file(tmp_path_factory):
    """
    db_file fixture.

    Returns:
        tempfile: test.db
    """
    return tmp_path_factory.mktemp("data") / "test.db"


@pytest.fixture(scope="function")
def db_conn(db_file):  # pylint: disable=redefined-outer-name
    """
    db_conn connection fixture for db_file.

    Yields:
        sqlite3.Connection: database connection
    """
    with db.db_connect(db_file) as conn:
        yield conn


@pytest.fixture(scope="function")
def memory_conn_with_tables():
    """
    memory_conn_with_tables fixture.

    Yields:
        sqlite3.Connection: database connection
    """
    with db.db_connect() as conn:
        db.create_roles_table(conn)
        yield conn


def test_create_roles_table(
    db_conn,  # pylint: disable=redefined-outer-name
):
    """
    Test creating the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    db.create_roles_table(db_conn)
    assert "roles" in [
        t[0]
        for t in db_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    ]


def test_insert_role(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test inserting a role.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.insert_role(memory_conn_with_tables, "role1", "dir1", True)
    role = db.select_role(memory_conn_with_tables, "role1")
    assert role == ("role1", "dir1", 1)


def test_select_role(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting a role.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.insert_role(memory_conn_with_tables, "role1", "dir1", True)
    role = db.select_role(memory_conn_with_tables, "role1")
    assert role == ("role1", "dir1", 1)


def test_select_roles(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting all roles.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.insert_role(memory_conn_with_tables, "role1", "dir1", True)
    db.insert_role(memory_conn_with_tables, "role2", "dir2", False)
    roles = db.select_roles(memory_conn_with_tables)
    assert roles == [("role1", "dir1", 1), ("role2", "dir2", 0)]


def test_update_role(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test updating a role.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.insert_role(memory_conn_with_tables, "role1", "dir1", True)
    db.update_role(memory_conn_with_tables, "role1", False)
    role = db.select_role(memory_conn_with_tables, "role1")
    assert role == ("role1", "dir1", 0)


def test_delete_role(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test deleting a role.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.insert_role(memory_conn_with_tables, "role1", "dir1", True)
    db.delete_role(memory_conn_with_tables, "role1")
    role = db.select_role(memory_conn_with_tables, "role1")
    assert role is None


def test_select_role_not_exists(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting a role that does not exist.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    db.create_roles_table(memory_conn_with_tables)
    role = db.select_role(memory_conn_with_tables, "role1")
    assert role is None
