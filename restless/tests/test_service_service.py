"""Tests for the Service class."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

from configparser import NoSectionError
from pathlib import Path

import pytest
from lib_standard import EnhancedConfigParser

from restless.service.service import Service, load_service, new_service


@pytest.fixture
def service_dir(tmp_path_factory) -> str:
    """Create a temporary directory to store the service files."""
    return tmp_path_factory.mktemp("service")


def test_service_class_init_no_name(
    service_dir,
):  # pylint: disable=redefined-outer-name
    """ "Test the Service class."""
    service = Service(service_dir)
    assert Path(service.directory).exists()
    assert "service" in Path(service.directory).stem
    assert isinstance(service.settings, EnhancedConfigParser)
    assert service.is_active is False
    assert service.settings_file == service_dir / "settings.ini"


def test_service_class_init_with_name(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """ "Test the Service class."""
    service = Service(service_dir, "test_service")
    assert Path(service.directory).exists()
    assert service.name == "test_service"
    assert isinstance(service.settings, EnhancedConfigParser)
    assert service.is_active is False
    assert service.settings_file == service_dir / "settings.ini"


def test_new_service(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the new_service function."""
    service = new_service("test_service", service_dir)
    assert isinstance(service, Service)
    assert service.name == "test_service"
    assert service.is_active is True
    assert (
        service.settings_file == service_dir / "test_service" / "settings.ini"
    )
    assert service.settings_file.exists()


def test_new_service_already_exists(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the new_service function."""
    new_service("test_service", service_dir)
    with pytest.raises(FileExistsError):
        new_service("test_service", service_dir)


def test_new_service_directory_not_exists(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the new_service function."""
    with pytest.raises(FileNotFoundError):
        new_service("test_service", service_dir / "not_exists")


def test_load_service(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    service = new_service("test_service", service_dir)
    service_obj = load_service(service.directory)
    assert isinstance(service_obj, Service)
    assert service_obj.name == "test_service"
    assert service_obj.is_active is True
    assert (
        service_obj.settings_file
        == service_dir / "test_service" / "settings.ini"
    )
    assert service_obj.settings_file.exists()


def test_load_service_dir_not_exists(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    with pytest.raises(FileNotFoundError):
        load_service(service_dir / "not_exists")


def test_load_service_no_service_section(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    service = new_service("test_service", service_dir)
    assert service.settings_file.exists() is True
    assert service.settings.has_section("SERVICE") is True
    service.settings.remove_section("SERVICE")
    assert service.settings.has_section("SERVICE") is False
    with open(service.settings_file, "w", encoding="utf-8") as file:
        service.settings.write(file)
    with pytest.raises(NoSectionError):
        load_service(service_dir / "test_service")


def test_load_service_no_name_key(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    service = new_service("test_service", service_dir)
    assert service.settings_file.exists() is True
    assert service.settings.has_option("SERVICE", "name") is True
    service.settings.remove_option("SERVICE", "name")
    assert service.settings.has_option("SERVICE", "name") is False

    with open(service.settings_file, "w", encoding="utf-8") as file:
        service.settings.write(file)

    assert service.settings.has_option("SERVICE", "name") is False

    with pytest.raises(KeyError):
        load_service(service_dir / "test_service")


def test_load_service_empty_name_key(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    service = new_service("test_service", service_dir)
    assert service.settings_file.exists() is True
    assert service.settings.has_option("SERVICE", "name") is True
    service.settings.set("SERVICE", "name", "")
    assert service.settings.get("SERVICE", "name") == ""

    with open(service.settings_file, "w", encoding="utf-8") as file:
        service.settings.write(file)

    with pytest.raises(ValueError):
        load_service(service_dir / "test_service")


def test_load_service_no_settings_file(
    service_dir,  # pylint: disable=redefined-outer-name
):
    """Test the load_service function."""
    service = new_service("test_service", service_dir)
    assert service.settings_file.exists() is True
    service.settings_file.unlink()
    assert service.settings_file.exists() is False
    with pytest.raises(FileNotFoundError):
        load_service(service_dir / "test_service")
