"""Models for the auth service."""

from pydantic import BaseModel
from pydantic import Field


class SongAlbumArt(BaseModel):
    """Song album art model."""

    height: int = Field(..., example=640)
    width: int = Field(..., example=640)
    url: str = Field(..., example="https://example.com/image.jpg")


class SongMetadata(BaseModel):
    """Song metadata model."""

    song_id: str = Field(..., example="songid1")
    title: str = Field(..., example="title1")
    artist: str = Field(..., example="artist1")
    album: str = Field(..., example="album1")
    release_date: str = Field(..., example="2021-01-01")
    images: list[SongAlbumArt] = Field(
        ...,
        example=[
            {
                "height": 640,
                "width": 640,
                "url": "https://example.com/image.jpg",
            }
        ],
    )


class SongsList(BaseModel):
    """Songs list model."""

    songs: list[SongMetadata] = Field(
        ...,
        examples=[
            [
                {
                    "song_id": "songid1",
                    "title": "title1",
                    "artist": "artist1",
                    "album": "album1",
                    "release_date": "2021-01-01",
                },
                {
                    "song_id": "songid2",
                    "title": "title2",
                    "artist": "artist2",
                    "album": "album2",
                    "release_date": "2021-01-02",
                },
            ]
        ],
    )


class SongInfo(BaseModel):
    """Song info model."""

    title: str = Field(None, example="title1")
    artist: str = Field(None, example="artist1")
    album: str = Field(None, example="album1")
