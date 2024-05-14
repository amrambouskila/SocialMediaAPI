"""add rest of the columns to posts table

Revision ID: 10922c6be19f
Revises: eb302a90f725
Create Date: 2022-08-06 17:12:28.008956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10922c6be19f'
down_revision = 'eb302a90f725'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='1', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    pass


def downgrade() -> None:
    op.drop_columns('posts', 'published')
    op.drop_columns('posts', 'created_at')
    pass
