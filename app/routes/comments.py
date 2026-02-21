from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))

from app.services.case_service import get_case_by_id

@router.get("/case/{case_id}/comments", response_class=HTMLResponse)
async def case_comments(request: Request, case_id: int):
    case = get_case_by_id(case_id)
    if not case:
        return RedirectResponse("/") # or show 404
    return templates.TemplateResponse("case_detail.html", {"request": request, "case": case})
