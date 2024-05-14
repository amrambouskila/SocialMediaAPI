"""add foreign key to posts table

Revision ID: eb302a90f725
Revises: c48820d843f1
Create Date: 2022-08-06 17:03:15.376716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb302a90f725'
down_revision = 'c48820d843f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
