from alembic import op
import sqlalchemy as sa

revision = 'V5'
down_revision = 'V4'  # Replace this with the actual previous revision ID
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user_lesson_progress',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), primary_key=True),
        sa.Column('is_completed', sa.Boolean(), server_default='false')
    )

def downgrade():
    op.drop_table('user_lesson_progress')
