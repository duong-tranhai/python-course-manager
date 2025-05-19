from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.schemas.course import CourseResponse
from app.schemas.lesson import LessonResponse


class AttendanceSessionCreate(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    type: str  # manual / auto / quiz-based

class AttendanceSessionResponse(AttendanceSessionCreate):
    id: int
    model_config = {
        "from_attributes": True
    }

class AttendanceSessionWithCourseLesson(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    type: str
    course: CourseResponse
    lesson: Optional[LessonResponse] = None
    model_config = {
        "from_attributes": True
    }

class StudentAttendanceResponse(BaseModel):
    id: int
    user_id: int
    attendance_session_id: int
    status: str
    check_in_time: datetime
    updated_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }

class AttendancePatch(BaseModel):
    user_id: int               # student being updated
    present: bool              # True = present, False = absent

class AttendanceBulkUpdate(BaseModel):
    session_id: int
    updates: List[AttendancePatch] = Field(..., min_items=1)