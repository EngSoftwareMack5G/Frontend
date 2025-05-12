from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="paginas")
router = APIRouter(prefix="/mentorado")

@router.get("/business", response_class=HTMLResponse)
async def business(request: Request):
    return templates.TemplateResponse("Mentorado/business.html", {"request": request})

@router.get("/carrers", response_class=HTMLResponse)
async def carrers(request: Request):
    return templates.TemplateResponse("Mentorado/carrers.html", {"request": request})

@router.get("/finance", response_class=HTMLResponse)
async def finance(request: Request):
    return templates.TemplateResponse("Mentorado/finance.html", {"request": request})

@router.get("/leadership", response_class=HTMLResponse)
async def leadership(request: Request):
    return templates.TemplateResponse("Mentorado/leadership.html", {"request": request})

@router.get("/recents", response_class=HTMLResponse)
async def leadership(request: Request):
    return templates.TemplateResponse("Mentorado/recents.html", {"request": request})

@router.get("/inscricao", response_class=HTMLResponse)
async def inscricao(request: Request):
    return templates.TemplateResponse("Mentorado/inscricao.html", {"request": request})

@router.get("/mentorship/{mentorship_id}", response_class=HTMLResponse)
async def mentorship_detail(request: Request, mentorship_id: int):
    return templates.TemplateResponse("Mentorado/mentorship.html", {"request": request,})


@router.get("/my_mentorships", response_class=HTMLResponse)
async def my_mentorships(request: Request):
    return templates.TemplateResponse("Mentorado/my_mentorships.html", {"request": request})
