"""Music routes module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from music_service.lib.music import shutdown
from music_service.lib.music import startup

music_router = APIRouter(
    prefix="/music",
    tags=["music"],
    on_startup=[startup],
    on_shutdown=[shutdown],
)


@music_router.get("/songs")
async def get_songs(token: str = Depends(HTTPBearer())) -> None:
    """This is the get songs endpoint."""
    return {"songs": ["song1", "song2", "song3"]}
