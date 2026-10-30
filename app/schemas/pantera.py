from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class PanteraRelatorioResponse(BaseModel):
    id_report: str
    id_acionamento: str
    dt_acionamento: str
    dt_chegada: str
    intervalo: Optional[timedelta] = None
    total_segundos: float
    total_minutos: float

class PanteraIndicator(BaseModel):
    isCritical: bool