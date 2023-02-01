"""Ansible integration for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"
import os
from pathlib import Path

DEFAULT_SERVICE_TREE = {
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


def create_service_dir(
    name: str,
    services_dir: Path,
    tree_data: dict | None = None,
) -> None:
    """
    Create a new service directory and populate it with the default tree.

    Args:
        name (str): service name
        services_dir (Path): path to the services directory
        tree_data (dict, optional): dictionary of directories and files to
            create. If None, the default tree will be used. Defaults to None.

    Raises:
        OSError: Failed to create service directory
        Exception: Failed to create directory
        Exception: Failed to create file
    """
    if tree_data is None:
        tree_data = DEFAULT_SERVICE_TREE

    services_path: Path = services_dir / name
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
