"""Service."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


from configparser import NoSectionError
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
    _file_name: str = field(default="settings.ini", init=False, repr=False)
    _section: str = field(default="SERVICE", init=False, repr=False)

    @property
    def is_active(self) -> bool:
        """Check if the service is active."""
        return self.settings.getboolean(
            self._section, "active", fallback=False
        )

    @property
    def settings_file(self) -> Path:
        """Return Path obj for config file."""
        return Path(self.directory) / self._file_name


def new_service(name: str, services_dir: str | Path) -> Service:
    """Create a new service.

    Args:
        name (str): service name
        services_dir (str | Path): services directory

    Returns:
        Service: service instance
    """
    if not Path(services_dir).exists():
        raise FileNotFoundError(
            f"Services directory does not exist: {services_dir}"
        )
    service_path = Path(services_dir) / name.strip()
    try:
        service_path.mkdir(exist_ok=False)
    except FileExistsError as err:
        raise FileExistsError(
            f"Service directory already exists: {service_path}"
        ) from err
    service_obj = Service(name=name, directory=service_path)
    service_obj.settings.read_dict(
        {"SERVICE": {"name": name, "active": "True"}}
    )
    with open(service_obj.settings_file, "w", encoding="utf-8") as config_file:
        service_obj.settings.write(config_file)
    return service_obj


def load_service(directory: str | Path) -> Service:
    """Load a service."""
    service_obj = Service(directory=directory)
    service_obj.settings.read(service_obj.settings_file)
    if not Path(service_obj.directory).is_dir():
        raise FileNotFoundError(
            f"Service directory does not exist: {service_obj.directory}"
        )
    if not service_obj.settings_file.exists():
        raise FileNotFoundError(
            f"Settings file does not exist: {service_obj.settings_file}"
        )
    if not service_obj.settings.has_section("SERVICE"):
        raise NoSectionError("Service section must exist.")
    if not service_obj.settings.has_option("SERVICE", "name"):
        raise KeyError("Service.name must be set.")
    if service_obj.settings.get("SERVICE", "name") == "":
        raise ValueError("Service.name must not be empty.")

    service_obj.name = service_obj.settings.get("SERVICE", "name")
    return service_obj
