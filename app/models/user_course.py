from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


# User <-> Course: many-to-many
class UserCourse(Base):
    __tablename__ = "user_course"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="courses")
    course = relationship("Course", back_populates="users")
