import sqlalchemy as sa
from alembic import op

revision = 'V8'
down_revision = 'V7'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('lesson_quizzes', sa.Column('passing_score', sa.Integer(), nullable=False, server_default='70'))

def downgrade():
    op.drop_column('lesson_quizzes', 'passing_score')

