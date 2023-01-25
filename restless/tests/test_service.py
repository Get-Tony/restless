"""pytest tests for the services module."""

import configparser

import pytest


@pytest.fixture(scope="session")
def settings_file(tmp_path_factory):
    """Return a temporary folder path."""
    settings = configparser.ConfigParser()
    settings.read_dict({"SERVICE": {"name": "test_service"}})
    settings_path = tmp_path_factory.mktemp("data") / "settings.ini"
    with open(settings_path, "w", encoding="utf-8") as file:
        settings.write(file)
    return settings_path
