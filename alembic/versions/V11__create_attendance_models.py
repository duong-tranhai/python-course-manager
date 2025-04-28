from alembic import op
import sqlalchemy as sa

revision = 'V11'
down_revision = 'V10'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'attendance_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id')),
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lessons.id'), nullable=True),
        sa.Column('start_time', sa.DateTime),
        sa.Column('end_time', sa.DateTime),
        sa.Column('type', sa.String),
    )

    op.create_table(
        'student_attendance',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('attendance_session_id', sa.Integer, sa.ForeignKey('attendance_sessions.id')),
        sa.Column('status', sa.String),
        sa.Column('timestamp', sa.DateTime),
    )

def downgrade():
    op.drop_table('student_attendance')
    op.drop_table('attendance_sessions')
