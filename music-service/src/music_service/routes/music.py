"""Music routes module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from music_service.lib.music import music_lib

music_router = APIRouter(
    prefix="/music",
    tags=["music"],
    on_startup=[music_lib.startup],
    on_shutdown=[music_lib.shutdown],
)


@music_router.get("/songs")
async def get_songs(token: str = Depends(HTTPBearer())) -> None:
    """This is the get songs endpoint."""
    return music_lib.list_songs(token)
