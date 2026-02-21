from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from app.services.case_service import save_case

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@router.get("/report", response_class=HTMLResponse)
async def report_get(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

@router.post("/report")
async def report_post(
    request: Request,
    missing_full_name: str = Form(...),
    gender: str = Form(None),
    age: int = Form(None),
    missing_state: str = Form(None),
    missing_city: str = Form(None),
    pin_code: str = Form(None),
    missing_date: str = Form(None),
    missing_time: str = Form(None),
    description: str = Form(None),
    complainant_name: str = Form(...),
    relationship: str = Form(None),
    complainant_phone: str = Form(...),
    address_line1: str = Form(None),
    missing_image: UploadFile = File(...)
):
    form_data = {
        "missing_full_name": missing_full_name,
        "gender": gender,
        "age": age,
        "missing_state": missing_state,
        "missing_city": missing_city,
        "pin_code": pin_code,
        "missing_date": missing_date,
        "missing_time": missing_time,
        "description": description,
        "complainant_name": complainant_name,
        "relationship": relationship,
        "complainant_phone": complainant_phone,
        "address_line1": address_line1
    }
    
    save_case(form_data, missing_image)
    
    return RedirectResponse(url="/", status_code=303)
