from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship

from app.models import Base


class LessonQuiz(Base):
    __tablename__ = "lesson_quizzes"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    title = Column(String, nullable=False)
    max_attempts = Column(Integer, nullable=False, default=1)
    passing_score = Column(Integer, nullable=False, default=70)  # in percent

    questions = relationship("QuizQuestion", back_populates="quiz")
    lesson = relationship("Lesson", back_populates="quiz")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("lesson_quizzes.id"))
    question = Column(String, nullable=False)
    choices = Column(JSON)  # Expecting list of strings
    correct_answer = Column(String, nullable=False)

    quiz = relationship("LessonQuiz", back_populates="questions")


class StudentQuizResult(Base):
    __tablename__ = "student_quiz_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("lesson_quizzes.id"))
    selected_answers = Column(JSON)  # Dict[question_id] = selected_choice
    score = Column(Integer)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
