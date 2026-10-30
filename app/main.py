from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import routers

app = FastAPI(
    title="Torre de Controle - Grupo Olho D'Água",
    description="API do dashboard operacional",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(routers.router, prefix=settings.API_PREFIX)