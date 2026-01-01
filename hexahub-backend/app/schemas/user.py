"""User Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: Optional[str] = None  # Optional: for local auth
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserInDB(UserBase):
    """Schema for user as stored in database."""

    id: int
    is_active: bool
    is_superuser: bool
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """Schema for user in API responses."""

    pass  # Same as UserInDB, but separate for clarity


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""

    user_id: Optional[int] = None
    username: Optional[str] = None
