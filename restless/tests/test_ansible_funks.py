"""Tests for the ansible module."""

import pytest

from restless.ansible_funks import create_service_dir


@pytest.fixture(scope="function")
def base_path(tmp_path_factory):
    """Create a temporary directory for Ansible Runner private data."""
    base_path = (  # pylint: disable=redefined-outer-name
        tmp_path_factory.mktemp("services")
    )
    return base_path


def test_create_service_dir(base_path):  # pylint: disable=redefined-outer-name
    """Create a directory for a service."""
    service_name = "test_service"
    create_service_dir(service_name, base_path)
    assert (base_path / service_name).is_dir()
    assert (base_path / service_name / "env").is_dir()
    assert (base_path / service_name / "env" / "envvars").is_file()
    assert (base_path / service_name / "env" / "extravars").is_file()
    assert (base_path / service_name / "env" / "passwords").is_file()
    assert (base_path / service_name / "env" / "cmdline").is_file()
    assert (base_path / service_name / "env" / "settings").is_file()
    assert (base_path / service_name / "env" / "ssh_key").is_file()
    assert (base_path / service_name / "inventory").is_dir()
    assert (base_path / service_name / "inventory" / "hosts").is_file()
    assert (base_path / service_name / "project").is_dir()
    assert (base_path / service_name / "project" / "main.yml").is_file()
    assert (base_path / service_name / "project" / "roles").is_dir()
    assert (base_path / service_name / "project" / "roles" / "common").is_dir()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "defaults"
    ).is_dir()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "handlers"
    ).is_dir()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "meta"
    ).is_dir()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "README.md"
    ).is_file()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "tasks"
    ).is_dir()
    assert (
        base_path
        / service_name
        / "project"
        / "roles"
        / "common"
        / "tasks"
        / "main.yml"
    ).is_file()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "tests"
    ).is_dir()
    assert (
        base_path / service_name / "project" / "roles" / "common" / "vars"
    ).is_dir()
