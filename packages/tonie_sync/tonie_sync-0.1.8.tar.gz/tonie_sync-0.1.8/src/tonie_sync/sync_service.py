import logging
import os

from .clients import SpotDLClientFactory, TonieClient


class SyncService:
    """Responsible for syncing music from Spotify to a Toniebox."""

    def __init__(
        self,
        spotify_client_id: str | None,
        spotify_client_secret: str | None,
        tonie_username: str | None,
        tonie_password: str | None,
        tonie_household: str | None,
        target_directory: str | None,
    ):
        self.spotify_client_id = os.environ.get("spotify_client_id", spotify_client_id)
        self.spotify_client_secret = os.environ.get("spotify_client_secret", spotify_client_secret)
        self.tonie_username = os.environ.get("tonie_username", tonie_username)
        self.tonie_password = os.environ.get("tonie_password", tonie_password)
        self.tonie_household = os.environ.get("tonie_household", tonie_household)
        self.target_directory = os.environ.get("target_directory", target_directory)
        self.spotify_client = SpotDLClientFactory.create(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret,
            target_directory=self.target_directory,
        )

    def sync(self, creative_tonie_name: str, query: str):
        """Sync music from Spotify to a Toniebox.

        Args:
            creative_tonie_name: The name of the creative Tonie.
            query: The search query to find songs on Spotify.

        """
        tonie_client = TonieClient(
            email=self.tonie_username,
            password=self.tonie_password,
            household=self.tonie_household,
        )

        if not os.path.exists(self.target_directory):
            logging.info(f"Creating download folder {self.target_directory}")
            os.makedirs(self.target_directory)

        download_tracks_metadata = self.spotify_client.search_and_download(query=query)

        tonie_client.update_creative_tonie(creative_tonie_name, download_tracks_metadata)
