"""Song Information Module."""

import logging

import spotipy
from music_service import const
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)


class SongInformation:
    """Song Information Class."""

    def __init__(self):
        """Initialize the song information class."""
        self.spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                const.SPOTIFY_CLIENT_ID, const.SPOTIFY_CLIENT_SECRET
            )
        )

    def _search_song(self, song_name: str) -> dict:
        """
        Search for a song on Spotify.

        Args:
            song_name (str): The name of the song to search for.

        Returns:
            dict: The search results for the song.
        """
        logger.info("Searching for song %s", song_name)
        return self.spotify_client.search(song_name)

    def _get_song_info(self, song_id: str) -> dict:
        """
        Get the information for a song from Spotify.

        Args:
            song_id (str): The ID of the song to get information for.

        Returns:
            dict: The information for the song.
        """
        logger.info("Getting information for song %s", song_id)
        raw_details = self.spotify_client.track(song_id)
        return {
            "name": raw_details["name"],
            "artist": raw_details["artists"][0]["name"],
            "album": raw_details["album"]["name"],
            "release_date": raw_details["album"]["release_date"],
            "duration": raw_details["duration_ms"],
            "popularity": raw_details["popularity"],
        }

    def get_song_metadata(self, song_name: str) -> dict:
        """
        Get the metadata for a song.

        Args:
            song_name (str): The name of the song to get metadata for.

        Returns:
            dict: The metadata for the song.
        """
        try:
            song_id = self._search_song(song_name)["tracks"]["items"][0]["id"]
            return self._get_song_info(song_id)
        except Exception as e:
            logger.error("Error getting song metadata: %s", e)
            return None


if __name__ == "__main__":
    song_info = SongInformation()
    print(song_info.get_song_metadata("Linkin Park - Castle Of Glass.mp3"))
