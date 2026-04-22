from typing import Optional

import httpx
from app.core.config import settings
from fastapi import HTTPException, UploadFile

class LicensingClient:

    # função que cria um empreendimento na API do AKASHA para o post criar empreendimento
    async def create_development(self, name: str, description: str) -> dict:
    
        url = f"{settings.LICENSING_BASE_URL}/api/licensing/developments"
                
        payload = {      
        "name": name,       
        "description": description,             
        "e_ai": True            
        }

        headers = {        
        "x-api-key": settings.LICENSING_API_KEY
        }

        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(url, json=payload, headers=headers)           
            response.raise_for_status()
            return response.json()

    # função que manda os dados para a IA para o post classificar empreendimento
    async def mandar_dados(self, development_id: int) -> dict:
           url = f"{settings.LICENSING_BASE_URL}/api/licensing/ai/classify/full"

           headers = {
            "x-api-key": settings.LICENSING_API_KEY
           }
           
           payload = {
               "development_id": development_id
           }

           async with httpx.AsyncClient(timeout = 300) as client:
                response = await client.post(url, json=payload, headers=headers)      
                print(response.text)     
                response.raise_for_status()
                return response.json()
            
       
    # função que recebe os dados do formulário e envia para a IA para o post receber dados
    async def receber_dados(
        self,
        development_id: int,
        user_input: str,
        document: UploadFile,
        e_ai: str | None = None,
    ):
        url = f"{settings.LICENSING_BASE_URL}/api/licensing/ai/inputs"

        data = {
            "development_id": str(development_id),
            "user_input": user_input,
        }

        if e_ai is not None and str(e_ai).strip() != "":
            data["e_ai"] = str(e_ai).strip().lower()

        file_bytes = await document.read()

        files = {
            "document": (
                document.filename,
                file_bytes,
                document.content_type or "application/octet-stream"
            )
        }
        
        headers = {
            "x-api-key": settings.LICENSING_API_KEY
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, data=data, files=files,headers=headers)

            print("URL:", url)
            print("DATA:", data)
            print("FILE:", document.filename)
            print("STATUS:", response.status_code)
            print("BODY:", response.text)

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail={
                    "erro": "Erro ao chamar API externa",
                    "url": str(e.request.url),
                    "status_code": e.response.status_code,
                    "resposta": e.response.text,
                },
            )
            
        