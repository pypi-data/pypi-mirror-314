# SpotifyClient is removed from the library for now, because authentication
# using username + password does no longer work and zeroconf is not implemented yet.
# import logging
# import os
# import re
# import tempfile
# import time
# from pathlib import Path

# import ffmpy
# import music_tag
# import requests
# from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality
# from librespot.core import Session
# from librespot.metadata import TrackId

# from ..models import SpotifyTrackMetadata
# from ..models.track_metadata import TrackMetadata
# from ..utils import format_seconds


# class SpotifyClient:
#     PLAYLISTS_URL = "https://api.spotify.com/v1/playlists"
#     TRACKS_URL = "https://api.spotify.com/v1/tracks"
#     EPISODE_INFO_URL = "https://api.spotify.com/v1/episodes"
#     SHOWS_URL = "https://api.spotify.com/v1/shows"

#     def __init__(self, username, password, target_directory):
#         self.username = username
#         self.password = password
#         self.session = self._get_spotify_session(target_directory)
#         self._logger = logging.getLogger(__name__)
#         self.download_root = os.path.join(target_directory, "download")
#         os.makedirs(self.download_root, exist_ok=True)

#     def download_tracks(self, download_root: str, download_url: str) -> list[SpotifyTrackMetadata]:
#         """Download all tracks from a Spotify URL.

#         Args:
#             download_root: The path to the data directory.
#             download_url: The URL to download from.

#         Returns:
#             A list of metadata for the downloaded tracks.

#         """
#         url_type, spotify_id = self.parse_url(download_url)
#         if url_type == "playlist":
#             tracks_metadata = self.get_playlist_tracks_metadata(spotify_id)
#         return tracks_metadata

#     def _get_spotify_session(self, target_directory):
#         """Initialize the Spotify session.

#         Args:
#             target_directory: The path to the data directory.

#         """
#         cred_location = os.path.join(target_directory, "credentials.json")
#         if Path(cred_location).is_file():
#             try:
#                 conf = Session.Configuration.Builder().set_store_credentials(False).build()
#                 return Session.Builder(conf).stored_file(cred_location).create()
#             except RuntimeError:
#                 pass
#         else:
#             conf = Session.Configuration.Builder().set_stored_credential_file(cred_location).build()
#             return Session.Builder(conf).user_pass(self.username, self.password).create()

#     def _get_auth_header(self):
#         """Get the authorization header for the Spotify API.

#         Returns:
#             dict: The authorization header.

#         """
#         token = self.session.tokens().get_token(
#             "user-read-email",
#             "playlist-read-private",
#             "user-library-read",
#             "user-follow-read",
#         )
#         header = {
#             "Authorization": f"Bearer {token.access_token}",
#             "Content-Type": "application/json",
#             "app-platform": "WebPlayer",
#         }
#         return header

#     def _make_request(self, url, params=None):
#         """Make a request to the Spotify API.

#         Args:
#             url: The URL to make the request to.
#             params: The parameters to include in the request.

#         Returns:
#             dict: The response from the request.

#         Raises:
#             ValueError: If the response from the URL is invalid or if parsing the response fails.

#         """
#         header = self._get_auth_header()
#         response = requests.get(url, headers=header, params=params)
#         response.raise_for_status()
#         return response.json()

#     def parse_url(self, search_input: str) -> tuple[str, str]:
#         """Parse a Spotify URL or URI and return the ID and object type.

#         Args:
#             search_input: The Spotify URL or URI to parse.

#         Returns:
#             dict[str, str]: A dict with the Id and type of the object.

#         Example:
#             >>> regex_input_for_urls('https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P?si=abc123')
#             >>> "track", "7ouMYWpwJ422jRcDASZB7P"

#         Raises:
#             ValueError: If no ID is found in the input.

#         """
#         # Regular expression to match Spotify URLs and URIs
#         pattern = re.compile(
#             r"(?:spotify:(?P<type>\w+):(?P<id>\w+))|(?:https://open.spotify.com/(?P<type2>\w+)/(?P<id2>\w+))"
#         )
#         match = pattern.search(search_input)

#         if match:
#             object_type = match.group("type") or match.group("type2")
#             object_id = match.group("id") or match.group("id2")
#             return object_type, object_id

#         raise ValueError("No ID found in the input.")

#     def get_playlist_tracks_metadata(self, playlist_id: str) -> list[SpotifyTrackMetadata]:
#         """Retrieve all tracks from a specific Spotify playlist.

#         This function fetches all tracks from a playlist identified by its ID from Spotify.
#         It handles pagination to retrieve all tracks by making multiple requests if necessary.

#         Args:
#             playlist_id: The ID of the playlist as a string.

#         Returns:
#             A list of tracks (list[dict]), where each track is represented as a dictionary containing its metadata.

#         Raises:
#             ValueError: If the response from the URL is invalid or if parsing the response fails.

#         """
#         tracks = []
#         offset = 0
#         limit = 100

#         while True:
#             resp = self._make_request(
#                 url=f"{self.PLAYLISTS_URL}/{playlist_id}/tracks",
#                 params={"limit": limit, "offset": offset},
#             )
#             offset += limit
#             tracks.extend(resp["items"])
#             if len(resp["items"]) < limit:
#                 break
#         tracks_metadata = []
#         for track in tracks:
#             track_metadata = self.get_track_metadata(track["track"]["id"])
#             tracks_metadata.append(track_metadata)
#         return tracks_metadata

#     def get_track_metadata(self, track_id) -> SpotifyTrackMetadata:
#         """Retrieve metadata for a specific Spotify track.

#         Args:
#             track_id: The ID of the track as a string.

#         Returns:
#             dict: Metadata for the track.

#         Raises:
#             ValueError: If the response from the URL is invalid or if parsing the response fails.

#         """
#         try:
#             response = self._make_request(
#                 url=f"{self.TRACKS_URL}",
#                 params={"ids": track_id, "market": "from_token"},
#             )
#             track = response["tracks"][0]
#             artists = []
#             for data in track["artists"]:
#                 artists.append(data["name"])
#             track_metadata = SpotifyTrackMetadata(
#                 download_root=self.download_root,
#                 artists=artists,
#                 album_name=track["album"]["name"],
#                 name=track["name"],
#                 image_url=track["album"]["images"][0]["url"],
#                 release_year=track["album"]["release_date"].split("-")[0],
#                 disc_number=track["disc_number"],
#                 track_number=track["track_number"],
#                 id=track["id"],
#                 is_playable=track["is_playable"],
#                 duration_ms=track["duration_ms"],
#             )
#         except Exception as e:
#             raise ValueError(f"Failed to parse TRACKS_URL [ '{track_id}' ] response: {str(e)}") from e
#         return track_metadata

#     def process_track(self, track_metadata: SpotifyTrackMetadata) -> SpotifyTrackMetadata:
#         """Process a track from Spotify.

#         Determine the target location and download the track to the target location, if
#         it does not already exist and is playable.

#         Args:
#             track_metadata: The metadata for the track to process.

#         Returns:
#             SpotifyTrackMetadata: The metadata of the downloaded track.

#         """
#         try:
#             logging.info(f"Processing [ '{track_metadata.name}' ] ...")
#             if os.path.exists(track_metadata.download_path):
#                 self._logger.info("... track already exists => Skipping download.")
#                 return track_metadata

#             if not track_metadata.is_playable:
#                 self._logger.warning("... track is not playable => Skipping download.")
#                 return track_metadata
#             self.download_track(track_metadata)
#             return track_metadata

#         except Exception as e:
#             self._logger.error(f"... failed to download track [ '{track_metadata.name}' ]: {str(e)}")
#             return track_metadata

#     def download_track(
#         self,
#         track_metadata: SpotifyTrackMetadata,
#     ):
#         """Download a track from Spotify."""
#         self._logger.info("... downloading")
#         download_tempfile = tempfile.NamedTemporaryFile(delete=False)
#         librespot_track = TrackId.from_base62(track_metadata.id)
#         stream = self.session.content_feeder().load(
#             librespot_track, VorbisOnlyAudioQuality(AudioQuality.HIGH), False, None
#         )
#         total_size = stream.input_stream.size
#         time_start = time.time()
#         downloaded = 0
#         b = 0
#         while b < 5:
#             data = stream.input_stream.stream().read(20000)
#             download_tempfile.write(data)
#             downloaded += len(data)
#             b += 1 if data == b"" else 0
#             if True:  # if args.ban_protection:
#                 delta_real = time.time() - time_start
#                 delta_want = (downloaded / total_size) * (track_metadata.duration_ms / 5000)
#                 if delta_want > delta_real:
#                     time.sleep(delta_want - delta_real)
#         time_downloaded = time.time()
#         logging.info(f"... finished download in {format_seconds(int(time_downloaded - time_start))}!")
#         self._convert_to_mp3(download_tempfile.name, track_metadata.download_path)
#         self._set_metadata(track_metadata.download_path, track_metadata)

#     def _set_metadata(self, file_path, track_metadata: TrackMetadata) -> None:
#         tags = music_tag.load_file(file_path)
#         tags["albumartist"] = track_metadata.artists[0]
#         tags["artist"] = ", ".join(track_metadata.artists)
#         tags["tracktitle"] = track_metadata.name
#         tags["album"] = track_metadata.album_name
#         tags["year"] = track_metadata.release_year
#         tags["discnumber"] = track_metadata.disc_number
#         tags["tracknumber"] = track_metadata.track_number
#         try:
#             if track_metadata.image_url:
#                 image_url = track_metadata.image_url
#                 img = requests.get(image_url).content
#                 tags["artwork"] = img
#         except Exception as e:
#             logging.error(f"Failed to download image: {str(e)}")
#         tags.save()
#         return

#     def _convert_to_mp3(self, temp_filename, filename) -> None:
#         """Convert raw audio into a playable file.

#         This function uses ffmpy to convert a raw audio file into a playable format.
#         It sets the codec to 'libmp3lame' and the bitrate to '160k' unless the codec is 'copy'.
#         The function handles errors related to the ffmpeg executable not being found.

#         Args:
#             temp_filename: The path to the temporary raw audio file as a string.
#             filename: The path to the output playable audio file as a string.

#         Returns:
#             None

#         """
#         self._logger.info("... converting Track Audio Format")

#         output_params = ["-c:a", "libmp3lame", "-b:a", "160k"]

#         try:
#             ff_m = ffmpy.FFmpeg(
#                 global_options=["-y", "-hide_banner", "-loglevel error"],
#                 inputs={temp_filename: None},
#                 outputs={filename: output_params},
#             )
#             ff_m.run()

#         except ffmpy.FFExecutableNotFoundError:
#             logging.warning("Skipping conversion - ffmpeg not found!")
#         except ffmpy.FFRuntimeError as e:
#             logging.error(f"Failed to convert file: {str(e)}")
