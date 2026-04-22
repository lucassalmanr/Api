
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
import httpx
from app.clients.licensing_client import LicensingClient
from app.schemas.licensing import Classification, DevelopmentCreateRequest, FormData
from app.services.licensing_service import LicensingService
from app.schemas.licensing import EmpreendimentoRequest, EmpreendimentoResponse
from typing import Annotated, Optional
import json



router = APIRouter(prefix="/api/v1/licenciamento", tags=["Licenciamento"])
service = LicensingService()
client = LicensingClient()

# Verifica se a API está funcionando corretamente
@router.get("/health")
def health():
    return {"status": "ok"}

# apenas para teste local
@router.post("/empreendimentos-teste", response_model=EmpreendimentoResponse)
def criar_empreendimento_teste(payload: EmpreendimentoRequest):
    return service.processar_empreendimento(payload)



# Recebe as informações básicas e cadastra um novo empreendimento na API do AKASHA (`/api/licensing/developments`).
@router.post("/criar-empreendimento")
async def criar_empreendimento(payload: DevelopmentCreateRequest):
    try:
        dados = await client.create_development(
            payload.name,
            payload.description
        )
        dados2 = dados.get('data', {})
        ultimo_id = dados2.get('id')
        
        return {
            "name": payload.name,
            "description": payload.description,
            "id": ultimo_id
        }
    # tratamento de erros
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 422:
            raise HTTPException(
                status_code=422,
                detail="Erro de validação na API externa"
            )

        elif status_code == 500:
            raise HTTPException(
                status_code=500,
                detail="Erro interno na API externa"
            )
        
        elif status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Não autorizado: Verifique sua chave de API"
            )

        elif status_code == 201:
            raise HTTPException(
                status_code=201,
                detail="Empreendimento criado com sucesso"
            )
        
        elif status_code == 200:
            raise HTTPException(
                status_code=200,
                detail="Empreendimento atualizado com sucesso"
            )

        else:
            raise HTTPException(
                status_code=status_code,
                detail=f"Erro HTTP inesperado: {e.response.text}"
            )

   
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Erro de conexão com a API externa"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )        


# Recebe o arquivo e as informações do formulário e envia para a API oficial do AKASHA (`/api/licensing/forms`).
@router.post(f"/forms")
async def forms(
    development_id: Annotated[str, Form()],
    user_input: Annotated[str, Form()],
    document: Annotated[UploadFile, File()],
    e_ai: Annotated[bool, Form()]   
    ):
            return await client.receber_dados(development_id, user_input, document, e_ai)


# Recebe o ID do empreendimento e envia para a API oficial do AKASHA (`/api/licensing/ai/classify/full`).
@router.post("/api/licensing/ai/classify/full")
async def Classificacao(payload: Classification):
    try:
        dados_classificados = await client.mandar_dados(payload.development_id)
        data = dados_classificados.get('data', {})
        classificacao = { "group": data.get('group'),
            "activity": data.get('activity'),
            "criterios": data.get('criteria'),
            "porte": data.get('classification') or "M", 
            "modalidade": data.get('modality')}
        # cria um arquivo .json com as infomações adquiridas o nome é relativo ao id
        with open(f"C:/Users/lucas.resende/Downloads/primeira API/app/data/data{payload.development_id}.json", "w", encoding="utf-8") as arquivo:
            json.dump(classificacao, arquivo, ensure_ascii=False, indent=4) 
        return classificacao

    # tratamento de erros
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 422:
            raise HTTPException(
                status_code=422,
                detail="Erro de validação na API externa"
            )

        elif status_code == 500:
            raise HTTPException(
                status_code=500,
                detail="Erro interno na API externa"
            )
        
        elif status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Não autorizado: Verifique sua chave de API"
            )

        elif status_code == 201:
            raise HTTPException(
                status_code=201,
                detail="Classificação realizada com sucesso"
            )
        
        elif status_code == 200:
            raise HTTPException(
                status_code=200,
                detail="Classificação atualizada com sucesso"
            )

        else:
            raise HTTPException(
                status_code=status_code,
                detail=f"Erro HTTP inesperado: {e.response.text}"
            )

