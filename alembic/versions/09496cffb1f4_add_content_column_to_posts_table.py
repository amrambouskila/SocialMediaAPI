"""Add content column to posts table

Revision ID: 09496cffb1f4
Revises: 2c0b3b30df8d
Create Date: 2022-08-06 16:52:12.855920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09496cffb1f4'
down_revision = '2c0b3b30df8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
