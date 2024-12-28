"""Models for the auth service."""

from pydantic import BaseModel
from pydantic import Field


class SongsList(BaseModel):
    """Songs list model."""

    songs: list[str] = Field(..., example=["song1", "song2", "song3"])


class SongMetadata(BaseModel):
    """Song metadata model."""

    song_id: str = Field(..., example="songid1")
    title: str = Field(..., example="title1")
    artist: str = Field(..., example="artist1")
    album: str = Field(..., example="album1")
    release_date: str = Field(..., example="2021-01-01")
