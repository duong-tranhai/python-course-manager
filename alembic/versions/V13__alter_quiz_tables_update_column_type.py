"""Update score to Float in student_quiz_results

Revision ID: update_score_to_float
Revises: <put-previous-revision-id-here>
Create Date: 2025-04-28

"""
import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic.
revision = 'V13'
down_revision = 'V12'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'student_quiz_results',
        'score',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=True
    )

    op.alter_column(
        'lesson_quizzes',
        'passing_score',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'student_quiz_results',
        'score',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=True
    )

    op.alter_column(
        'lesson_quizzes',
        'passing_score',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False
    )