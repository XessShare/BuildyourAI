"""User database model."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication and user management."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # Optional: for local auth
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # "authentik", "google", etc.
    oauth_id = Column(String, nullable=True)  # External user ID

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
