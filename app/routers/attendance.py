from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import attendance as crud
from app.database import SessionLocal
from app.models.user import User
from app.schemas.attendance import (
    AttendanceSessionCreate, AttendanceSessionResponse,
    StudentAttendanceResponse
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

@router.post("/check-in/{session_id}", response_model=StudentAttendanceResponse)
def check_in(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.mark_attendance(current_user.id, session_id, db)

@router.get("/course/{course_id}", response_model=List[StudentAttendanceResponse])
def list_attendance(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.get_attendance_by_course(course_id, db)
