from datetime import datetime

from sqlalchemy.orm import Session

from app.models.student_attendance import AttendanceSession, StudentAttendance
from app.schemas import attendance as schema


def create_attendance_session(data: schema.AttendanceSessionCreate, db: Session):
    session = AttendanceSession(
        course_id=data.course_id,
        lesson_id=data.lesson_id,
        start_time=data.start_time,
        end_time=data.end_time,
        type=data.type
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def mark_attendance(user_id: int, session_id: int, db: Session):
    existing = db.query(StudentAttendance).filter_by(
        user_id=user_id, attendance_session_id=session_id
    ).first()

    if existing:
        return existing  # already marked

    record = StudentAttendance(
        user_id=user_id,
        attendance_session_id=session_id,
        status="present",
        timestamp=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_attendance_by_course(course_id: int, db: Session):
    return (
        db.query(StudentAttendance)
        .join(AttendanceSession)
        .filter(AttendanceSession.course_id == course_id)
        .all()
    )
