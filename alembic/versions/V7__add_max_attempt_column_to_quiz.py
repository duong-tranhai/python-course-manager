import sqlalchemy as sa
from alembic import op

revision = 'V7'
down_revision = 'V6'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('lesson_quizzes', sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='1'))

def downgrade():
    op.drop_column('lesson_quizzes', 'max_attempts')
