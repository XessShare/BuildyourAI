"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, TokenData, UserResponse
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token.

    Args:
        data: Data to encode in token
        expires_delta: Optional expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from token.

    Args:
        token: JWT token
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception

    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint (placeholder for Authentik OAuth).

    For MVP: Simple username/password login
    Production: Replace with Authentik OAuth flow

    Args:
        form_data: Login form data (username, password)
        db: Database session

    Returns:
        Token: JWT access token
    """
    # For MVP: Find user by username (no password validation yet)
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        # Create demo user if doesn't exist (MVP only)
        user = User(
            email=f"{form_data.username}@hexahub.local",
            username=form_data.username,
            full_name=f"Demo User {form_data.username}",
            is_active=True,
            oauth_provider="local",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/callback")
async def oauth_callback(code: str, state: str = None):
    """Authentik OAuth callback endpoint (placeholder).

    Args:
        code: OAuth authorization code
        state: OAuth state parameter

    Returns:
        dict: Placeholder response
    """
    # TODO: Implement Authentik OAuth flow
    return {
        "message": "OAuth callback - Implementation pending",
        "code": code,
        "state": state,
    }
