"""Music routes module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Header
from fastapi import HTTPException
from fastapi import Security
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from music_service.lib.models import SongMetadata
from music_service.lib.models import SongsList
from music_service.lib.music import music_lib
from music_service.utils.token_manager import TokenManager

music_router = APIRouter(
    prefix="/music",
    tags=["music"],
    on_startup=[music_lib.startup],
    on_shutdown=[music_lib.shutdown],
)

security = HTTPBearer()
token_manager = TokenManager()


def validate_token(
    token: HTTPAuthorizationCredentials = Security(security),
) -> None:
    """Validate the token."""
    if not token_manager.validate(token.credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")


@music_router.get("/songs")
async def get_songs(token: str = Depends(HTTPBearer())) -> SongsList:
    """This is the get songs endpoint."""
    if not token_manager.validate(token.credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return music_lib.list_songs()


@music_router.get("/metadata/{song_id}")
async def get_song_metadata(
    song_id: str, token: HTTPAuthorizationCredentials = Depends(validate_token)
) -> SongMetadata:
    """This is the get song metadata endpoint."""
    return music_lib.get_song_metadata(song_id)


@music_router.get("/stream/{song_id}")
async def stream_song(
    song_id: str,
    music_range: str = Header(None),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
) -> StreamingResponse:
    """This is to stream the song."""
    return music_lib.stream_song(song_id, music_range)


@music_router.post("/upload")
async def upload_song(
    file: UploadFile = File(...),
    token: HTTPAuthorizationCredentials = Depends(validate_token),
) -> SongMetadata:
    """This is the upload song endpoint."""
    return music_lib.upload_song(file)
