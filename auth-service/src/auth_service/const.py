"""Constant values for the auth service."""

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
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "users")

# JWT configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "refresh_secret")
