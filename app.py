from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="paginas")

# Redireciona da raiz para /home
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/home")

# Root
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/feedbacks", response_class=HTMLResponse)
async def feedbacks(request: Request):
    return templates.TemplateResponse("feedbacks.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):    
    return templates.TemplateResponse("about.html", {"request": request})

#Mentor
@app.get("/mentor/criarmentoria", response_class=HTMLResponse)
async def criarmentoria(request: Request):
    return templates.TemplateResponse("Mentor/criarmentoria.html", {"request": request})

@app.get("/mentor/my_mentorships", response_class=HTMLResponse)
async def my_mentorships(request: Request):
    return templates.TemplateResponse("Mentor/my_mentorships.html", {"request": request})

#Mentorado
@app.get("/mentorado/business", response_class=HTMLResponse)
async def business(request: Request):
    return templates.TemplateResponse("Mentorado/business.html", {"request": request})

@app.get("/mentorado/carrers", response_class=HTMLResponse)
async def carrers(request: Request):
    return templates.TemplateResponse("Mentorado/carrers.html", {"request": request})

@app.get("/mentorado/finance", response_class=HTMLResponse)
async def finance(request: Request):
    return templates.TemplateResponse("Mentorado/finance.html", {"request": request})

@app.get("/mentorado/leadership", response_class=HTMLResponse)
async def leadership(request: Request):
    return templates.TemplateResponse("Mentorado/leadership.html", {"request": request})

@app.get("/mentorado/recents", response_class=HTMLResponse)
async def leadership(request: Request):
    return templates.TemplateResponse("Mentorado/recents.html", {"request": request})

@app.get("/mentorado/inscricao", response_class=HTMLResponse)
async def inscricao(request: Request):
    return templates.TemplateResponse("Mentorado/inscricao.html", {"request": request})

@app.get("/mentorado/mentorship", response_class=HTMLResponse)
async def my_mentorships(request: Request):
    return templates.TemplateResponse("Mentorado/mentorship.html", {"request": request})

@app.get("/mentorado/my_mentorships", response_class=HTMLResponse)
async def my_mentorships(request: Request):
    return templates.TemplateResponse("Mentorado/my_mentorships.html", {"request": request})
