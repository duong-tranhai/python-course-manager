import io
from datetime import datetime
from sqlite3 import IntegrityError

import pandas as pd
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse, JSONResponse

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.student_attendance import AttendanceSession, StudentAttendance
from app.models.user import User
from app.schemas import attendance as schema
from app.schemas.attendance import AttendanceBulkUpdate


# Create new attendance session by teacher
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

# Check in session by student
def mark_attendance(user_id: int, session_id: int, db: Session):
    # Optional: Validate session timing
    session = db.query(AttendanceSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Attendance session not found")

    now = datetime.now()
    if session.start_time > now or session.end_time < now:
        raise HTTPException(status_code=400, detail="Session is not currently active")

    # Attempt to insert record
    try:
        record = StudentAttendance(
            user_id=user_id,
            attendance_session_id=session_id,
            status="present",
            check_in_time=datetime.now()
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()  # Very important!
        raise HTTPException(status_code=400, detail="You have already checked in to this session")

# get all the sessions list by teacher
def get_sessions_by_teacher(db: Session, current_user: User):
    sessions = (
        db.query(AttendanceSession)
        .join(Course, AttendanceSession.course_id == Course.id)
        .outerjoin(AttendanceSession.lesson)
        .filter(
            or_(
                AttendanceSession.lesson == None,  # no lesson attached
                AttendanceSession.lesson_id == Lesson.id  # has lesson in enrolled course
            )
        )
        .filter(Course.creator_id == current_user.id)
        .order_by(AttendanceSession.start_time.desc())
        .all()
    )

    return sessions

# get available sessions for a student
def get_available_sessions(db: Session, current_user: User):
    if current_user.role.name.lower() != "student":
        raise HTTPException(status_code=403, detail="Only students can view this")

    now = datetime.now()
    enrolled_course_ids = [course.course_id for course in current_user.courses]

    if not enrolled_course_ids:
        return []

    sessions = (
        db.query(AttendanceSession)
        .outerjoin(AttendanceSession.lesson)  # allow lesson_id to be null
        .filter(AttendanceSession.start_time <= now)
        .filter(AttendanceSession.end_time >= now)
        .filter(
            or_(
                AttendanceSession.lesson == None,  # no lesson attached
                Lesson.course_id.in_(enrolled_course_ids)  # has lesson in enrolled course
            )
        )
        .all()
    )

    return sessions

# get all student's attendances list in a specific course
def get_attendance_by_course(course_id: int, db: Session):
    return (
        db.query(StudentAttendance)
        .join(AttendanceSession)
        .filter(AttendanceSession.course_id == course_id)
        .all()
    )

# automatic mark absent for all the expired sessions
def mark_absent_for_expired_sessions(db: Session):
    now = datetime.now()

    # Step 1: Find all sessions that already ended but not processed
    sessions = db.query(AttendanceSession).filter(AttendanceSession.end_time < now).all()

    for session in sessions:
        if not session.lesson:
            continue  # skip if session is not linked to a lesson

        course = session.lesson.course
        enrolled_students = course.users  # many-to-many relationship: Course.users

        for student in enrolled_students:
            # Step 2: Check if student already has a check-in
            existing = db.query(StudentAttendance).filter_by(
                attendance_session_id=session.id, user_id=student.user_id
            ).first()

            if not existing:
                # Step 3: Mark absent
                new_absence = StudentAttendance(
                    attendance_session_id=session.id,
                    user_id=student.id,
                    status="absent",
                    check_in_time=None,
                )
                db.add(new_absence)

    db.commit()
    return {"message": "Absent students marked for expired sessions."}

# bulk update the existing attendances for teacher
def bulk_update_attendance(data: AttendanceBulkUpdate, teacher: User, db: Session):
    # 1.  Validate session exists and teacher owns the course
    session = db.query(AttendanceSession).filter_by(id=data.session_id).first()
    if not session:
        raise HTTPException(404, "Attendance session not found")

    course: Course = session.course
    if course.creator_id != teacher.id and teacher.role.name.lower() != "admin":
        raise HTTPException(403, "Not authorized to edit this session")

    # 2.  Loop through each patch request
    for patch in data.updates:
        record = (
            db.query(StudentAttendance)
            .filter_by(session_id=data.session_id, user_id=patch.user_id)
            .first()
        )
        if record:
            record.status = "present" if patch.present else "absent"
            record.updated_at = datetime.now()
        else:
            # Create if missing
            new_rec = StudentAttendance(
                session_id=data.session_id,
                user_id=patch.user_id,
                status="present" if patch.present else "absent",
                check_in_time=None,
                updated_at=datetime.now()
            )
            db.add(new_rec)

    db.commit()
    return {"message": "Attendance records updated"}

def export_attendance_csv(
        session_id: int,
        db: Session,
        current_user: User
):
    session = db.query(AttendanceSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.course.creator_id != current_user.id and current_user.role.name.lower() != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    records = (
        db.query(StudentAttendance)
        .filter_by(attendance_session_id=session_id)
        .join(User)
        .all()
    )

    if not records:
        return JSONResponse(status_code=404, content={"detail": "No attendance records found."})

    # Prepare dataframe
    data = [{
        "Student ID": rec.user.id,
        "Name": rec.user.username,
        "Email": rec.user.email,
        "Status": rec.status,
        "Check-in Time": rec.check_in_time.isoformat() if rec.check_in_time else ""
    } for rec in records]

    df = pd.DataFrame(data)

    # Convert to CSV in-memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    filename = f"attendance_session_{session_id}.csv"
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
