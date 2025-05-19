from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models import Base


class AttendanceSession(Base):
    __tablename__ = 'attendance_sessions'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    type = Column(String)  # manual / auto / quiz-based
    summary = Column(String, nullable=True)  # 🆕 Add this line

    course = relationship('Course')
    lesson = relationship('Lesson')

class StudentAttendance(Base):
    __tablename__ = 'student_attendances'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    attendance_session_id = Column(Integer, ForeignKey('attendance_sessions.id'))
    status = Column(String)  # present / absent
    check_in_time = Column(DateTime)
    updated_at = Column(DateTime, default=None)

    user = relationship('User')
    session = relationship('AttendanceSession')

    __table_args__ = (
        UniqueConstraint('attendance_session_id', 'user_id', name='uix_session_student'),
    )

