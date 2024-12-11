# from unittest.mock import MagicMock, patch

# import pytest
# from tonie_sync.clients.spotify_client import SpotifyClient


# @pytest.fixture
# def spotify_client():
#     with patch.object(SpotifyClient, "_get_spotify_session", return_value=MagicMock()):
#         return SpotifyClient(username="test", password="test", target_directory="test")


# def test_parse_url_with_valid_url(spotify_client):
#     url = "https://open.spotify.com/track/7ouMYWpwJ422jRcDASZB7P?si=abc123"
#     expected_result = (
#         "track",
#         "7ouMYWpwJ422jRcDASZB7P",
#     )
#     result = spotify_client.parse_url(url)
#     assert result == expected_result


# def test_parse_url_with_valid_uri(spotify_client):
#     uri = "spotify:track:7ouMYWpwJ422jRcDASZB7P"
#     expected_result = (
#         "track",
#         "7ouMYWpwJ422jRcDASZB7P",
#     )
#     result = spotify_client.parse_url(uri)
#     assert result == expected_result


# def test_parse_url_with_invalid_input(spotify_client):
#     invalid_input = "invalid_input"
#     with pytest.raises(ValueError):
#         spotify_client.parse_url(invalid_input)
