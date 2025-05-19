from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.course import Course
from ..models.lesson import Lesson
from ..models.user import User
from ..models.user_course import UserCourse
from ..models.user_lesson_progress import UserLessonProgress
from ..schemas import course as schema
from ..schemas.course import CourseWithProgress


def create_course(db: Session, course: schema.CourseCreate, creator_id: int):
    db_course = Course(**course.dict(), creator_id=creator_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course: schema.CourseUpdate):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        return None
    db_course.title = course.title
    db_course.description = course.description
    db.commit()
    db.refresh(db_course)
    return db_course

def mark_course_complete(course_id: int, current_user_id: int, db: Session):
    # Check if enrolled
    enrollment = db.query(UserCourse).filter_by(user_id=current_user_id, course_id=course_id).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="You are not enrolled in this course")

    # Get all lessons in the course
    lessons = db.query(Lesson).filter_by(course_id=course_id).all()
    if not lessons:
        raise HTTPException(status_code=400, detail="No lessons found in course")

    # Get completed lessons by student
    completed_ids = set(
        row.lesson_id for row in db.query(UserLessonProgress)
        .filter_by(user_id=current_user_id, is_completed=True)
        .filter(UserLessonProgress.lesson_id.in_([l.id for l in lessons]))
        .all()
    )

    if len(completed_ids) != len(lessons):
        raise HTTPException(status_code=400, detail="Please complete all lessons before finishing the course")

    # Update status
    enrollment.is_completed = True
    db.commit()
    return {"message": "Course marked as completed"}

def get_courses(db: Session):
    return db.query(Course).all()

def enroll_user(user_id: int, course_id: int, db: Session):
    # Check if already enrolled
    existing = db.query(UserCourse).filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return {"message": "Already enrolled"}

    enrollment = UserCourse(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Enrolled successfully"}

def get_courses_by_user(user_id: int, db: Session):
    # Corrected query: get actual users
    courses = db.query(Course).join(UserCourse).filter(UserCourse.user_id == user_id).all()
    response = []

    for course in courses:
        lessons = db.query(Lesson).filter_by(course_id=course.id).all()
        total = len(lessons)

        completed = db.query(UserLessonProgress).filter_by(user_id=user_id, is_completed=True) \
            .filter(UserLessonProgress.lesson_id.in_([l.id for l in lessons])).count()

        progress = int((completed / total) * 100) if total > 0 else 0

        response.append(CourseWithProgress(
            id=course.id,
            title=course.title,
            description=course.description,
            creator_id=course.creator_id,
            is_completed=any(uc.is_completed for uc in course.users if uc.user_id == user_id),
            progress=progress
        ))

    return response

def get_users_by_course(course_id: int, db: Session, current_user_id: int):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed to view students in this course")

    # Corrected query: get actual users
    users = db.query(User).join(UserCourse).filter(UserCourse.course_id == course.id).all()
    return users

def enroll_user_by_teacher(course_id: int, user_id: int, db: Session, current_user: User):
    course = db.query(Course).filter(Course.id == course_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not course or not user:
        raise HTTPException(status_code=404, detail="Course or user not found")
    if current_user.role_id != 1 or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the course creator can assign students")
    if user.role_id != 2:
        raise HTTPException(status_code=400, detail="This user is not a student-role User. Please enroll student only!")

    # Check if already enrolled
    existing = db.query(UserCourse).filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return {"message": "User already enrolled"}

    enrollment = UserCourse(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "User enrolled successfully"}

def delete_course(course_id: int, db: Session, creator_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.creator_id != creator_id:
        raise HTTPException(status_code=403, detail="You can only delete your own courses")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted!"}

def get_course_recommendations(
    user_id: int,
    db: Session
):
    # Subquery to find enrolled course IDs
    subquery = db.query(UserCourse.course_id).filter_by(user_id=user_id).subquery()

    # Recommend all courses not enrolled
    courses = db.query(Course).filter(Course.id.notin_(subquery)).limit(5).all()

    return courses
