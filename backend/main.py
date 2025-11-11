import os
import importlib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Allow origins from env var ALLOWED_ORIGINS (comma-separated).
# Fallback includes common local dev origins and the Vercel frontend origin.
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://eth-q.vercel.app"
).split(",")
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _safe_include(module_path: str, router_attr: str = "router"):
    """
    Try to import module_path and include its `router` into the FastAPI app
    if available. Failures are printed but don't stop the app from starting.
    """
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, router_attr, None)
        if router is not None:
            app.include_router(router)
            print(f"Including router from {module_path}")
        else:
            print(f"No router attribute '{router_attr}' found in {module_path}")
    except Exception as e:
        print(f"Could not import {module_path}: {e}")

# Attempt to include routers from possible locations in the project.
_safe_include("auth.routes")        # auth/routes.py usually defines auth router
_safe_include("quizzes.routes")     # quizzes/routes.py (alternate location)
_safe_include("routers.quiz")       # routers/quiz.py (alternate location)
_safe_include("routers.analytics") # routers/analytics.py

# Add a simple root endpoint (optional)
@app.get("/")
def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
