"""Insert default roles into roles table"""

from alembic import op

# revision identifiers, used by Alembic.
revision = 'V2'
down_revision = 'V1'  # use your previous revision ID here
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        INSERT INTO roles (id, name) VALUES
        (1, 'teacher'),
        (2, 'student'),
        (3, 'admin')
        ON CONFLICT (id) DO NOTHING;
    """)

def downgrade():
    op.execute("""
        DELETE FROM roles WHERE id IN (1, 2, 3);
    """)
