import os
import sys

# ── Ensure project root is on path ───────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.database import init_db
from app.routes.landing import router as landing_router
from app.routes.report import router as report_router
from app.routes.officer import router as officer_router
from app.routes.comments import router as comments_router
from app.config import config

# ── App factory ───────────────────────────────────────────────────────────────
app = FastAPI(title="Missing Person AI")

# Static files
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialise DB on startup
@app.on_event("startup")
async def startup():
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    init_db()

# Routers
app.include_router(landing_router)
app.include_router(report_router)
app.include_router(officer_router)
app.include_router(comments_router)
