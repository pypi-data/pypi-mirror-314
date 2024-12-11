# -*- coding: utf-8; -*-
"""add User.prevent_password_change

Revision ID: 524373deb98e
Revises: e206b9457091
Create Date: 2023-05-02 18:49:58.063276

"""

# revision identifiers, used by Alembic.
revision = '524373deb98e'
down_revision = 'e206b9457091'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # user
    op.add_column('user', sa.Column('prevent_password_change', sa.Boolean(), nullable=True))
    op.add_column('user_version', sa.Column('prevent_password_change', sa.Boolean(), autoincrement=False, nullable=True))


def downgrade():

    # user
    op.drop_column('user_version', 'prevent_password_change')
    op.drop_column('user', 'prevent_password_change')
