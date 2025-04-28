from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.models import Base

class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), primary_key=True)
    is_completed = Column(Boolean, default=False)
