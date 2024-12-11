# -*- coding: utf-8; -*-
"""add invoice_date for receiving row

Revision ID: 093db8c16e7d
Revises: 0d1c2362b8b7
Create Date: 2023-08-07 13:40:04.545706

"""

# revision identifiers, used by Alembic.
revision = '093db8c16e7d'
down_revision = '0d1c2362b8b7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types
from sqlalchemy.dialects import postgresql


def upgrade():

    # purchase_item
    op.add_column('purchase_item', sa.Column('invoice_date', sa.Date(), nullable=True))

    # batch_purchase_row
    op.add_column('batch_purchase_row', sa.Column('invoice_date', sa.Date(), nullable=True))


def downgrade():

    # batch_purchase_row
    op.drop_column('batch_purchase_row', 'invoice_date')

    # purchase_item
    op.drop_column('purchase_item', 'invoice_date')
