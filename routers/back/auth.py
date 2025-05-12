from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
import httpx
from settings import settings
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/auth", tags=["auth"])

LOGIN_URL = settings.LOGIN_USER_URL
REGISTER_URL = settings.REGISTER_USER_URL
DELETE_USER_URL = settings.DELETE_USER_URL
KEY_USER_URL = settings.KEY_USER_URL

@router.post("/login")
async def login_user(request: Request, response: Response):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username e senha são obrigatórios.")

    try:
        async with httpx.AsyncClient(verify=False) as client:
            auth_response = await client.post(LOGIN_URL, json={"username": username, "password": password})
            auth_response.raise_for_status()
        
    except httpx.HTTPStatusError as exc:
        return Response(content=exc.response.text, status_code=exc.response.status_code) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Auth Server: {str(e)}")

    auth_data = auth_response.json()
    token = auth_data.get("token")
    user_type = auth_data.get("type")

    if not token:
        raise HTTPException(status_code=500, detail="Token não recebido do Auth Server.")

    # Define o cookie com o token JWT
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Coloque True em produção com HTTPS
        samesite="lax",
        max_age=3600,  # 1 hora
        path="/"
    )

    return {"message": "Login bem-sucedido", "type": user_type}

@router.post("/logoff")
async def logoff_user(request: Request, response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout bem-sucedido"}


@router.post("/register")
async def register_user(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    user_type = data.get("type")

    if not username or not password or not user_type:
        raise HTTPException(status_code=400, detail="Campos obrigatórios ausentes.")

    try:
        async with httpx.AsyncClient(verify=False) as client:
            auth_response = await client.post(
                REGISTER_URL,
                json={"username": username, "password": password, "type": user_type},
                timeout=10
            )
            auth_response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar: {str(e)}")

    return JSONResponse(content={"message": "Usuário criado com sucesso"}, status_code=201)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.delete("/delete")
async def delete_user(request: Request):
    # Obtém o token do cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=400, detail="Token não encontrado no cookie")

    # Obtém os dados enviados no corpo da solicitação
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username e password são obrigatórios")

    # Faz a requisição para deletar o usuário
    async with httpx.AsyncClient(verify=False) as client:
        request = client.build_request("DELETE", DELETE_USER_URL, json={"username": username, "password": password}, headers={"Authorization": f"Bearer {token}"})
        response = await client.send(request)
    
    if response.status_code == 200:
        # Remove o cookie do token ao deletar o usuário
        response = JSONResponse({"message": "Usuário deletado com sucesso", "isDeleted": True})
        response.delete_cookie("access_token")  # Deleta o cookie "access_token"
        return response
    else:
        return JSONResponse({"message": "Usuário ou senha incorreta", "isDeleted": False}, status_code=401)

@router.get("/key")
async def get_user_key(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie")
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{KEY_USER_URL}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar: {str(e)}")

    return response.json()

