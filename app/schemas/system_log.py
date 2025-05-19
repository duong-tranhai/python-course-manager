# schemas/system_log.py
from pydantic import BaseModel
from datetime import datetime

class SystemLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    detail: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
