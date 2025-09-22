from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import prompts, run
from app.routes import jobs as jobs_routes

app = FastAPI(title="NeuroPhish API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == ["*"] else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompts.router)
app.include_router(run.router)
app.include_router(jobs_routes.router)

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/__routes")
def _routes():
    return [r.path for r in app.router.routes]