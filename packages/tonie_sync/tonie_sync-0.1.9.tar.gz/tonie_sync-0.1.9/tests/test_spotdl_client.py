from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tonie_sync.clients.spotdl_client import SpotDLClientFactory


@pytest.fixture
def spotdl_client():
    """Return a SpotDLClient instance for testing."""
    with patch("spotdl.Spotdl", return_value=MagicMock()):
        return SpotDLClientFactory.create(
            client_id="test_id", client_secret="test_secret", target_directory=Path("test_music")
        )


def test_sanitize_query_with_valid_url(spotdl_client):
    """Test that the sanitize_query method returns the correct result for a valid URL."""
    url = "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P?si=abc123"
    expected_result = "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P"
    result = spotdl_client.sanitize_query(url)
    assert result == expected_result


def test_sanitize_query_with_valid_uri(spotdl_client):
    """Test that the sanitize_query method returns the correct result for a valid URI."""
    uri = "spotify:track:7ouMYWpwJ422jRcDASZB7P"
    expected_result = "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P"
    result = spotdl_client.sanitize_query(uri)
    assert result == expected_result


def test_sanitize_query_with_invalid_input(spotdl_client):
    """Test that the sanitize_query method raises a ValueError if the input is invalid."""
    invalid_input = "invalid_input"
    with pytest.raises(ValueError):
        spotdl_client.sanitize_query(invalid_input)
