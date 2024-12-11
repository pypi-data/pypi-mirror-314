# -*- coding: utf-8; -*-
"""grow product.true_margin

Revision ID: 492f7f75e07f
Revises: 17cd825534de
Create Date: 2023-11-15 09:28:05.215294

"""

# revision identifiers, used by Alembic.
revision = '492f7f75e07f'
down_revision = '17cd825534de'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # product_volatile
    op.alter_column('product_volatile', 'true_margin',
               existing_type=sa.NUMERIC(precision=9, scale=5),
               type_=sa.Numeric(precision=12, scale=5),
               existing_nullable=True)


def downgrade():

    # product_volatile
    op.alter_column('product_volatile', 'true_margin',
               existing_type=sa.Numeric(precision=12, scale=5),
               type_=sa.NUMERIC(precision=9, scale=5),
               existing_nullable=True)
