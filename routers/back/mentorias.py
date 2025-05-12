from fastapi import APIRouter, Request, HTTPException, Response, Depends
from fastapi.responses import JSONResponse
import httpx
from settings import settings

router = APIRouter(prefix="/api/mentorias", tags=["mentorias"])

BASE_MENTORIA_URL = settings.MENTORIA_SERVER_URL

def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado no cookie")
    return token

@router.post("")
async def criar_mentoria(request: Request):
    token = get_token_from_cookie(request)
    data = await request.json()

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(f"{BASE_MENTORIA_URL}", json=data, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mentoria: {str(e)}")

    return JSONResponse(status_code=201, content=response.json())

@router.get("")
async def listar_mentorias_usuario(request: Request):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{BASE_MENTORIA_URL}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar mentorias: {str(e)}")

    return response.json()

@router.get("/{mentoria_id}")
async def buscar_mentoria(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{BASE_MENTORIA_URL}/{mentoria_id}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar mentoria: {str(e)}")

    return response.json()

@router.put("/{mentoria_id}")
async def atualizar_mentoria(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)
    data = await request.json()

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.put(f"{BASE_MENTORIA_URL}/{mentoria_id}", json=data, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar mentoria: {str(e)}")

    return response.json()

@router.delete("/{mentoria_id}")
async def deletar_mentoria(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(f"{BASE_MENTORIA_URL}/{mentoria_id}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar mentoria: {str(e)}")

    return Response(status_code=204)

@router.get("/topico/{nome_topico}")
async def listar_por_topico(request: Request, nome_topico: str):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{BASE_MENTORIA_URL}/topico/{nome_topico}", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar mentorias por tópico: {str(e)}")

    return response.json()

@router.post("/{mentoria_id}/mentorados")
async def adicionar_mentorado(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                f"{BASE_MENTORIA_URL}/{mentoria_id}/mentorados",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar mentorado: {str(e)}")

    return JSONResponse(status_code=201, content={"message": "Mentorado adicionado com sucesso"})

@router.delete("/{mentoria_id}/mentorados")
async def remover_mentorado(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)
    body = await request.json()
    mentorado_email = body.get("Mentorado_email")

    try:
        async with httpx.AsyncClient(verify=False) as client:
            request_httpx = client.build_request(
                "DELETE",
                f"{BASE_MENTORIA_URL}/{mentoria_id}/mentorados",
                json={"Mentorado_email": mentorado_email} if mentorado_email else None,
                headers={"Authorization": f"Bearer {token}"}
            )
            response = await client.send(request_httpx)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover mentorado: {str(e)}")

    return Response(status_code=204)

@router.get("/{mentoria_id}/mentorados")
async def listar_mentorados(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                f"{BASE_MENTORIA_URL}/{mentoria_id}/mentorados",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar mentorados: {str(e)}")

    return response.json()

@router.get("/{mentoria_id}/inscrito")
async def verificar_inscricao(request: Request, mentoria_id: int):
    token = get_token_from_cookie(request)

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                f"{BASE_MENTORIA_URL}/{mentoria_id}/inscrito",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return JSONResponse(status_code=exc.response.status_code, content=exc.response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar inscrição: {str(e)}")

    return response.json()
