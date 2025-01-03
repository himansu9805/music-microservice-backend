"""Users lib module."""

import logging

from auth_service import const
from auth_service.lib.models import NewUser
from auth_service.lib.models import UserLogin
from auth_service.lib.models import UserLogoutResponse
from auth_service.lib.models import UserResponse
from auth_service.utils.mongo_connect import MongoConnect
from auth_service.utils.password_handler import PasswordHandler
from auth_service.utils.token_manager import create_access_token
from auth_service.utils.token_manager import create_refresh_token
from auth_service.utils.token_manager import decode_token
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

logger = logging.getLogger(__name__)

MONGO_CLIENT = None
PASSWORD_HANDLER = None


def check_config():
    """
    Checks if required environment variables for MongoDB configuration are set.

    Raises:
        Exception: If any of the required environment variables (MONGO_URI,
        DATABASE_NAME, COLLECTION_NAME) are not set.
    """
    logger.info("Checking configuration")
    message = ""
    if not const.MONGO_URI:
        message += "MONGO_URI, "
    if not const.DATABASE_NAME:
        message += "DATABASE_NAME, "
    if not const.COLLECTION_NAME:
        message += "COLLECTION_NAME"
    if message:
        raise EnvironmentError(message + " environment variables not set")


def startup():
    """
    Initializes the MongoDB connection and password handler.
    """
    global MONGO_CLIENT, PASSWORD_HANDLER  # pylint: disable=global-statement
    check_config()
    MONGO_CLIENT = MongoConnect(
        uri=const.MONGO_URI,
        database=const.DATABASE_NAME,
        collection=const.COLLECTION_NAME,
    )
    if MONGO_CLIENT:
        logger.info("MongoDB connection established")
    PASSWORD_HANDLER = PasswordHandler()


def shutdown():
    """
    Shutdown function to close the MongoDB client connection if it exists.
    """
    if MONGO_CLIENT:
        MONGO_CLIENT.client.close()
        logger.info("MongoDB connection closed")


def create_user(user_data: NewUser) -> UserResponse | HTTPException:
    """
    Create a new user in the database.

    Args:
        user_data (NewUser): The data for the new user.

    Returns:
        UserResponse: The response containing the created user's data.
        HTTPException: If an error occurs during user creation.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    try:

        user_data_dict = user_data.model_dump()
        user_data_dict.pop("password")
        new_user = NewUser(
            **user_data_dict,
            password=PASSWORD_HANDLER.hash_password(user_data.password),
        )
        if MONGO_CLIENT.get_collection().insert_one(new_user.model_dump()):
            return UserResponse(**new_user.model_dump())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )
    except Exception as e:
        logger.error("Error creating user: %s", e)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error creating user")


def login_user(
    user_data: UserLogin, response: Response
) -> UserResponse | HTTPException:
    """
    Authenticates a user and sets access and refresh tokens in cookies.

    Args:
        user_data (UserLogin): The login data of the user.
        response (Response): The response object to set cookies.

    Returns:
        UserResponse: The response containing user data if login is successful.
        HTTPException: An exception if login fails.

    Raises:
        HTTPException: If the email or password is invalid or any other error
        occurs during login.
    """
    try:
        user_data_dict = user_data.model_dump()
        user = MONGO_CLIENT.get_collection().find_one(
            {"email": user_data_dict["email"]}
        )
        if user:
            if PASSWORD_HANDLER.verify_password(
                user_data.password, user["password"]
            ):
                user.pop("_id")
                user.pop("password")
                user["created_at"] = user["created_at"].isoformat()
                user["updated_at"] = user["updated_at"].isoformat()
                response.set_cookie(
                    key="access_token",
                    value=f"{create_access_token(user)}",
                )
                response.set_cookie(
                    key="refresh_token",
                    value=f"{create_refresh_token(user)}",
                )
                return UserResponse(**user)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
    except Exception as e:
        logger.error("Error logging in user: %s", e)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error logging in user")


def logout_user(response: Response, token: str) -> UserLogoutResponse:
    """
    Logs out the user by deleting authentication cookies.

    Args:
        response (Response): The HTTP response object to modify.

    Returns:
        UserLogoutResponse: A response object indicating the user has been
        logged out.
    """
    decoded_token = decode_token(token.credentials)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return UserLogoutResponse(message="User logged out")
