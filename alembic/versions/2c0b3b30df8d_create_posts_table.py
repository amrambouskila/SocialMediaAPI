"""create posts table

Revision ID: 2c0b3b30df8d
Revises: 
Create Date: 2022-08-06 16:43:18.868843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c0b3b30df8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
