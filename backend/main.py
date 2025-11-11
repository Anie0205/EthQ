import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, Base, engine
from auth import routes as auth_routes
from auth import models as auth_models  # Import to register models
from quizzes import routes as quiz_routes
from quizzes import models as quiz_models  # Import to register models
from routers import quiz as ai_quiz_router
from routers import analytics as analytics_router

# Create database tables (imports above ensure all models are registered)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EthQ API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ], # Allow local dev origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to EthQ API", "status": "running"}

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(quiz_routes.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(ai_quiz_router.router)
app.include_router(analytics_router.router)
