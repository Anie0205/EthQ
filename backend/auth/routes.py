from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from auth import models, utils
from schemas import TokenData, UserCreate, UserLogin, Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not token:
            print("DEBUG: No token provided")
            raise credentials_exception
        payload = utils.decode_access_token(token)
        if payload is None:
            print("DEBUG: Token decode failed - invalid token or SECRET_KEY mismatch")
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            print("DEBUG: No email in token payload")
            raise credentials_exception
        token_data = TokenData(email=email)
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Exception in get_current_user: {type(e).__name__}: {e}")
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        print(f"DEBUG: User not found for email: {token_data.email}")
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")

    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
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
