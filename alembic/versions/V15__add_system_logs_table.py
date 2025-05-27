import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'V15'
down_revision = 'V14'  # use your previous revision ID here
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'system_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('detail', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )


def downgrade():
    op.drop_table('system_logs')
