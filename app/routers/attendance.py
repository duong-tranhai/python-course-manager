from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.auth import get_current_user
from app.crud import attendance as crud
from app.database import SessionLocal
from app.helpers.audit import log_action
from app.models.user import User
from app.schemas.attendance import (
    AttendanceSessionCreate, AttendanceSessionResponse,
    StudentAttendanceResponse, AttendanceBulkUpdate, AttendanceSessionWithCourseLesson
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/attendances", tags=["Attendance"])

@router.post("/sessions", response_model=AttendanceSessionResponse)
def create_session(
    data: AttendanceSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.create_attendance_session(data, db)

@router.get("/available", response_model=List[AttendanceSessionResponse])
def get_available_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_available_sessions(db, current_user)

@router.get("/by-teacher", response_model=List[AttendanceSessionWithCourseLesson])
def get_sessions_by_teacher(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name.lower() != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view this")

    return crud.get_sessions_by_teacher(db, current_user)

@router.get("/course/{course_id}", response_model=List[StudentAttendanceResponse])
def get_list_attendances(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.get_attendance_by_course(course_id, db)

@router.post("/check-in/{session_id}", response_model=StudentAttendanceResponse)
def check_in(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log_action(db, user_id=current_user.id, action="check_in", detail=f"Checked in to session ID {session_id}")

    return crud.mark_attendance(current_user.id, session_id, db)

@router.post("/mark-absent-expired")
def mark_absent_for_expired_sessions(db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user)):
    if current_user is not None:
        if current_user.role.name.lower() not in ("admin", "teacher"):
            raise HTTPException(status_code=403, detail="Not authorized")

    return crud.mark_absent_for_expired_sessions(db)

@router.patch("/records", status_code=200)
def update_attendance_records(
    payload: AttendanceBulkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name.lower() not in ("teacher", "admin"):
        raise HTTPException(403, "Only teachers or admins may update attendance")

    return crud.bulk_update_attendance(payload, current_user, db)

@router.get("/export", response_class=StreamingResponse)
def export_attendance_csv(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.export_attendance_csv(session_id, db, current_user)