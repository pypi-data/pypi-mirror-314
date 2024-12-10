import logging
import os
from pathlib import Path

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_settings import BaseSettings

from .clients import SpotDLClient, TonieClient


class SyncServiceConfig(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    tonie_username: EmailStr
    tonie_password: str
    tonie_household: str
    target_directory: Path

    @field_validator("target_directory", mode="before")
    def validate_target_directory(cls, v):
        return Path(v)


class SyncService(BaseModel):
    config: SyncServiceConfig = SyncServiceConfig()

    def sync(self, creative_tonie_name: str, query: str):
        spotify_client = SpotDLClient(
            client_id=self.config.spotify_client_id,
            client_secret=self.config.spotify_client_secret,
            target_directory=self.config.target_directory,
        )
        tonie_client = TonieClient(
            email=self.config.tonie_username,
            password=self.config.tonie_password,
            household=self.config.tonie_household,
        )

        if not os.path.exists(self.config.target_directory):
            logging.info(f"Creating download folder {self.config.target_directory}")
            os.makedirs(self.config.target_directory)

        download_tracks_metadata = spotify_client.search_and_download(query=query)

        tonie_client.update_creative_tonie(creative_tonie_name, download_tracks_metadata)
