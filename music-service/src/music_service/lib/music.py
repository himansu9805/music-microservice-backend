"""Music lib module."""

import logging
import uuid
from typing import Generator

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import Header
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from music_service import const
from music_service.lib.models import SongMetadata
from music_service.lib.models import SongsList
from music_service.utils.mongo_connect import MongoConnect
from music_service.utils.song_information import SongInformation
from music_service.utils.token_manager import TokenManager

logger = logging.getLogger(__name__)
logger.addFilter(logging.Filter("music_service.lib.music"))


class MusicLib:
    """Music library class."""

    def __init__(self):
        """Initialize the music library."""
        self.token_manager = None
        self.s3_client = None
        self.metadata_mongo_client = None
        self.password_handler = None
        self.song_info_client = None

    def _check_config(self):
        """Check if the required environment variables are set."""
        logger.info("Checking configuration")
        message = ""
        if not const.MINIO_ENDPOINT:
            message += "MINIO_ENDPOINT, "
        if not const.MINIO_ACCESS_KEY:
            message += "MINIO_ACCESS_KEY, "
        if not const.MINIO_SECRET_KEY:
            message += "MINIO_SECRET_KEY, "
        if not const.MINIO_BUCKET_NAME:
            message += "MINIO_BUCKET_NAME, "
        if not const.MONGO_URI:
            message += "MONGO_URI, "
        if not const.DATABASE_NAME:
            message += "DATABASE_NAME, "
        if not const.METADATA_COLLECTION_NAME:
            message += "METADATA_COLLECTION_NAME"
        if message:
            raise EnvironmentError(message + "environment variables not set")

    def startup(self):
        """This is the startup function of the music library."""
        self._check_config()
        self.token_manager = TokenManager()
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"http://{const.MINIO_ENDPOINT}",
            aws_access_key_id=const.MINIO_ACCESS_KEY,
            aws_secret_access_key=const.MINIO_SECRET_KEY,
        )
        self.metadata_mongo_client = MongoConnect(
            const.MONGO_URI,
            const.DATABASE_NAME,
            const.METADATA_COLLECTION_NAME,
        )
        self.song_info_client = SongInformation()
        logger.info("Music library started")

    def shutdown(self):
        """This is the shutdown function of the music library."""
        self.token_manager = None
        self.s3_client = None
        logger.info("Music library stopped")

    def _stream_file_from_s3(
        self, bucket_name: str, file_key: str, start: int, end: int
    ) -> Generator[bytes, None, None]:
        """Stream a file from S3."""
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name, Key=file_key, Range=f"bytes={start}-{end}"
            )
            file_body = response["Body"]
            while chunk := file_body.read(8192):
                yield chunk
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail=f"Error streaming file: {str(e)}"
            ) from e

    def list_songs(self, token: str) -> SongsList:
        """List all the songs."""
        if not self.token_manager.validate(token.credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=const.MINIO_BUCKET_NAME
            )
            songs = [obj["Key"] for obj in response.get("Contents", [])]
            return SongsList(songs=songs)
        except NoCredentialsError:
            raise HTTPException(
                status_code=500, detail="No valid credentials"
            ) from None
        except self.s3_client.exceptions.NoSuchBucket:
            raise HTTPException(
                status_code=404, detail="Bucket not found"
            ) from None
        except self.s3_client.exceptions.NoSuchKey:
            raise HTTPException(
                status_code=404, detail="File not found"
            ) from None
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail=f"Error listing songs: {str(e)}"
            ) from e

    def stream_music(self, file_key: str, music_range: str = Header(None)):
        """Stream music."""
        try:
            file_head = self.s3_client.head_object(
                Bucket=const.MINIO_BUCKET_NAME, Key=file_key
            )
            file_size = file_head["ContentLength"]
        except NoCredentialsError:
            raise HTTPException(
                status_code=500, detail="No valid credentials"
            ) from None
        except self.s3_client.exceptions.NoSuchKey:
            raise HTTPException(
                status_code=404, detail="File not found"
            ) from None
        if music_range:
            try:
                range_start, range_end = music_range.replace(
                    "bytes=", ""
                ).split("-")
                range_start = int(range_start)
                range_end = int(range_end) if range_end else file_size - 1
                if range_start >= file_size or range_end >= file_size:
                    raise HTTPException(
                        status_code=416,
                        detail="Requested range not satisfiable",
                    )
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid Range Header"
                ) from None
            headers = {
                "Content-Range": (
                    f"bytes {range_start}-{range_end}/{file_size}"
                ),
                "Accept-Ranges": "bytes",
                "Content-Length": str(range_end - range_start + 1),
            }

            return StreamingResponse(
                self._stream_file_from_s3(
                    const.MINIO_BUCKET_NAME, file_key, range_start, range_end
                ),
                media_type="audio/mpeg",
                status_code=206,
                headers=headers,
            )
        return StreamingResponse(
            self._stream_file_from_s3(
                const.MINIO_BUCKET_NAME, file_key, 0, file_size - 1
            ),
            media_type="audio/mpeg",
        )

    def get_song_metadata(self, song_id: str) -> SongMetadata:
        """Get the metadata of a song."""
        try:
            metadata = self.metadata_mongo_client.get_collection().find_one(
                {"song_id": song_id}
            )
            if not metadata:
                raise HTTPException(
                    status_code=404, detail="Metadata not found"
                )
            metadata.pop("_id")
            return SongMetadata(**metadata)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail=f"Error getting metadata: {str(e)}"
            ) from e

    def upload_song(self, file: UploadFile) -> SongMetadata:
        """Upload a song."""
        logger.info("Uploading song %s", file.filename)
        file_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, file.filename))
        try:
            self.s3_client.upload_fileobj(
                file.file,
                const.MINIO_BUCKET_NAME,
                file_name,
            )
        except NoCredentialsError:
            raise HTTPException(
                status_code=500, detail="No valid credentials"
            ) from None
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail=f"Error uploading file: {str(e)}"
            ) from e
        try:
            filtered_file_name = file.filename
            if (
                filtered_file_name.split(" ")[0].endswith(".")
                and filtered_file_name.split(" ")[0][:-1].isdigit()
            ):
                filtered_file_name = " ".join(
                    filtered_file_name.split(" ")[1:]
                )
            if "." in filtered_file_name:
                filtered_file_name = filtered_file_name.rsplit(".", 1)[0]
            song_details = self.song_info_client.get_song_metadata(
                filtered_file_name
            )
            metadata = {
                "song_id": file_name,
                "title": file.filename,
                "artist": "Unknown",
                "album": "Unknown",
                "release_date": "Unknown",
            }
            if song_details:
                metadata = {
                    "song_id": file_name,
                    "title": song_details["name"],
                    "artist": song_details["artist"],
                    "album": song_details["album"],
                    "release_date": song_details["release_date"],
                }
            self.metadata_mongo_client.get_collection().insert_one(metadata)
            return SongMetadata(**metadata)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail=f"Error saving metadata: {str(e)}"
            ) from e


music_lib = MusicLib()
