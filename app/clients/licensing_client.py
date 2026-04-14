import httpx
from app.core.config import settings


class LicensingClient:

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

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)           
            response.raise_for_status()
            return response.json()

    
    
    
    async def receber_dados(self, development_id: int) -> dict:
           url = f"{settings.LICENSING_BASE_URL}/api/licensing/ai/classify/full"
           headers = {
            "x-api-key": settings.LICENSING_API_KEY
           }
           
           payload = {
               "development_id": development_id
           }

           async with httpx.AsyncClient(timeout = 60) as client:
                response = await client.post(url, json=payload, headers=headers)           
                response.raise_for_status()
                return response.json()
    