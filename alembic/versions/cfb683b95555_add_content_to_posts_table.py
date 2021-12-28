"""add content to posts table

Revision ID: cfb683b95555
Revises: 4b21b29de24c
Create Date: 2021-12-28 15:43:00.747951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb683b95555'
down_revision = '4b21b29de24c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
