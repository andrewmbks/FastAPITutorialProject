"""Add content column to post table

Revision ID: 3036e521aaee
Revises: b4f09c7cb640
Create Date: 2021-12-09 16:11:03.550640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3036e521aaee'
down_revision = 'b4f09c7cb640'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
