import sqlalchemy as sa
from alembic import op

revision = 'V9'
down_revision = 'V8'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('student_quiz_results', sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))

def downgrade():
    op.drop_column('student_quiz_results', 'submitted_at')

