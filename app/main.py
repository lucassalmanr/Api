from fastapi import FastAPI 
from app.routes.licensing import router 

app = FastAPI( 
              title="API Local Simples",
              version="1.0.0" ) 


app.include_router(router)
