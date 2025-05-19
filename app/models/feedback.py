from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime

from app.models import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    content = Column(Text)
    rating = Column(Integer)  # e.g., 1–5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
