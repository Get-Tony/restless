"""Main module for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

from dataclasses import dataclass, field
from pathlib import Path

from lib_standard import EnhancedConfigParser

from restless.service import Service


@dataclass
class App:
    """Restless app class."""

    settings: EnhancedConfigParser = field(
        default_factory=EnhancedConfigParser, init=True, repr=True
    )
    config_file: str = field(default="config.ini", init=False, repr=False)
    services: list[Service] = field(
        default_factory=list, init=False, repr=False
    )

    def new_service(self, name: str, directory: str | Path) -> Service:
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

    def load_service(self, directory: str | Path) -> Service:
        """Load an existing service.

        Args:
            name (str): service name
            directory (str | Path): service directory

        Returns:
            Service: service instance
        """
        service_obj = Service(directory=directory)
        service_obj.load()
        return service_obj

    def load(self) -> None:
        """Load the app settings."""
        if not Path(self.config_file).is_file():
            raise FileNotFoundError(
                f"Config file not found: {self.config_file}"
            )
        self.settings.read(self.config_file)
