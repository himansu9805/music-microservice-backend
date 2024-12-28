"""Music routes module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Header
from fastapi import UploadFile
from fastapi.security import HTTPBearer
from music_service.lib.models import SongMetadata
from music_service.lib.models import SongsList
from music_service.lib.music import music_lib

music_router = APIRouter(
    prefix="/music",
    tags=["music"],
    on_startup=[music_lib.startup],
    on_shutdown=[music_lib.shutdown],
)


@music_router.get("/songs")
async def get_songs(token: str = Depends(HTTPBearer())) -> SongsList:
    """This is the get songs endpoint."""
    return music_lib.list_songs(token)


@music_router.get("/metadata/{song_id}")
async def get_song_metadata(song_id: str) -> SongMetadata:
    """This is the get song metadata endpoint."""
    return music_lib.get_song_metadata(song_id)


@music_router.get("/stream/{song_id}")
async def get_song(song_id: str, music_range: str = Header(None)) -> None:
    """This is the get song endpoint."""
    return music_lib.stream_music(song_id, music_range)


@music_router.post("/upload")
async def upload_song(file: UploadFile = File(...)) -> SongMetadata:
    """This is the upload song endpoint."""
    return music_lib.upload_song(file)
