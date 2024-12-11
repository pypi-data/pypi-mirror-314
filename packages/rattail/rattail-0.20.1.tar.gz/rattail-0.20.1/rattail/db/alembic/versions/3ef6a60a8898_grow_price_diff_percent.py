# -*- coding: utf-8; -*-
"""grow price_diff_percent

Revision ID: 3ef6a60a8898
Revises: f30d2225fa49
Create Date: 2023-09-28 11:21:40.684985

"""

# revision identifiers, used by Alembic.
revision = '3ef6a60a8898'
down_revision = 'f30d2225fa49'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_pricing_row
    op.alter_column('batch_pricing_row', 'price_diff_percent',
                    type_=sa.Numeric(precision=10, scale=3))


def downgrade():

    # batch_pricing_row
    op.alter_column('batch_pricing_row', 'price_diff_percent',
                    type_=sa.Numeric(precision=8, scale=3))
