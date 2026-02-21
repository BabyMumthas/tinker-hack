import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.models.database import init_db
from app.routes.landing import router as landing_router
from app.routes.report import router as report_router
from app.routes.officer import router as officer_router
from app.routes.comments import router as comments_router
from app.config import config

import sys
import os

app = FastAPI(title="Missing Person AI")

# ── Session middleware (required for request.session) ─────────────────────────
app.add_middleware(
    SessionMiddleware,
    secret_key=config.SECRET_KEY,
    session_cookie="officer_session",
    max_age=3600,   # 1 hour
)

# ── Static files ──────────────────────────────────────────────────────────────
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount uploads folder at /uploads (separate from /static to avoid prefix conflict)
upload_dir = config.UPLOAD_FOLDER
os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# ── DB init on startup ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    init_db()

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(landing_router)
app.include_router(report_router)
app.include_router(officer_router)
app.include_router(comments_router)
