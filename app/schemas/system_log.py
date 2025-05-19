# schemas/system_log.py
from datetime import datetime

from pydantic import BaseModel


class SystemLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    detail: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
