"""Add is_completed column to user_course table"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'V3'
down_revision = 'V2'  # use your previous revision ID here
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user_course', sa.Column('is_completed', sa.Boolean(), server_default='false'))

def downgrade():
    op.drop_column('user_course', 'is_completed')

