from datetime import datetime

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    course_id: int | None = None
    lesson_id: int | None = None
    content: str
    rating: int

class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
