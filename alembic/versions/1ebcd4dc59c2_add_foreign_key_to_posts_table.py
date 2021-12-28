"""add foreign-key to posts table

Revision ID: 1ebcd4dc59c2
Revises: 6e2a1f4983bf
Create Date: 2021-12-28 15:57:56.069175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ebcd4dc59c2'
down_revision = '6e2a1f4983bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',
                          local_cols=[
                              'owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
