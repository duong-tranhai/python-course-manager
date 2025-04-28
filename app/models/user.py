from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    created_courses = relationship("Course", back_populates="creator")

    # store the courses which user is enrolling
    courses = relationship("UserCourse", back_populates="user")
