"""Restless settings."""

from pydantic import BaseSettings

FILE_ENCODING = "utf-8"


class Settings(BaseSettings):
    """Restless settings."""

    debug: bool = False
    file_encoding: str = "utf-8"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = FILE_ENCODING


settings = Settings()
