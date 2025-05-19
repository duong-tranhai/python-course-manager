from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..crud import user as crud, feedback as feedback_crud, course as course_crud
from ..database import SessionLocal
from ..models.user import User
from ..schemas import user as schema, feedback as feedback_schema

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=list[schema.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/{user_id}", response_model=schema.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}/dashboard-summary")
def get_student_dashboard_summary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.get_student_dashboard_summary(user_id, db)

@router.post("/{user_id}/feedback", response_model=feedback_schema.FeedbackResponse)
def create_feedback(
    user_id: int,
    feedback: feedback_schema.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return feedback_crud.create_feedback(user_id, feedback, db)

@router.get("/{user_id}/recommendations")
def get_course_recommendation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return course_crud.get_course_recommendations(user_id, db)