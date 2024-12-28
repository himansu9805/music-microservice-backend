"""Music lib module."""

import logging

from fastapi import HTTPException
from music_service.utils.token_manager import TokenManager

logger = logging.getLogger(__name__)


class MusicLib:
    """Music library class."""

    def __init__(self):
        """Initialize the music library."""
        self.token_manager = None

    def startup(self):
        """This is the startup function of the music library."""
        logger.info("Music library started")
        self.token_manager = TokenManager()

    def shutdown(self):
        """This is the shutdown function of the music library."""
        logger.info("Music library stopped")

    def list_songs(self, token: str):
        """List all the songs."""
        logger.info(token)
        if not self.token_manager.validate(token.credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")
        return {"songs": ["song1", "song2", "song3"]}


music_lib = MusicLib()
