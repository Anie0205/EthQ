"""
Robust authentication dependencies that work with all request types.
This custom implementation avoids issues with HTTPBearer and OAuth2PasswordBearer
when dealing with multipart/form-data requests.
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from auth import models, utils

def get_user(db: Session, email: str):
    """Helper function to get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()

# Create a flexible bearer token extractor
security = HTTPBearer(auto_error=False)

async def get_token_from_header(
    authorization: Optional[str] = Header(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Extract Bearer token from Authorization header.
    Works with all request types including multipart/form-data.
    """
    token = None
    
    # Try to get token from Header directly (most reliable for multipart)
    if authorization:
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authorization scheme")
        except (ValueError, AttributeError):
            pass
    
    # Fallback to HTTPBearer (works for regular requests)
    if not token and credentials:
        token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_header)
) -> models.User:
    """
    Get current authenticated user from JWT token.
    This is a robust implementation that works with all request types.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate token
        payload = utils.decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        
        # Get user from database
        user = get_user(db, email=email)
        if user is None:
            raise credentials_exception
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging but don't expose details
        print(f"Authentication error: {type(e).__name__}: {str(e)}")
        raise credentials_exception

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Get current active user (additional check for active status)."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

