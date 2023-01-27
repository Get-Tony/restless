"""pytest tests for the services module."""

from pathlib import Path

import pytest
from lib_standard import EnhancedConfigParser

from restless.service import AnsibleService


@pytest.fixture(scope="session")
def settings_file(tmp_path_factory) -> Path:
    """Return a temporary folder path."""
    settings = EnhancedConfigParser()
    settings.read_dict({"SERVICE": {"name": "test_service"}})
    settings_path = tmp_path_factory.mktemp("data") / "settings.ini"
    with open(settings_path, "w", encoding="utf-8") as file:
        settings.write(file)
    assert settings_path.is_file()
    return settings_path


@pytest.fixture(scope="function")
def service(
    settings_file,  # pylint: disable=redefined-outer-name
) -> AnsibleService:
    """Create an AnsibleService instance."""
    return AnsibleService(
        name="test_service",
        config_path=settings_file.parent,
        description="Test service",
    )


def test_service_init(service):  # pylint: disable=redefined-outer-name
    """Test the AnsibleService class."""

    assert service.name == "test_service"
    assert service.description == "Test service"
    assert service.config == EnhancedConfigParser()
    assert service.active is True
    assert service.last_loaded_on is None


def test_service_load_active(service):  # pylint: disable=redefined-outer-name
    """Test the AnsibleService.load() method."""
    assert isinstance(service.config, EnhancedConfigParser)
    assert service.active is True
    assert service.last_loaded_on is None
    service.load()
    assert service.last_loaded_on is not None


def test_service_load_inactive(
    service,  # pylint: disable=redefined-outer-name
):
    """Test the AnsibleService.load() method."""
    assert isinstance(service.config, EnhancedConfigParser)
    service.active = False
    assert service.active is False
    assert service.last_loaded_on is None
    with pytest.raises(RuntimeError):
        service.load()
    assert service.last_loaded_on is None


def test_service_load_invalid_path(
    service,  # pylint: disable=redefined-outer-name
):
    """Test the AnsibleService.load() method."""
    assert isinstance(service.config, EnhancedConfigParser)
    service.active = True
    service.config_path = "invalid_path"
    with pytest.raises(ValueError):
        service.load()


def test_service_save(service):  # pylint: disable=redefined-outer-name
    """Test the AnsibleService.save() method."""
    with pytest.raises(NotImplementedError):
        service.save()
