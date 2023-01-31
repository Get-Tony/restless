"""Ansible integration for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

from pathlib import Path

from git.repo import Repo


def clone_repo(
    name: str,
    repo_url: str,
    local_base_dir: Path,
    branch: str | None = None,
) -> Path:
    """
    Clone a Git repository into a directory.

    Args:
        name (str): name of the directory to clone the repository into
        repo_url (str): URL of the Git repository to clone
        local_base_dir (Path): directory to store the repository directory
        branch (str, optional): branch to checkout. Defaults to None.

    Raises:
        FileNotFoundError: Failed to create repository directory,
            missing parent directory.
        Exception: Failed to clone repository

    Returns:
        Path: path to the cloned repository
    """
    repo_dir = local_base_dir / name
    err_msg = f"Failed to create repository directory: {local_base_dir}."
    try:
        repo_dir.mkdir()
    except FileNotFoundError as err:
        raise FileNotFoundError(f"{err_msg}") from err

    try:
        repo = Repo.clone_from(repo_url, repo_dir)
    except Exception as err:
        raise Exception(f"Failed to clone repository: {repo_url}.") from err

    if branch:
        repo.git.checkout(branch)

    return repo_dir
