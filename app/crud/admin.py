from fastapi import HTTPException
from sqlalchemy import Integer, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.role import Role
from app.models.system_log import SystemLog
from app.models.user import User
from app.models.user_course import UserCourse
from app.models.user_lesson_progress import UserLessonProgress
from app.schemas import course as schema
from app.schemas.role import RoleBase


def get_admin_dashboard_data(db: Session):
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_lessons = db.query(Lesson).count()

    active_students = (
        db.query(UserLessonProgress.user_id)
        .distinct()
        .count()
    )

    completion_avg = db.query(func.avg(UserLessonProgress.is_completed.cast(Integer))).scalar() or 0

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_lessons": total_lessons,
        "active_students": active_students,
        "average_completion_rate": round(completion_avg * 100, 2)
    }

def get_all_users(db: Session, search: str = None, role_id: int = None):
    query = db.query(User).join(Role).options()

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(like_pattern),
                User.email.ilike(like_pattern)
            )
        )

    if role_id:
        query = query.filter(User.role_id == role_id)

    return query.all()

def get_all_courses_with_stats(db: Session):
    courses = db.query(Course).options(joinedload(Course.creator)).all()

    course_data = []

    for course in courses:
        total_students = (
            db.query(UserCourse)
            .filter(UserCourse.course_id == course.id)
            .count()
        )

        total_lessons = (
            db.query(Lesson)
            .filter(Lesson.course_id == course.id)
            .count()
        )

        total_completed = (
            db.query(UserLessonProgress)
            .join(Lesson, Lesson.id == UserLessonProgress.lesson_id)
            .filter(
                Lesson.course_id == course.id,
                UserLessonProgress.is_completed == True
            ).count()
        )

        total_progress = (
            db.query(UserLessonProgress)
            .join(Lesson, Lesson.id == UserLessonProgress.lesson_id)
            .filter(Lesson.course_id == course.id).count()
        )

        avg_completion = (
            (total_completed / total_progress) * 100 if total_progress else 0
        )

        course_data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "creator": {
                "id": course.creator.id,
                "username": course.creator.username
            },
            "total_students": total_students,
            "lesson_count": total_lessons,
            "avg_completion_rate": round(avg_completion, 2)
        })

    return course_data

def get_course_details(course_id: int, db: Session):
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .options(
            joinedload(Course.creator),
            joinedload(Course.lessons),
            joinedload(Course.users) # enrolled students list
        )
        .first()
    )

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course

def update_course(course_id: int, update_data: schema.CourseUpdate, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.title = update_data.title
    course.description = update_data.description
    db.commit()
    db.refresh(course)
    return course

def delete_course(course_id: int, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

def get_all_roles(db: Session):
    return db.query(Role).all()

def create_role(role_data: RoleBase, db: Session):
    if db.query(Role).filter_by(name=role_data.name).first():
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(**role_data.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(role_id: int, update_data: RoleBase, db: Session):
    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.name = update_data.name
    db.commit()
    return role

def delete_role(role_id: int, db: Session):
    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted"}

def assign_role_to_user(user_id: int, role_id: int, db: Session):
    user = db.query(User).get(user_id)
    role = db.query(Role).get(role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    user.role_id = role.id
    db.commit()
    return {"message": f"Role '{role.name}' assigned to user '{user.username}'"}

def get_system_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SystemLog).order_by(SystemLog.timestamp.desc()).offset(skip).limit(limit).all()