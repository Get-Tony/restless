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
        Exception: Failed to create service directory
        Exception: Failed to create directory
        Exception: Failed to create file
    """
    if tree_data is None:
        tree_data = DEFAULT_SERVICE_TREE

    services_path: Path = services_dir / name
    try:
        os.makedirs(services_path, exist_ok=True)
    except OSError as err:
        raise Exception(
            f"Failed to create service directory: {services_path}. Error: {err}"  # pylint: disable=line-too-long # noqa: E501
        ) from err

    def create_subdirectories_and_files(inner_key, inner_value):
        if isinstance(inner_value, dict):
            try:
                os.makedirs(inner_key, exist_ok=True)
            except Exception as err:
                raise Exception(
                    f"Failed to create directory: {inner_key}. Error: {err}"
                ) from err
            for sub_key, sub_value in inner_value.items():
                sub_key = inner_key / sub_key
                create_subdirectories_and_files(sub_key, sub_value)
        elif isinstance(inner_value, str):
            try:
                with open(inner_key, "w", encoding="utf-8") as file:
                    file.write(inner_value)
            except Exception as err:
                raise Exception(
                    f"Failed to create file: {inner_key}. Error: {err}"
                ) from err

    for base_key, base_value in tree_data.items():
        create_subdirectories_and_files(services_path / base_key, base_value)
