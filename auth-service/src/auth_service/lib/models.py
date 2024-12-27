"""Models for the auth service."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Role(str, Enum):
    """Roles enum."""

    USER = "user"
    ADMIN = "admin"


class NewUser(BaseModel):
    """New user model."""

    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    role: Optional[Role] = Field(default=Role.USER, example="user")
    active: Optional[bool] = Field(default=True, example=True)
    created_at: Optional[datetime] = Field(
        default=datetime.now(),
        example="2021-01-01T00:00:00Z",
    )
    updated_at: Optional[datetime] = Field(
        default=datetime.now(),
        example="2021-01-01T00:00:00Z",
    )


class NewUserRequest(BaseModel):
    """New user register model."""

    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")


class UserResponse(BaseModel):
    """User response model."""

    email: str = Field(..., example="john.doe@example.com")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    role: str = Field(..., example="user")
    active: bool = Field(..., example=True)
    created_at: datetime = Field(..., example="2021-01-01T00:00:00Z")
    updated_at: datetime = Field(..., example="2021-01-01T00:00:00Z")


class UserLogin(BaseModel):
    """User login model."""

    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password")


class UserLogoutResponse(BaseModel):
    """User logout response model."""

    message: str = Field(..., example="Successfully logged out")
