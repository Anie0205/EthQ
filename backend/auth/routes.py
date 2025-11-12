from fastapi import APIRouter, Depends, HTTPException, status, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from database import get_db
from auth import models, utils
from schemas import Token
from auth.dependencies import get_current_user, get_current_active_user

router = APIRouter()


def get_user(db: Session, email: str):
    """Helper function to get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


@router.post("/register", response_model=Token)
async def register_user(
    email: Optional[str] = Body(None), 
    password: Optional[str] = Body(None),
    form_email: Optional[str] = Form(None),
    form_password: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Prefer JSON body, fallback to form-data
    email = email or form_email
    password = password or form_password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    db_user = get_user(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")

    hashed_password = utils.get_password_hash(password)
    db_user = models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, email=form_data.username)
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
