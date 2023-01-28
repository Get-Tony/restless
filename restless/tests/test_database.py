"""pytest tests for the database module."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

import pytest

from restless.db import (
    create_services_table,
    db_connect,
    delete_service,
    insert_service,
    select_service,
    select_services,
    update_service,
)


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
    with db_connect(db_file) as conn:
        yield conn


@pytest.fixture(scope="function")
def memory_conn_with_tables():
    """
    memory_conn_with_tables fixture.

    Yields:
        sqlite3.Connection: database connection
    """
    with db_connect() as conn:
        create_services_table(conn)
        yield conn


def test_create_services_table(
    db_conn,  # pylint: disable=redefined-outer-name
):
    """
    Test creating the services table.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    create_services_table(db_conn)
    assert "services" in [
        t[0]
        for t in db_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    ]


def test_insert_service(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test inserting a service.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    insert_service(memory_conn_with_tables, "service1", "dir1", True)
    service = select_service(memory_conn_with_tables, "service1")
    assert service == ("service1", "dir1", 1)


def test_select_service(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting a service.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    insert_service(memory_conn_with_tables, "service1", "dir1", True)
    service = select_service(memory_conn_with_tables, "service1")
    assert service == ("service1", "dir1", 1)


def test_select_services(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting all services.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    insert_service(memory_conn_with_tables, "service1", "dir1", True)
    insert_service(memory_conn_with_tables, "service2", "dir2", False)
    services = select_services(memory_conn_with_tables)
    assert services == [("service1", "dir1", 1), ("service2", "dir2", 0)]


def test_update_service(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test updating a service.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    insert_service(memory_conn_with_tables, "service1", "dir1", True)
    update_service(memory_conn_with_tables, "service1", False)
    service = select_service(memory_conn_with_tables, "service1")
    assert service == ("service1", "dir1", 0)


def test_delete_service(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test deleting a service.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    insert_service(memory_conn_with_tables, "service1", "dir1", True)
    delete_service(memory_conn_with_tables, "service1")
    service = select_service(memory_conn_with_tables, "service1")
    assert service is None


def test_select_service_not_exists(
    memory_conn_with_tables,  # pylint: disable=redefined-outer-name
):
    """
    Test selecting a service that does not exist.

    Args:
        memory_conn_with_tables (sqlite3.Connection): database connection
    """
    create_services_table(memory_conn_with_tables)
    service = select_service(memory_conn_with_tables, "service1")
    assert service is None
