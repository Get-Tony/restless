"""Restless application."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


import os
import shutil
import sqlite3
from pathlib import Path

from restless import database, git_manager

DEFAULT_PROJECT_TREE = {
    "env": {
        "envvars": "",
        "extravars": "",
        "passwords": "",
        "cmdline": "",
        "settings": "",
        "ssh_key": "",
    },
    "inventory": {"hosts": ""},
    "project": {
        "roles": {
            "common": {
                "defaults": {},
                "handlers": {},
                "meta": {},
                "README.md": "# Common Role\n",
                "tasks": {
                    "main.yml": "---\n",
                },
                "tests": {},
                "vars": {},
            }
        },
        "main.yml": "---\n",
    },
}


class Project:
    """Restless project."""

    def __init__(self, db_file: str | Path):
        """Initialize the project."""
        self.db_file = db_file
        self.roles_dir = Path(self.db_file).parent / "project" / "roles"

    def load(self) -> None:
        """Load the application."""
        if not Path(self.db_file).exists():
            raise Exception("DB file does not exist. Run 'restless init'.")
        try:
            with database.db_connect(self.db_file) as db_conn:
                roles = database.select_roles(db_conn)
                for role_ in roles:
                    print(f"Loading role: {role_['name']}")

        except Exception as err:
            raise Exception("Failed to load application.") from err

    def init(self) -> None:
        """Initialize the application."""
        try:
            Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
            with database.db_connect(self.db_file) as db_conn:
                database.create_roles_table(db_conn)
            self.roles_dir.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            raise Exception("Failed to initialize application.") from err

    def add_role(self, name: str, repo_url: str) -> None:
        """Add a role."""
        try:
            with database.db_connect(self.db_file) as db_conn:
                database.insert_role(
                    db_conn, name, str(self.roles_dir / name), repo_url
                )
        except sqlite3.IntegrityError as err:
            print(f"Failed to clone repository: {repo_url}. error: {err}")
        try:
            git_manager.clone_repo(
                repo_url,
                self.roles_dir / name.strip().replace(" ", "_").lower(),
            )
        except Exception as err:
            if "fatal: destination path" in str(err):
                raise FileExistsError(
                    f"Failed to create repository directory: {self.roles_dir / name.strip().replace(' ', '_').lower()}."  # noqa: E501 pylint: disable=line-too-long
                ) from err
            raise Exception(
                f"Failed to clone repository: {repo_url}."
            ) from err

    def remove_role(self, name: str) -> None:
        """Remove a role."""
        with database.db_connect(self.db_file) as db_conn:
            database.delete_role(db_conn, name)
        role_dir = self.roles_dir / f"{name}"
        if role_dir.exists() and role_dir.is_dir():
            print(f"Removing role directory: {role_dir}")
            try:
                shutil.rmtree(role_dir)
            except Exception as err:
                raise FileExistsError(
                    f"Failed to remove role directory: {role_dir}"
                ) from err

    def list_roles(self) -> list[dict[str, str | int]]:
        """List roles."""
        with database.db_connect(self.db_file) as db_conn:
            return database.select_roles(db_conn)

    def update_role(self, name: str) -> None:
        """Update a role."""
        with database.db_connect(self.db_file) as db_conn:
            role = database.select_role(db_conn, name)
        if not role:
            raise Exception(f"Role '{name}' does not exist.")
        try:
            git_manager.pull_repo(Path(str(role["directory"])))
        except Exception as err:
            raise Exception(f"Failed to update role: {name}") from err

    def update_roles(self) -> None:
        """Update all roles."""
        with database.db_connect(self.db_file) as db_conn:
            roles = database.select_roles(db_conn)
        pulled_roles = []
        for role_ in roles:
            print(f"Updating role: {role_['name']}")
            try:
                git_manager.pull_repo(Path(str(role_["directory"])))
                pulled_roles.append(role_["name"])
            except Exception:  # pylint: disable=broad-except
                continue

    def roles_status(self) -> dict[str, list[str]]:
        """Show status of roles."""
        with database.db_connect(self.db_file) as db_conn:
            roles = database.select_roles(db_conn)
        report: dict[str, list[str]] = {"clean": [], "dirty": []}

        for role_ in roles:
            repo_obj = git_manager.repo_obj_from_dir(
                Path(str(role_["directory"]))
            )
            if not repo_obj.is_dirty():
                report["clean"].append(str(role_["name"]))
            elif repo_obj.is_dirty():
                report["dirty"].append(str(role_["name"]))
        return report


def create_project_dir(
    name: str,
    projects_dir: Path,
    tree_data: dict | None = None,
) -> None:
    """
    Create a project directory.

    Args:
        name (str): service name
        projects_dir (Path): path to projects directory
        tree_data (dict, optional): dictionary of directories and files to
            create. If None, the default tree will be used. Defaults to None.

    Raises:
        OSError: Failed to create service directory
        Exception: Failed to create directory
        Exception: Failed to create file
    """
    if tree_data is None:
        tree_data = DEFAULT_PROJECT_TREE

    services_path: Path = projects_dir / name
    try:
        services_path.mkdir(parents=True, exist_ok=False)
    except OSError as err:
        raise OSError(f"Failed to create service directory: {err}") from err

    def create_subdirectories_and_files(inner_key, inner_value):
        if isinstance(inner_value, dict):
            os.makedirs(inner_key, exist_ok=True)

            for sub_key, sub_value in inner_value.items():
                sub_key = inner_key / sub_key
                create_subdirectories_and_files(sub_key, sub_value)
        elif isinstance(inner_value, str):
            with open(inner_key, "w", encoding="utf-8") as file:
                file.write(inner_value)

    for base_key, base_value in tree_data.items():
        create_subdirectories_and_files(services_path / base_key, base_value)
