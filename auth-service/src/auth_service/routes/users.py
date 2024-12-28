"""Users routes module."""

from auth_service.lib.models import NewUserRequest
from auth_service.lib.models import UserLogin
from auth_service.lib.models import UserResponse
from auth_service.lib.users import users_lib
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi.security import HTTPBearer

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    on_startup=[users_lib.startup],
    on_shutdown=[users_lib.shutdown],
)


@user_router.post("/register")
async def register(user_data: NewUserRequest) -> UserResponse:
    """This is the register endpoint."""
    return users_lib.create_user(user_data)


@user_router.post("/login")
async def login(user_data: UserLogin, response: Response) -> UserResponse:
    """This is the login endpoint."""
    return users_lib.login_user(user_data, response)


@user_router.get("/logout")
async def logout(
    response: Response, token: str = Depends(HTTPBearer())
) -> None:
    """This is the logout endpoint."""
    return users_lib.logout_user(response, token)
