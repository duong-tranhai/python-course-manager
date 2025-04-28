from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.models.user_course import UserCourse
from app.models.user_lesson_progress import UserLessonProgress
from app.schemas.lesson import LessonCreate, LessonUpdate


def create_lesson(course_id: int, lesson: LessonCreate, db: Session, current_user_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this course")

    new_lesson = Lesson(title=lesson.title, content=lesson.content, course_id=course_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

def get_lessons(course_id: int, db: Session, current_user: User):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.creator_id != current_user.id and current_user.role_id == 1:
        raise HTTPException(status_code=403, detail="You are not allowed to view lessons for this course")

    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    return lessons

def update_lesson(lesson_id: int, update: LessonUpdate, db: Session, current_user_id: int):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=403, detail="You cannot edit this lesson")

    lesson.title = update.title
    lesson.content = update.content
    db.commit()
    db.refresh(lesson)
    return lesson

def delete_lesson(lesson_id: int, db: Session, current_user_id: int):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=403, detail="You cannot delete this lesson")

    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}

def get_lessons_with_progress(course_id: int, db: Session, current_user: User):
    # Ensure student is enrolled
    enrolled = db.query(UserCourse).filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrolled:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")

    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    progress_map = {
        row.lesson_id: row.is_completed
        for row in db.query(UserLessonProgress).filter_by(user_id=current_user.id).all()
    }

    return [
        {
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "is_completed": progress_map.get(lesson.id, False)
        }
        for lesson in lessons
    ]
