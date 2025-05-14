from fastapi import APIRouter, Request, HTTPException, Depends, Response, UploadFile, File, Form
from fastapi.responses import JSONResponse
import httpx
from settings import settings # Assume que settings.py tem USERS_SERVER_URL
from fastapi.security import OAuth2PasswordBearer # Não usado diretamente aqui, mas pode ser para outros endpoints
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/users", tags=["users"])

BASE_USERS_URL = settings.USERS_SERVER_URL + "/perfil"# Ex: "http://localhost:8001/api/internal/users" ou similar

@router.post("")
async def create_profile(
    request: Request,
    response: Response,
    nome: str = Form(...),
    descricao: str = Form(...),
    genero: str = Form(...),
    foto: UploadFile = File(...)
):
    # Obtém o token do cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie. Faça login novamente.") 

    headers = {
        "Authorization": f"Bearer {token}"
    }

    form_data_to_send = {
        "nome": (None, nome),
        "descricao": (None, descricao),
        "genero": (None, genero),
        "foto": (foto.filename, await foto.read(), foto.content_type)
    }
    try:
        async with httpx.AsyncClient() as client:
            service_response = await client.post(
                BASE_USERS_URL, 
                files=form_data_to_send, 
                headers=headers,
                timeout=10.0
            )
            service_response.raise_for_status()
            try:
                response_data = service_response.json()
            except Exception:
                response_data = service_response.text
            return JSONResponse(
                content=response_data,
                status_code=service_response.status_code
            )
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mentoria: {str(e)}")
    return JSONResponse(status_code=201, content=response.json())

@router.get("")
async def get_profile(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie. Faça login novamente.")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            service_response = await client.get(BASE_USERS_URL, headers=headers, timeout=10.0)
            service_response.raise_for_status()
            return JSONResponse(content=service_response.json(), status_code=service_response.status_code)
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar perfil: {str(e)}")


@router.get("/imagem")
async def get_profile_image(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie. Faça login novamente.")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            service_response = await client.get(f"{BASE_USERS_URL}/imagem", headers=headers, timeout=10.0)
            service_response.raise_for_status()
            media_type = service_response.headers.get("content-type", "application/octet-stream")
            return Response(content=service_response.content, media_type=media_type)
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar imagem do perfil: {str(e)}")


@router.put("")
async def update_profile(
    request: Request,
    nome: str = Form(None),
    descricao: str = Form(None),
    genero: str = Form(None),
    foto: UploadFile = File(None)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie. Faça login novamente.")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "nome": (None, nome) if nome else None,
        "descricao": (None, descricao) if descricao else None,
        "genero": (None, genero) if genero else None,
        "foto": (foto.filename, await foto.read(), foto.content_type) if foto else None
    }
    # Remove chaves com valor None
    files = {k: v for k, v in files.items() if v is not None}

    try:
        async with httpx.AsyncClient() as client:
            service_response = await client.put(BASE_USERS_URL, files=files, headers=headers, timeout=10.0)
            service_response.raise_for_status()
            return JSONResponse(content=service_response.json(), status_code=service_response.status_code)
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar perfil: {str(e)}")


@router.delete("")
async def delete_profile(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie. Faça login novamente.")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            service_response = await client.delete(BASE_USERS_URL, headers=headers, timeout=10.0)
            if service_response.status_code != 204:
                return JSONResponse(status_code=service_response.status_code, content=service_response.text)
            return Response(status_code=204)
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar perfil: {str(e)}")

class EmailRequest(BaseModel):
    email: EmailStr

@router.get("/nome")
async def obter_nome_por_email(request: EmailRequest):
    """
    Retorna o nome de um perfil a partir do e-mail informado no corpo da requisição.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_USERS_URL}/nome/{request.email}"
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Perfil não encontrado")
            raise HTTPException(status_code=500, detail="Erro ao consultar serviço de perfil")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Serviço de perfil indisponível")

    nome = response.json()
    return nome