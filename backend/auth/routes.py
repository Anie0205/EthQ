from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel, EmailStr, Field
import json

from database import get_db
from auth import models, utils
from schemas import Token
from auth.dependencies import get_current_user, get_current_active_user

router = APIRouter()


def get_user(db: Session, email: str):
    """Helper function to get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


# Pydantic model for JSON registration
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


@router.post("/register", response_model=Token)
async def register_user(request: Request, db: Session = Depends(get_db)):
    """Register a new user with email and password"""
    
    try:
        # Read raw body
        body_bytes = await request.body()
        print(f"DEBUG: Received body: {body_bytes[:200]}")
        
        # Parse JSON
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)
        print(f"DEBUG: Parsed JSON: {body_dict}")
        
        # Validate with Pydantic
        register_data = RegisterRequest(**body_dict)
        email = register_data.email
        password = register_data.password
        
        print(f"DEBUG: Validated - email: {email}, password length: {len(password)}")
        
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode failed: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        print(f"ERROR: Validation failed: {e}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    
    # Check if user already exists
    existing_user = get_user(db, email=email)
    if existing_user:
        print(f"ERROR: Email {email} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    try:
        hashed_password = utils.get_password_hash(password)
        db_user = models.User(email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"SUCCESS: Created user {email}")
    except Exception as e:
        db.rollback()
        print(f"ERROR: Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    # Generate access token
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    print(f"SUCCESS: Generated token for {email}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Login with username (email) and password to get access token"""
    
    print(f"DEBUG: Login attempt for: {form_data.username}")
    
    user = get_user(db, email=form_data.username)
    if not user:
        print(f"ERROR: User {form_data.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        print(f"ERROR: Invalid password for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print(f"SUCCESS: Login successful for {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
