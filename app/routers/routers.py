from fastapi import APIRouter, HTTPException, Depends
from app.services.panteraservice import buscar_relatorio_pantera, buscar_relatorio_comparativo_safra
from app.services.iotebeservice import get_data_iotebe_from_api
from app.schemas.pantera import PanteraRelatorioResponse
from app.schemas.iotebe import IotebeSchema
from app.schemas.ionics import IonicsSchema
from app.schemas.fila_carregamento import FilaCarregamento
from app.services.ionicsservice import get_ionics_kpis
from app.services.fila_carregamentoservice import get_fila_carregamento_kpis
from app.oracle_database import get_session_ionics
from sqlalchemy.orm import Session
import httpx
from typing import List

router = APIRouter()

@router.get("/pantera/relatorio", response_model=List[PanteraRelatorioResponse])
async def get_relatorio_pantera():

    try:
        dados = await buscar_relatorio_pantera()
        return dados
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro na API do Pantera: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/pantera/comparativo-safra", response_model=List[PanteraRelatorioResponse])
async def get_pantera_comp_safra():

    try:
        dados = await buscar_relatorio_comparativo_safra()
        return dados
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro na API do Pantera: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/iotebe", response_model=list[IotebeSchema])
async def get_ioteb_indicator():
    try:
        dados = await get_data_iotebe_from_api()
        return dados
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro na api do IOTEBE: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/ionics", response_model=IonicsSchema)
async def get_ionics(session: Session = Depends(get_session_ionics)):
    try:
        dados = await get_ionics_kpis(session)
        return dados
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/fila-carregamento", response_model=list[FilaCarregamento])
async def get_fila_carregamento():
    try:
        dados = await get_fila_carregamento_kpis()
        return dados
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )