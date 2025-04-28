"""Initial schema for Course Manager"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'V1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('role_id', sa.Integer, nullable=False)
    )

    op.create_table(
        'courses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('creator_id', sa.Integer, sa.ForeignKey('users.id'))
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )

    op.create_table(
        'user_course',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id'))
    )

def downgrade():
    op.drop_table('user_courses')
    op.drop_table('courses')
    op.drop_table('users')
    op.drop_table('roles')
