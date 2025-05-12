from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="paginas")
router = APIRouter()

@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/home")
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.get("/feedbacks", response_class=HTMLResponse)
async def feedbacks(request: Request):
    return templates.TemplateResponse("feedbacks.html", {"request": request})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):    
    return templates.TemplateResponse("about.html", {"request": request})