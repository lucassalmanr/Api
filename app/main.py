from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 
from app.routes.licensing import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI( 
              title="API Local Simples",
              version="1.0.0" ) 

# 1. Defina as origens que podem acessar sua API
# Você pode colocar ["*"] para liberar para TODO MUNDO para desenvolvimento
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


app.include_router(router)

templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

BASE_DIR = Path(__file__).resolve().parent 
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/",tags=["Telas"])
async def index(request: Request, nome: str = "Visitante"):
    return templates.TemplateResponse(
    request=request,   
    name="teste.html",
    
    context={"request": request,  "nome": nome}
    )

