from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..crud import course as course_crud
from ..database import SessionLocal
from ..models.user import User
from ..schemas import course as course_schema
from ..schemas import user as user_schema

router = APIRouter(prefix="/courses", tags=["Courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new course
@router.post("/", response_model=course_schema.CourseResponse)
def create_course(course: course_schema.CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Only teachers can create courses")

    return course_crud.create_course(db=db, course=course, creator_id=current_user.id)

# Update an existing course
@router.put("/{course_id}", response_model=course_schema.CourseResponse)
def update_course(course_id: int, course: course_schema.CourseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1 or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this course")

    return course_crud.update_course(db, course_id, course)

# Teacher enroll a user to specific course
@router.post("/{course_id}/enroll-user/{user_id}")
def enroll_user_by_teacher(course_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return course_crud.enroll_user_by_teacher(course_id, user_id, db, current_user)

# Mark course as completed
@router.patch("/{course_id}/complete")
def mark_course_complete(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return course_crud.mark_course_complete(course_id, current_user.id, db)

# Get all courses
@router.get("/", response_model=List[course_schema.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return course_crud.get_courses(db=db)

# Enroll user in course by themselves
@router.post("/{course_id}/enroll")
def enroll_user(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Not logged in!")
    return course_crud.enroll_user(user_id=current_user.id, course_id=course_id, db=db)

# get all enrolled courses of a student
@router.get("/by-user/{user_id}", response_model=List[course_schema.CourseWithProgress])
def get_courses_by_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return course_crud.get_courses_by_user(user_id, db)

# get enrolled students in a Course
@router.get("/by-course/{course_id}/users", response_model=List[user_schema.UserResponse])
def get_users_by_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return course_crud.get_users_by_course(course_id, db, current_user.id)

# delete course by id
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Only teachers can delete courses")

    return course_crud.delete_course(course_id, db, current_user.id)

