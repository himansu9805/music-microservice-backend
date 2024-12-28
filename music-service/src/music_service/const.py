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
TRACKS_COLLECTION_NAME = os.getenv("COLLECTION_NAME", "tracks")
