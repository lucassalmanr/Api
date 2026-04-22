#apenas para teste
from app.schemas.licensing import EmpreendimentoRequest

class LicensingService:

    def __init__(self):
        self.ultimo_id = 0

    # função que processa o empreendimento para o teste
    def processar_empreendimento(self, payload: EmpreendimentoRequest) -> dict:
        return {
            "id": self.definir_ultimoid(),
            "message": f"Empreendimento recebido com sucesso area:{payload.area} e status: {payload.stats}",
            "data": {
                "name": payload.name,
                "description": payload.description}
            }
    
   
    
    def mostrarsucesso(self, payload: EmpreendimentoRequest):
        return {
            "message": "API Funcionando"
        }

    def definir_ultimoid(self):
        
        self.ultimo_id += 1
        return self.ultimo_id
