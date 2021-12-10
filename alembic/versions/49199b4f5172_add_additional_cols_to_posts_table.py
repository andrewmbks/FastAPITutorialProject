"""add additional cols to posts table

Revision ID: 49199b4f5172
Revises: 4cc7c8056222
Create Date: 2021-12-09 16:35:33.354488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49199b4f5172'
down_revision = '4cc7c8056222'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
