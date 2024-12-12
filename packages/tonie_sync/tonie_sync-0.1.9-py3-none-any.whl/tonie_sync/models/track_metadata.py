import os
from pathlib import Path

from pydantic import BaseModel, field_validator
from spotdl.types.song import Song
from spotdl.utils.formatter import create_file_name

from ..utils import fix_filename


class TrackMetadata(BaseModel):
    """Metadata for a track downloaded from a music service."""

    artists: list[str]
    download_root: Path
    name: str
    duration_ms: int
    album_name: str | None = None
    image_url: str | None = None
    release_year: int | None = None
    disc_number: int | None = None
    track_number: int | None = None
    id: str | None = None
    is_playable: bool | None = None

    @field_validator("download_root")
    def validate_download_root(cls, v):
        """Validate the download root path."""
        return Path(os.path.abspath(v))

    @property
    def artist_and_name(self) -> str:
        """Return the artist and track name as a string."""
        return f"{self.artists[0]} - {self.name}"

    @property
    def duration_seconds(self) -> int:
        """Return the duration of the track in seconds."""
        if self.duration_ms is None:
            return 0
        return self.duration_ms // 1000

    @property
    def filename(self) -> str:
        """Return the filename for the downloaded track."""
        filename = fix_filename(f"{self.artist_and_name}.mp3")
        return filename

    @property
    def download_path(self) -> str:
        """Return the download path for the track."""
        return os.path.join(self.download_root, self.filename)


class SpotifyTrackMetadata(TrackMetadata):
    """Metadata for a track downloaded from Spotify."""

    pass


class SpotDLTrackMetadata(TrackMetadata):
    """Metadata for a track downloaded using SpotDL."""

    song: Song

    @property
    def filename(self) -> str:
        """Return the filename for the downloaded track.

        Note:
            The filename is generated using the `create_file_name` function from SpotDL.

        """
        return str(
            create_file_name(
                self.song,
                "{artists} - {title}.{output-ext}",
                "mp3",
                restrict=False,
                short=False,
            )
        )
