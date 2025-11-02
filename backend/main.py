from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import quiz

app = FastAPI(title="Ethical Quiz Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Ethical Quiz Generator API", "status": "running", "docs": "/docs"}

app.include_router(quiz.router)
if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
