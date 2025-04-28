"""Create new table Lesson"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'V4'
down_revision = 'V3'  # use your previous revision ID here
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id'), nullable=False)
    )


def downgrade():
    op.drop_table('lessons')

