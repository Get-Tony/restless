"""Main module for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

from dataclasses import dataclass, field
from pathlib import Path

from lib_standard import EnhancedConfigParser


@dataclass
class Service:
    """Service class."""

    directory: str | Path = field(init=True, repr=True)
    name: str | None = field(default="", init=True, repr=True)
    settings: EnhancedConfigParser = field(
        default_factory=EnhancedConfigParser, init=True, repr=True
    )
    _config_file_name: str = field(
        default="settings.ini", init=False, repr=False
    )
    _config_section: str = field(default="SERVICE", init=False, repr=False)

    @property
    def is_active(self) -> bool:
        """Check if the service is active."""
        return self.settings.getboolean(
            self._config_section, "active", fallback=False
        )

    @property
    def config_file(self) -> Path:
        """Return Path obj for config file."""
        return Path(self.directory) / self._config_file_name

    def load(self) -> None:
        """Load settings."""
        if not self.config_file.is_file():
            raise FileNotFoundError(
                f"Config file not found: {self.config_file}"
            )
        temp_parser = EnhancedConfigParser()
        temp_parser.read(self.config_file)
        if self._config_section not in self.settings:
            raise KeyError(
                "%s section missing from: %s" % self._config_section,
                self.config_file,
            )
        self.settings.read(self.config_file)

    def save(self) -> None:
        """Save settings."""
        with open(self.config_file, "w", encoding="utf-8") as file:
            self.settings.write(file)


def new_service(name: str, directory: str | Path) -> Service:
    """Create a new service.

    Args:
        name (str): service name
        directory (str | Path): service directory

    Returns:
        Service: service instance
    """
    service_obj = Service(name=name, directory=directory)
    service_obj.settings.read_dict(
        {"SERVICE": {"name": name, "active": "True"}}
    )
    service_obj.config_file.parent.mkdir(parents=True, exist_ok=True)
    service_obj.save()
    return service_obj


def load_service(directory: str | Path) -> Service:
    """Load an existing service.

    Args:
        directory (str | Path): service directory

    Returns:
        Service: service instance
    """
    service_obj = Service(directory=directory)
    service_obj.load()
    return service_obj
