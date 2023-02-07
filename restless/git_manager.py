"""Ansible integration for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

from pathlib import Path

from git.repo import Repo


def clone_repo(
    repo_url: str,
    directory: str | Path,
    branch: str | None = None,
) -> None:
    """
    Clone a Git repository into a directory.

    Args:
        repo_url (str): URL of the Git repository to clone (no ".git").
        directory (str | Path): directory to clone the repository into.
        branch (str, optional): branch to checkout. Defaults to None.

    Raises:
        FileNotFoundError: Failed to create repository directory,
            missing parent directory.
        Exception: Failed to clone repository
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        repo = Repo.clone_from(repo_url, str(directory))
        if branch:
            repo.git.checkout(branch)
    except Exception as err:
        raise Exception(f"Failed to clone repository: {repo_url}.") from err


def pull_repo(directory: str | Path) -> None:
    """
    Pull a Git repository.

    Args:
        directory (str | Path): directory of the repository to pull.

    Raises:
        FileNotFoundError: Failed to find repository directory.
        Exception: Failed to pull repository
    """
    try:
        repo = Repo(str(directory))
        repo.remotes.origin.pull()
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Failed to find repository directory: {directory}."
        ) from err
    except Exception as err:
        raise Exception(f"Failed to pull repository: {directory}.") from err


def push_repo(directory: str | Path) -> None:
    """
    Push a Git repository.

    Args:
        directory (str | Path): directory of the repository to push.

    Raises:
        FileNotFoundError: Failed to find repository directory.
        Exception: Failed to push repository
    """
    try:
        repo = Repo(str(directory))
        repo.remotes.origin.push()
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Failed to find repository directory: {directory}."
        ) from err
    except Exception as err:
        raise Exception(f"Failed to push repository: {directory}.") from err


def commit_repo(directory: str | Path, message: str) -> None:
    """
    Commit a Git repository.

    Args:
        directory (str | Path): directory of the repository to commit.
        message (str): commit message.

    Raises:
        FileNotFoundError: Failed to find repository directory.
        Exception: Failed to commit repository
    """
    try:
        repo = Repo(str(directory))
        repo.git.add(A=True)
        repo.index.commit(message)
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Failed to find repository directory: {directory}."
        ) from err
    except Exception as err:
        raise Exception(f"Failed to commit repository: {directory}.") from err


def repo_obj_from_dir(directory: str | Path) -> Repo:
    """
    Get a Git repository.

    Args:
        directory (str | Path): directory of the repository to get.

    Raises:
        FileNotFoundError: Failed to find repository directory.
        Exception: Failed to get repository

    Returns:
        Repo: Git repository
    """
    try:
        return Repo(str(directory))
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Failed to find repository directory: {directory}."
        ) from err
    except Exception as err:
        raise Exception(f"Failed to get repository: {directory}.") from err
