from fastapi import FastAPI 
from app.routes.licensing import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI( 
              title="API Local Simples",
              version="1.0.0" ) 

# 1. Defina as origens que podem acessar sua API
# Você pode colocar ["*"] para liberar para TODO MUNDO (útil em desenvolvimento)
origins = ["*"]

# 2. Adicione o middleware ao app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Recomendo "*" para testes locais rápidos
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, PUT, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)


app.include_router(router)
