# Tonie Sync

A package to sync Spotify playlists to creative tonies.

> This package is not affiliated with Spotify or Tonies. It uses the Spotify and
> Tonie APIs to sync playlists to creative tonies. The package is intended for
> personal use only. Use at your own risk.
>
> The package is heavily inspired by
> [spoonie](https://github.com/Seji64/spoonie).

## Installation

```bash
pip install tonie-sync
```

This package requires these additional dependencies:

- ffmpeg

## Usage

```python
from tonie_sync import SyncService

query = [
    "joji - test drive",  # search term
    "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",   # track
    "https://open.spotify.com/playlist/2nvhh0bzHb6wdO1yNGZTaY",  # playlist
    ]
creative_tonie_name = "My Creative Tonie"

sync_service = SyncService()  # Create a new SyncService instance with settings from environment variables
sync_service.sync(query=query, creative_tonie_name=creative_tonie_name)  # Sync the Spotify playlists to the creative tonies
```

## Environment Variables

| Environment Variable  | Description                      | Example Value         |
| --------------------- | -------------------------------- | --------------------- |
| SPOTIFY_CLIENT_ID     | Spotify account username         | 123456789             |
| SPOTIFY_CLIENT_SECRET | Spotify account password         | this_is_very_secret   |
| TONIE_USERNAME        | Tonie account email              | my_email@provider.com |
| TONIE_PASSWORD        | Tonie account password           | another_secret        |
| TONIE_HOUSEHOLD       | Name of the Tonie household      | My Household          |
| target_directory      | Path to the local data directory | ./.local              |
