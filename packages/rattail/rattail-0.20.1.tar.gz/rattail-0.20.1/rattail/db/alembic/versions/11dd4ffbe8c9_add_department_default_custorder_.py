# -*- coding: utf-8; -*-
"""add Department.default_custorder_discount

Revision ID: 11dd4ffbe8c9
Revises: 492f7f75e07f
Create Date: 2023-12-22 11:38:15.504641

"""

# revision identifiers, used by Alembic.
revision = '11dd4ffbe8c9'
down_revision = '492f7f75e07f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # department
    op.add_column('department', sa.Column('default_custorder_discount', sa.Numeric(precision=5, scale=3), nullable=True))
    op.add_column('department_version', sa.Column('default_custorder_discount', sa.Numeric(precision=5, scale=3), autoincrement=False, nullable=True))


def downgrade():

    # department
    op.drop_column('department_version', 'default_custorder_discount')
    op.drop_column('department', 'default_custorder_discount')
