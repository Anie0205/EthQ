import os
import importlib
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()

from database import engine, Base
# Import all models here so tables can be created
from auth import models
from quizzes import models as quiz_models

# Automatically create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EthQ API", version="1.0.0")

# CORS Configuration - More permissive for debugging
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://eth-q.vercel.app"
).split(",")
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS if o.strip()]

# Add wildcard for development
if os.getenv("ENVIRONMENT") == "development":
    ALLOWED_ORIGINS.append("*")

print(f"DEBUG: Allowed origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: {request.method} {request.url}")
    print(f"DEBUG: Headers: {dict(request.headers)}")
    
    # Try to read body for POST requests
    if request.method == "POST":
        try:
            body = await request.body()
            print(f"DEBUG: Body length: {len(body)} bytes")
            print(f"DEBUG: Body preview: {body[:200]}")
        except Exception as e:
            print(f"DEBUG: Could not read body: {e}")
    
    response = await call_next(request)
    print(f"DEBUG: Response status: {response.status_code}")
    return response

def _safe_include(module_path: str, router_attr: str = "router", prefix: str = ""):
    """
    Try to import module_path and include its `router` into the FastAPI app
    if available. Failures are printed but don't stop the app from starting.
    """
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, router_attr, None)
        if router is not None:
            if prefix:
                app.include_router(router, prefix=prefix)
            else:
                app.include_router(router)
            print(f"✓ Including router from {module_path}")
        else:
            print(f"⚠ No router attribute '{router_attr}' found in {module_path}")
    except ModuleNotFoundError as e:
        print(f"⚠ Module not found: {module_path} - {e}")
    except Exception as e:
        print(f"✗ Could not import {module_path}: {e}")

# Include routers
print("\n=== Loading Routers ===")
_safe_include("auth.routes")           # auth/routes.py
_safe_include("quizzes.routes", prefix="/quizzes")  # quizzes/routes.py
_safe_include("routers.quiz", prefix="/quiz")       # routers/quiz.py
_safe_include("routers.analytics", prefix="/analytics")  # routers/analytics.py
print("======================\n")

# Root endpoint for health checks
@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "EthQ API is running",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n🚀 Starting server on port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
