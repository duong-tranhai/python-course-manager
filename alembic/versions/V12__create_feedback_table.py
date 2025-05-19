from alembic import op
import sqlalchemy as sa

revision = 'V12'
down_revision = 'V11'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'feedbacks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id'), nullable=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_table('feedbacks')
