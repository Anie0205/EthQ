from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.routes import get_current_active_user
from auth import models as auth_models
from services.analytics_service import compute_user_analytics

router = APIRouter(tags=["Analytics"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: auth_models.User = Depends(get_current_active_user)):
    return compute_user_analytics(db, user_id=current_user.id)
