"""pytest tests for the services module."""
import pytest

from restless.services import Service


def test_service_init():
    """Test the Service class."""
    service = Service()
    assert service


def test_service_call():
    """Test the Service class."""
    service = Service()
    with pytest.raises(NotImplementedError):
        assert service()


def test_service_run():
    """Test the Service class."""
    service = Service()
    with pytest.raises(NotImplementedError):
        assert service.run()
