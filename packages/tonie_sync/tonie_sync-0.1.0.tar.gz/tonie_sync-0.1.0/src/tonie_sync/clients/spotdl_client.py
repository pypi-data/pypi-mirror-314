import logging
import os
import re
from pathlib import Path

from spotdl import Spotdl
from spotdl.types.song import Song

from ..models import SpotDLTrackMetadata


class SpotDLClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        target_directory: Path = Path("music"),
    ):
        self.original_directory = os.getcwd()
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        self.target_directory = target_directory
        self.spotdl = Spotdl(client_id=client_id, client_secret=client_secret)
        self.spotdl.downloader.settings["output"] = "{artists} - {title}.{output-ext}"
        self._logger = logging.getLogger(__name__)

    def search_and_download(self, query: list[str] | str) -> list[SpotDLTrackMetadata]:
        if isinstance(query, str):
            query = [query]
        sanitized_queries = []
        for q in query:
            sanitized_queries.append(self.sanitize_query(q))
        self._logger.info("Searching for songs with query [ '%s' ]", sanitized_queries)
        songs = self.spotdl.search(sanitized_queries)
        songs_metadata = self._get_track_metadata(songs)
        songs_to_download = [
            song_metadata.song for song_metadata in songs_metadata if not os.path.exists(song_metadata.download_path)
        ]
        self._logger.info(
            "Downloading [ %d/%d ] songs to [ '%s' ]",
            len(songs_to_download),
            len(songs),
            self.target_directory,
        )
        os.chdir(self.target_directory)
        self.spotdl.download_songs(songs_to_download)
        os.chdir(self.original_directory)
        return songs_metadata

    def sanitize_query(self, query: str) -> str:
        """Parse a Spotify URL or URI and return the ID and object type.

        Args:
            search_input: The Spotify URL or URI to parse.

        Returns:
            dict[str, str]: A dict with the Id and type of the object.

        Example:
            >>> regex_input_for_urls('https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P?si=abc123')
            >>> "track", "7ouMYWpwJ422jRcDASZB7P"

        Raises:
            ValueError: If no ID is found in the input.
        """
        OBJECT_TYPE_TO_BASE_URL = {
            "playlist": "https://open.spotify.com/playlist",
            "track": "https://open.spotify.com/track",
            "episode_info": "https://open.spotify.com/episode",
            "show": "https://open.spotify.com/show",
        }
        # Regular expression to match Spotify URLs and URIs
        pattern = re.compile(
            r"(?:spotify:(?P<type>\w+):(?P<id>\w+))|(?:https://open.spotify.com/(?P<type2>\w+)/(?P<id2>\w+))"
        )
        match = pattern.search(query)

        if match:
            object_type = match.group("type") or match.group("type2")
            object_id = match.group("id") or match.group("id2")
            base_url = OBJECT_TYPE_TO_BASE_URL.get(object_type)
        else:
            raise ValueError("No ID found in the input.")
        if base_url is None:
            raise ValueError(f"Unsupported object type [ '{object_type}' ]")
        url = f"{base_url}/{object_id}"
        return url

    def _get_track_metadata(self, songs: list[Song]) -> list[SpotDLTrackMetadata]:
        metadata = []
        for song in songs:
            metadata.append(
                SpotDLTrackMetadata(
                    artists=song.artists,
                    download_root=self.target_directory,
                    name=song.name,
                    duration_ms=song.duration * 1000,  # convert to ms
                    album_name=song.album_name,
                    image_url=song.cover_url,
                    release_year=song.year,
                    disc_number=song.disc_number,
                    track_number=song.track_number,
                    id=song.song_id,
                    is_playable=True,  # always True for Spotify songs, not provided by SpotDL
                    song=song,
                )
            )
        return metadata
