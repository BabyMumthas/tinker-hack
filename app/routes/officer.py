from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@router.get("/officer-login", response_class=HTMLResponse)
async def officer_login(request: Request):
    return templates.TemplateResponse("officer_login.html", {"request": request})

@router.get("/officer-dashboard", response_class=HTMLResponse)
async def officer_dashboard(request: Request):
    return templates.TemplateResponse("officer_dashboard.html", {"request": request})
