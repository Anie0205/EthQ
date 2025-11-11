import os
import importlib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="EthQ API", version="1.0.0")

# CORS Configuration - Allow your Vercel frontend
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://eth-q.vercel.app"
).split(",")
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS if o.strip()]

# Add wildcard for development if needed
if os.getenv("ENVIRONMENT") == "development":
    ALLOWED_ORIGINS.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Include routers - try both locations
print("\n=== Loading Routers ===")
_safe_include("auth.routes")           # auth/routes.py (no prefix, routes handle their own paths)
_safe_include("quizzes.routes", prefix="/quizzes")  # quizzes/routes.py with /quizzes prefix
_safe_include("routers.quiz", prefix="/quiz")       # routers/quiz.py with /quiz prefix  
_safe_include("routers.analytics", prefix="/analytics")  # routers/analytics.py with /analytics prefix
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