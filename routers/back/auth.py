from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login_user(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    # Aqui você faria a requisição ao auth server (por ex, via httpx)
    # E retornaria o token ou erro
    return JSONResponse({"token": "fake-jwt-token-for-" + username})
