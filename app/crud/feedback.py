from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.schemas import feedback as feedback_schema


def create_feedback(
    user_id: int,
    feedback: feedback_schema.FeedbackCreate,
    db: Session
):
    entry = Feedback(
        user_id=user_id,
        course_id=feedback.course_id,
        lesson_id=feedback.lesson_id,
        content=feedback.content,
        rating=feedback.rating,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
