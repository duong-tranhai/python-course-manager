from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import lesson as lesson_crud
from app.crud import quiz as quiz_crud
from app.database import SessionLocal
from app.models.user import User
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse

router = APIRouter(prefix="/lessons", tags=["lessons"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/course/{course_id}", response_model=LessonResponse)
def create_lesson(course_id: int, lesson: LessonCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return lesson_crud.create_lesson(course_id, lesson, db, current_user.id)

@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_lessons(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return lesson_crud.get_lessons(course_id, db, current_user)

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, update: LessonUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return lesson_crud.update_lesson(lesson_id, update, db, current_user.id)

@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return lesson_crud.delete_lesson(lesson_id, db, current_user.id)

@router.get("/course/{course_id}/with-progress")
def get_lessons_with_progress(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return lesson_crud.get_lessons_with_progress(course_id, db, current_user)

@router.get("/{lesson_id}/completed")
def is_lesson_completed(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    completed = quiz_crud.get_lesson_completion_status(current_user.id, lesson_id, db)
    return {"lesson_id": lesson_id, "is_completed": completed}