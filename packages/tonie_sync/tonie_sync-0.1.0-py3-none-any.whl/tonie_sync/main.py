import logging
import sys

from .sync_service import SyncService

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)


def main(query: str, creative_tonie_name: str):
    """Sync the files to the creative tonie based on the configuration."""
    sync_service = SyncService()
    sync_service.sync(query=query, creative_tonie_name=creative_tonie_name)


if __name__ == "__main__":
    query = "https://open.spotify.com/playlist/2nvhh0bzHb6wdO1yNGZTaY"
    creative_tonie_name = "Kreativ-Tonie"
    main(query=query, creative_tonie_name=creative_tonie_name)
