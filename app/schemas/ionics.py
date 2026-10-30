from pydantic import BaseModel
from datetime import datetime

class IonicsSchema(BaseModel):
    quantidade_manual_teclado: int
    quantidade_auto_div: int
    quantidade_diesel_litros: float