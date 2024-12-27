"""Module for handling JWT tokens."""

import logging
from datetime import datetime
from datetime import timedelta

import jwt
from auth_service.const import ACCESS_TOKEN_EXPIRE_MINUTES
from auth_service.const import JWT_REFRESH_SECRET_KEY
from auth_service.const import JWT_SECRET_KEY
from auth_service.const import REFRESH_TOKEN_EXPIRE_MINUTES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_access_token(data: dict):
    """
    Creates an access token with an expiration time.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Creates a refresh token with the given data and expiration time.

    Args:
        data (dict): The data to include in the token payload.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, JWT_REFRESH_SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def decode_token(token: str, refresh: bool = False):
    """
    Decodes a JWT token and returns the payload if valid and not expired.

    Args:
        token (str): The JWT token to decode.
        refresh (bool, optional): Flag to indicate if the refresh token secret
        key should be used. Defaults to False.

    Returns:
        dict or None: The decoded JWT payload if valid and not expired,
        otherwise None.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    secret_key = JWT_REFRESH_SECRET_KEY if refresh else JWT_SECRET_KEY
    try:
        decoded_jwt = jwt.decode(token, secret_key, algorithms=["HS256"])
        return (
            decoded_jwt
            if decoded_jwt["exp"] >= datetime.now().timestamp()
            else None
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
