"""Restless application."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


import os
import shutil
import sqlite3
from pathlib import Path

import ansible_runner

from restless import database, git_manager

DEFAULT_PROJECT_TREE = {
    "ansible.cfg": """[defaults]
host_key_checking = False
retry_files_enabled = False
roles_path = ./project/roles
""",
    "inventory": {"hosts": "localhost ansible_connection=local"},
    "project": {
        "roles": {},
        "main.yml": """---
- name: Example
  hosts: localhost
  gather_facts: no
  roles:
""",
    },
}


class Project:
    """Restless project."""

    def __init__(self, db_file: str | Path):
        """Initialize the project."""
        self.db_file = db_file
        self.roles_dir = Path(self.db_file).parent / "project" / "roles"
        self.name = Path(self.db_file).stem

    def load(self) -> None:
        """Load the application."""
        if not Path(self.db_file).exists():
            raise Exception("DB file does not exist. Run 'restless init'.")
        print(f"Loading project: {self.name}")
        print(f"DB file: {self.db_file}")
        print(f"Roles: {[role_['name'] for role_ in self.list_roles()]}")
        print(f"Status: {self.git_roles_status()}")

    def init(self) -> None:
        """Initialize the application."""
        try:
            # Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
            create_project_dir(Path(self.db_file).parent)
            with database.db_connect(self.db_file) as db_conn:
                database.create_tables(db_conn)
            self.roles_dir.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            raise Exception("Failed to initialize application.") from err

    def add_role(self, name: str, repo_url: str) -> None:
        """Add a role."""
        role_dir: Path = (
            self.roles_dir / name.strip().replace(" ", "_").lower()
        )
        try:
            print(f"Cloning repository: {repo_url}")
            git_manager.clone_repo(
                repo_url,
                role_dir,
            )
        except FileExistsError as err:
            raise FileExistsError(
                f"Role directory already exists: {role_dir}."
            ) from err
        try:
            with database.db_connect(self.db_file) as db_conn:
                database.insert_role(
                    db_conn, name, str(self.roles_dir / name), repo_url
                )
        except sqlite3.IntegrityError as err:
            print(f"Failed to clone repository: {repo_url}. error: {err}")
        with database.db_connect(self.db_file) as db_conn:
            roles = database.select_roles(db_conn)
            if name not in [role["name"] for role in roles]:
                print(f"Failed to add role: {name}.")
                if Path(role_dir).exists():
                    shutil.rmtree(role_dir)

    def add_roles(self, roles: list[dict[str, str]]) -> None:
        """Add roles."""
        for role_ in roles:
            try:
                self.add_role(role_["name"], role_["repo_url"])
            except (FileExistsError, sqlite3.IntegrityError) as err:
                print(f"Failed to add role: {role_['name']}. error: {err}")
                continue
            print(f"Added role: {role_['name']}")

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

    def remove_roles(self, role_list: list[str]) -> None:
        """Remove roles."""
        with database.db_connect(self.db_file) as db_conn:
            known_roles = database.select_roles(db_conn)
        for role in role_list:
            if not any(role_["name"] == role for role_ in known_roles):
                print(f"Role '{role}' does not exist.")
                continue

    def git_pull_role(self, name: str) -> None:
        """Git pull a role."""
        with database.db_connect(self.db_file) as db_conn:
            role = database.select_role(db_conn, name)
        if not role:
            raise Exception(f"Role '{name}' does not exist.")
        try:
            git_manager.pull_repo(Path(str(role["directory"])))
        except Exception as err:
            raise Exception(f"Failed to update role: {name}") from err

    def git_pull_roles(self) -> None:
        """Git pull all roles."""
        with database.db_connect(self.db_file) as db_conn:
            roles = database.select_roles(db_conn)
        for role_ in roles:
            print(f"Pulling role: {role_['name']}")
            try:
                git_manager.pull_repo(Path(str(role_["directory"])))
            except Exception:  # pylint: disable=broad-except
                continue

    def git_roles_status(self) -> dict[str, list[str]]:
        """Show Git status of roles."""
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

    def run(self, playbook: str | Path | None = None):
        """Run the project."""
        if not Path(
            playbook or Path(self.db_file).parent / "project" / "main.yml"
        ).exists():
            raise Exception(f"Playbook '{playbook}' does not exist.")
        print(f"Running project: {self.name}")
        try:
            project_dir = Path(self.db_file).parent
            return ansible_runner.run(
                private_data_dir=project_dir,
                playbook="main.yml",
                inventory="inventory/hosts",
                envvars={"ANSIBLE_CONFIG": "ansible.cfg"},
            )
        except Exception as err:  # pylint: disable=broad-except
            raise Exception(f"Failed to run playbook: {playbook}") from err


def create_project_dir(
    projects_dir: str | Path,
    tree_data: dict | None = None,
) -> None:
    """
    Create a project directory.

    Args:
        projects_dir (str | Path): path to project directory
        tree_data (dict, optional): dictionary of directories and files to
            create. If None, the default tree will be used. Defaults to None.
    """
    if tree_data is None:
        tree_data = DEFAULT_PROJECT_TREE

    services_path: Path = Path(projects_dir)
    services_path.mkdir(parents=True, exist_ok=True)

    def create_subdirectories_and_files(inner_key, inner_value):
        if isinstance(inner_value, dict):
            os.makedirs(inner_key, exist_ok=True)

            for sub_key, sub_value in inner_value.items():
                sub_key = Path(inner_key) / sub_key
                create_subdirectories_and_files(sub_key, sub_value)
        elif isinstance(inner_value, str):
            if not Path(inner_key).is_file():
                print(f"Creating file: {inner_key} {inner_value}")
                with open(Path(inner_key), "w", encoding="utf-8") as file:
                    file.write(inner_value)

    for base_key, base_value in tree_data.items():
        create_subdirectories_and_files(services_path / base_key, base_value)
