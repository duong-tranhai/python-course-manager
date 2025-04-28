from alembic import op

revision = 'V10'
down_revision = 'V9'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
            INSERT INTO users (username, email, password, role_id)
            VALUES (
                'admin',
                'admin@example.com',
                '$2b$12$3qUOnxiZ5TntIKtnQ9EkhOjB3Fcj2NkTKLZqLUh7RI2uwrrI06Gta',
                3
            )
            ON CONFLICT (id) DO NOTHING;
        """)

def downgrade():
    op.execute("DELETE FROM users WHERE username = 'admin'")
