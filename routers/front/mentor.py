from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="paginas")
router = APIRouter(prefix="/mentor")

@router.get("/criarmentoria", response_class=HTMLResponse)
async def criarmentoria(request: Request):
    return templates.TemplateResponse("Mentor/criarmentoria.html", {"request": request})

@router.get("/my_mentorships", response_class=HTMLResponse)
async def my_mentorships(request: Request):
    return templates.TemplateResponse("Mentor/my_mentorships.html", {"request": request})
