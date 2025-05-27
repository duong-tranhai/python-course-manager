from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Course(Base):
    """
        Represents a course in the system.

        Attributes:
            id (int): Unique identifier for the course.
            title (str): Title of the course.
            description (str): A brief description of the course content.
            creator_id (int): The user ID of the course creator (usually a teacher).

        Relationships:
            lessons (list): List of lessons associated with the course.
            users (list): List of users enrolled in the course.
    """
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
