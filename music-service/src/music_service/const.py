"""Constant values for the music service."""

import os

# API version
API_VERSION = "v1"

# MongoDB connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://127.0.0.1:27017/?directConnection=true&"
    "serverSelectionTimeoutMS=2000&appName=mongosh+2.3.7",
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "test")
METADATA_COLLECTION_NAME = os.getenv("COLLECTION_NAME", "music_metadata")

# MinIO configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "root")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "rootroot")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "music-bucket")

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
