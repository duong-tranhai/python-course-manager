from alembic import op
import sqlalchemy as sa

revision = 'V6'
down_revision = 'V5'  # Replace with your actual previous revision ID
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'lesson_quizzes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id')),
        sa.Column('title', sa.String(), nullable=False)
    )

    op.create_table(
        'quiz_questions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('lesson_quizzes.id')),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('choices', sa.JSON(), nullable=True),  # Expected to be a list of strings
        sa.Column('correct_answer', sa.String(), nullable=False)
    )

    op.create_table(
        'student_quiz_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('lesson_quizzes.id')),
        sa.Column('selected_answers', sa.JSON(), nullable=True),  # Dict[question_id] = answer
        sa.Column('score', sa.Integer(), nullable=True)
    )

def downgrade():
    op.drop_table('student_quiz_results')
    op.drop_table('quiz_questions')
    op.drop_table('lesson_quizzes')
