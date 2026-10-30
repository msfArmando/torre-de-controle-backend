from pydantic import BaseModel
from datetime import datetime

class FilaCarregamento(BaseModel):
    organizacao: str
    quantidade_media_30_dias: float
    quantidade_media_8_dias: float
    tempo_carregamento_medio_30_dias: str | None
    tempo_carregamento_medio_8_dias: str | None
    fila: str
