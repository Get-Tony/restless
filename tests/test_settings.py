"""Test Restless settings."""

from src.settings import settings


def test_settings_availability() -> None:
    """Test settings availability."""
    assert isinstance(settings.debug, bool)
