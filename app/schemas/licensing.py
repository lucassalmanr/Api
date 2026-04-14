from pydantic import BaseModel

class EmpreendimentoRequest(BaseModel):
    name: str
    description: str
    type: str
    stats: str
    area: int


class EmpreendimentoResponse(BaseModel):
    id:int
    message: str
    data: dict

class DevelopmentCreateRequest(BaseModel):
    name: str
    description: str
    e_ia: bool
    
class FormData(BaseModel):
    development_id: int
    user_input: dict
    
class Classification(BaseModel):
    development_id: int