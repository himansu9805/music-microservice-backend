"""Users routes module."""
from fastapi import APIRouter
from fastapi import Response

from auth_service.lib.models import UserLogin
from auth_service.lib.models import NewUserRequest
from auth_service.lib.models import UserResponse
from auth_service.lib.user import startup
from auth_service.lib.user import shutdown
from auth_service.lib.user import create_user
from auth_service.lib.user import login_user
from auth_service.lib.user import logout_user

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    on_startup=[startup],
    on_shutdown=[shutdown],
)


@user_router.post("/register")
async def register(user_data: NewUserRequest) -> UserResponse:
    """This is the register endpoint."""
    return create_user(user_data)


@user_router.post("/login")
async def login(user_data: UserLogin, response: Response) -> UserResponse:
    """This is the login endpoint."""
    return login_user(user_data, response)


@user_router.get("/logout")
async def logout(response: Response) -> None:
    """This is the logout endpoint."""
    return logout_user(response)
