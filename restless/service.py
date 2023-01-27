"""Main module for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"

# %%
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from lib_standard import EnhancedConfigParser

# %%
SETTINGS_FILE = os.environ.get("SERVICE_SETTINGS_FILE", "settings.ini")


@dataclass
class AnsibleService:
    """Ansible service class."""

    name: str
    config_path: str | Path
    description: str = field(default="")
    config: EnhancedConfigParser = field(
        default_factory=EnhancedConfigParser, init=False, repr=True
    )

    # No init
    active: bool = field(default=True, init=False, repr=True)
    last_loaded_on: str | None = field(default=None, init=False, repr=True)

    def load(self) -> None:
        """Load state."""
        # Check if the service is active
        if not self.active:
            raise RuntimeError("Service is not active.")

        # Check if the service path is valid
        if not (Path(self.config_path) / SETTINGS_FILE).is_file():
            raise ValueError(
                f"Can not access settings file: {self.config_path}"
            )
        settings_path: Path = Path(self.config_path) / SETTINGS_FILE
        self.config.read(settings_path)
        self.last_loaded_on = str(datetime.now())

    def save(self) -> None:
        """Save state."""
        raise NotImplementedError("Service.save() must be implemented.")


# %%
