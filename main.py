from fastapi import FastAPI
from routers.back import auth
from routers.front import mentor, mentorado, pages

app = FastAPI()

# Rotas do front-end (HTML)
app.include_router(pages.router)
app.include_router(mentor.router)
app.include_router(mentorado.router)

# Rotas do back-end (APIs, autenticação, etc.)
print(auth.router, "ROUTER")
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)