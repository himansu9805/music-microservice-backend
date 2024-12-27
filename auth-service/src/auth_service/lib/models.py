"""Models for the auth service."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional


class Role(str, Enum):
    """Roles enum."""

    user = "user"
    admin = "admin"


class NewUser(BaseModel):
    """New user model."""

    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    role: Optional[Role] = Field(default=Role.user, example="user")
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
    active: bool = Field(True, example=True)
    created_at: datetime = Field(..., example="2021-01-01T00:00:00Z")
    updated_at: datetime = Field(..., example="2021-01-01T00:00:00Z")


class UserLogin(BaseModel):
    """User login model."""

    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password")


class UserLogoutResponse(BaseModel):
    """User logout response model."""

    message: str = Field(..., example="Successfully logged out")
