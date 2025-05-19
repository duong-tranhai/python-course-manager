from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models import user as model
from ..models.student_attendance import StudentAttendance
from ..models.user_course import UserCourse
from ..models.user_lesson_progress import UserLessonProgress
from ..schemas import user as schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schema.UserCreate):
    # db_user = model.User(**user.dict())
    hashed_password = get_password_hash(user.password)
    db_user = model.User(username=user.username, password=hashed_password, email=user.email, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(model.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_student_dashboard_summary(
    user_id: int,
    db: Session
):
    total_courses = db.query(UserCourse).filter_by(user_id=user_id).count()
    completed_courses = db.query(UserCourse).filter_by(user_id=user_id, is_completed=True).count()

    total_lessons = db.query(UserLessonProgress).filter_by(user_id=user_id).count()
    completed_lessons = db.query(UserLessonProgress).filter_by(user_id=user_id, is_completed=True).count()

    total_attendance = db.query(StudentAttendance).filter_by(user_id=user_id).count()
    present_attendance = db.query(StudentAttendance).filter_by(user_id=user_id, status="present").count()

    attendance_rate = (
        round((present_attendance / total_attendance) * 100, 2) if total_attendance else 0.0
    )

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "attendance_rate": attendance_rate,
        "badges": [],  # future integration
    }
