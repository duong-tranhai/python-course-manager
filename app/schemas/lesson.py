from pydantic import BaseModel

class LessonBase(BaseModel):
    title: str
    content: str = ""

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    course_id: int

    model_config = {
        "from_attributes": True
    }

class SimpleLessonResponse(BaseModel):
    id: int
    title: str
    content: str

    model_config = {
        "from_attributes": True
    }