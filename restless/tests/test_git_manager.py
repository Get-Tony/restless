"""Tests for the ansible module."""

from pathlib import Path

import pytest

from restless.git_manager import clone_repo

TEST_REPO_URL = "https://github.com/Get-Tony/lib_standard"


@pytest.fixture(scope="function")
def base_path(tmp_path_factory):
    """Create a temporary directory for Ansible Runner private data."""
    base_path = (  # pylint: disable=redefined-outer-name
        tmp_path_factory.mktemp("services")
    )
    return base_path


def test_clone_repo(base_path):  # pylint: disable=redefined-outer-name
    """Clone a git repository."""
    repo_name = "lib_standard"
    repo_url = TEST_REPO_URL
    branch = "main"
    repo_dir = clone_repo(repo_name, repo_url, base_path, branch)

    assert repo_dir.stem == repo_name
    assert repo_dir.is_dir()
    assert (repo_dir / ".git").is_dir()
    assert (repo_dir / "README.md").is_file()


def test_clone_repo_no_branch(
    base_path,  # pylint: disable=redefined-outer-name
):  # pylint: disable=redefined-outer-name
    """Clone a git repository."""
    repo_name = "lib_standard"
    repo_url = TEST_REPO_URL
    repo_dir = clone_repo(repo_name, repo_url, base_path)

    assert repo_dir.stem == repo_name
    assert repo_dir.is_dir()
    assert (repo_dir / ".git").is_dir()
    assert (repo_dir / "README.md").is_file()


def test_clone_repo_invalid_repo_url(
    base_path,  # pylint: disable=redefined-outer-name
):  # pylint: disable=redefined-outer-name
    """Clone a git repository."""
    repo_name = "lib_standard"
    repo_url = "https://github.com/Get-Tony/faux_repo"

    with pytest.raises(
        Exception, match=f"Failed to clone repository: {repo_url}"
    ):
        clone_repo(repo_name, repo_url, base_path)


def test_clone_repo_invalid_repo_dir():
    """Clone a git repository."""
    repo_name = "lib_standard"
    repo_url = TEST_REPO_URL
    bad_path = Path.cwd() / "bad_path"

    with pytest.raises(
        FileNotFoundError,
        match=f"Failed to create repository directory: {bad_path}",
    ):
        clone_repo(repo_name, repo_url, bad_path)
