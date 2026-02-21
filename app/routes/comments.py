from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@router.get("/case/{case_id}/comments", response_class=HTMLResponse)
async def case_comments(request: Request, case_id: int):
    return templates.TemplateResponse("case_detail.html", {"request": request, "case_id": case_id})
