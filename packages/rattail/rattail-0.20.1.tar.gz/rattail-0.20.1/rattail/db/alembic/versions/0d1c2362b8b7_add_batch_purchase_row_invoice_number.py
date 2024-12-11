# -*- coding: utf-8; -*-
"""add batch_purchase_row.invoice_number

Revision ID: 0d1c2362b8b7
Revises: e00841e2deb2
Create Date: 2023-07-07 17:09:03.723130

"""

# revision identifiers, used by Alembic.
revision = '0d1c2362b8b7'
down_revision = 'e00841e2deb2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types
from sqlalchemy.dialects import postgresql


def upgrade():

    # batch_purchase_row
    op.add_column('batch_purchase_row', sa.Column('invoice_number', sa.String(length=20), nullable=True))

    # purchase_item
    op.add_column('purchase_item', sa.Column('invoice_number', sa.String(length=20), nullable=True))


def downgrade():

    # purchase_item
    op.drop_column('purchase_item', 'invoice_number')

    # batch_purchase_row
    op.drop_column('batch_purchase_row', 'invoice_number')
