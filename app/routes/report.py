from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@router.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})
