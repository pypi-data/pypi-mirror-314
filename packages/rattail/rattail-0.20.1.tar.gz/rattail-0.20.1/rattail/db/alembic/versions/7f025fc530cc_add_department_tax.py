# -*- coding: utf-8; -*-
"""add department.tax

Revision ID: 7f025fc530cc
Revises: d69dd44f495c
Create Date: 2023-10-11 18:13:57.297032

"""

# revision identifiers, used by Alembic.
revision = '7f025fc530cc'
down_revision = 'd69dd44f495c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # department
    op.add_column('department', sa.Column('tax_uuid', sa.String(length=32), nullable=True))
    op.add_column('department', sa.Column('food_stampable', sa.Boolean(), nullable=True))
    op.create_foreign_key('department_fk_tax', 'department', 'tax', ['tax_uuid'], ['uuid'])
    op.add_column('department_version', sa.Column('tax_uuid', sa.String(length=32), autoincrement=False, nullable=True))
    op.add_column('department_version', sa.Column('food_stampable', sa.Boolean(), autoincrement=False, nullable=True))


def downgrade():

    # department
    op.drop_column('department_version', 'food_stampable')
    op.drop_column('department_version', 'tax_uuid')
    op.drop_constraint('department_fk_tax', 'department', type_='foreignkey')
    op.drop_column('department', 'food_stampable')
    op.drop_column('department', 'tax_uuid')
