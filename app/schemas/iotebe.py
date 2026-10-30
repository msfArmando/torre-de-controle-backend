from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class IotebeSchema(BaseModel):
    usina: str
    off_sla: int
    online_sensors: int
    total_sensors: int
    media_atual_horas: str
