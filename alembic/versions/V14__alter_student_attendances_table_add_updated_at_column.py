import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic.
revision = 'V14'
down_revision = 'V13'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('student_attendances', sa.Column('updated_at', sa.DateTime, nullable=True, default=None))

def downgrade():
    op.drop_column('student_attendances', 'updated_at')