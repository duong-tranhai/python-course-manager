from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)

    # store the list of enrolled users - many-to-many
    users = relationship("UserCourse", back_populates="course")

    # store the id of the course creator - many-to-one
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_courses")

    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
