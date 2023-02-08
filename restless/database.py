"""SQLite3 database abstraction layer for role."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

import sqlite3
from contextlib import contextmanager
from enum import Enum
from pathlib import Path

# Database queries


class RolesQueries(Enum):
    """SQLite3 Query enumeration."""

    CREATE_ROLES_TABLE = """CREATE TABLE IF NOT EXISTS roles(
        role_name TEXT NOT NULL UNIQUE,
        directory TEXT NOT NULL UNIQUE,
        repo_url TEXT NOT NULL,
        active INTEGER NOT NULL
    )"""
    INSERT_ROLE = """INSERT INTO roles VALUES(?, ?, ?, ?)"""
    SELECT_ROLE = """SELECT * FROM roles WHERE name = ?"""
    SELECT_REPO_URL = """SELECT * FROM roles WHERE repo_url = ?"""
    SELECT_ROLES = """SELECT * FROM roles"""
    UPDATE_ACTIVE = """UPDATE roles SET active = ? WHERE name = ?"""
    DELETE_ROLE = """DELETE FROM roles WHERE name = ?"""


class ProjectsQueries(Enum):
    """SQLite3 Query enumeration."""

    CREATE_PROJECTS_TABLE = """CREATE TABLE IF NOT EXISTS projects(
        project_name TEXT NOT NULL UNIQUE,
        directory TEXT NOT NULL UNIQUE,
        repo_url TEXT,
        active INTEGER NOT NULL
    )"""
    INSERT_PROJECT = """INSERT INTO projects VALUES(?, ?, ?, ?)"""
    SELECT_PROJECT = """SELECT * FROM projects WHERE name = ?"""
    SELECT_REPO_URL = """SELECT * FROM projects WHERE repo_url = ?"""
    SELECT_PROJECTS = """SELECT * FROM projects"""
    UPDATE_ACTIVE = """UPDATE projects SET active = ? WHERE name = ?"""
    DELETE_PROJECT = """DELETE FROM projects WHERE name = ?"""


class ProjectRoleQueries(Enum):
    """SQLite3 Query enumeration."""

    CREATE_PROJECT_ROLES_TABLE = """CREATE TABLE IF NOT EXISTS project_roles(
        project_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id),
        FOREIGN KEY(role_id) REFERENCES roles(id)
    )"""
    INSERT_PROJECT_ROLE = """INSERT INTO project_roles VALUES(?, ?)"""
    SELECT_PROJECT_ROLE = (
        """SELECT * FROM project_roles WHERE project_id = ?"""
    )
    SELECT_PROJECT_ROLES = """SELECT * FROM project_roles"""
    DELETE_PROJECT_ROLE = """DELETE FROM project_roles WHERE project_id = ?"""


# Database connection


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


# Roles


def create_tables(db_conn: sqlite3.Connection) -> None:
    """
    Create the database tables.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    with db_conn:
        db_conn.execute(RolesQueries.CREATE_ROLES_TABLE.value)
        db_conn.execute(ProjectsQueries.CREATE_PROJECTS_TABLE.value)
        db_conn.execute(ProjectRoleQueries.CREATE_PROJECT_ROLES_TABLE.value)


def insert_role(
    db_conn: sqlite3.Connection,
    role_name: str,
    directory: str | Path,
    repo_url: str | None,
    active: bool = True,
) -> None:
    """
    Insert a role into the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        role_name (str): role name
        directory (str | Path): role directory
        repo_url (str): role repository URL
        active (bool): role active status
    """
    with db_conn:
        db_conn.execute(
            RolesQueries.INSERT_ROLE.value,
            (role_name, directory, repo_url or "", active),
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


def set_role_active(
    db_conn: sqlite3.Connection, name: str, active: bool
) -> None:
    """
    Set a roles active status.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name
        active (bool): role active status
    """
    with db_conn:
        db_conn.execute(RolesQueries.UPDATE_ACTIVE.value, (active, name))


def delete_role(db_conn: sqlite3.Connection, name: str) -> None:
    """
    Delete a role from the roles table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): role name
    """
    with db_conn:
        db_conn.execute(RolesQueries.DELETE_ROLE.value, (name,))


# Projects


def create_projects_table(db_conn: sqlite3.Connection) -> None:
    """
    Create the projects table.

    Args:
        db_conn (sqlite3.Connection): database connection
    """
    with db_conn:
        db_conn.execute(ProjectsQueries.CREATE_PROJECTS_TABLE.value)


def insert_project(
    db_conn: sqlite3.Connection,
    name: str,
    directory: str | Path,
    repo_url: str | None,
    active: bool = True,
) -> None:
    """
    Insert a project into the projects table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): project name
        directory (str | Path): project directory
        repo_url (str): project repository URL
        active (bool): project active status
    """
    with db_conn:
        db_conn.execute(
            ProjectsQueries.INSERT_PROJECT.value,
            (name, directory, repo_url or "", active),
        )


def select_project(
    db_conn: sqlite3.Connection, name: str
) -> dict[str, str | int]:
    """
    Select a project from the projects table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): project name

    Returns:
        dict[str, str, str, str | int]: {name, directory, repo_url, active}
    """
    with db_conn:
        result = db_conn.execute(
            ProjectsQueries.SELECT_PROJECT.value, (name,)
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


def select_projects(
    db_conn: sqlite3.Connection,
) -> list[dict[str, str | int]]:
    """
    Select all projects from the projects table.

    Args:
        db_conn (sqlite3.Connection): database connection

    Returns:
        list[dict[str, str | int]]: list of projects
    """
    with db_conn:
        results = db_conn.execute(
            ProjectsQueries.SELECT_PROJECTS.value
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


def select_projects_by_repo_url(
    db_conn: sqlite3.Connection, repo_url: str
) -> list[dict[str, str | int]]:
    """
    Select all projects from the projects table by repo_url.

    Args:
        db_conn (sqlite3.Connection): database connection
        repo_url (str): project repository URL

    Returns:
        list[dict[str, str, str | int]]: [{name, directory, repo_url, active}}]
    """
    with db_conn:
        results = db_conn.execute(
            ProjectsQueries.SELECT_REPO_URL.value, (repo_url,)
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


def set_project_active(
    db_conn: sqlite3.Connection, name: str, active: bool
) -> None:
    """
    Set a projects active status.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): project name
        active (bool): project active status
    """
    with db_conn:
        db_conn.execute(ProjectsQueries.UPDATE_ACTIVE.value, (active, name))


def delete_project(db_conn: sqlite3.Connection, name: str) -> None:
    """
    Delete a project from the projects table.

    Args:
        db_conn (sqlite3.Connection): database connection
        name (str): project name
    """
    with db_conn:
        db_conn.execute(ProjectsQueries.DELETE_PROJECT.value, (name,))
