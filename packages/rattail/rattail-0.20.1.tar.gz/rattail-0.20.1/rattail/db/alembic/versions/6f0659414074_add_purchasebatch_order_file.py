# -*- coding: utf-8; -*-
"""add PurchaseBatch.order_file

Revision ID: 6f0659414074
Revises: b9d58e803208
Create Date: 2024-10-21 14:53:02.779348

"""

# revision identifiers, used by Alembic.
revision = '6f0659414074'
down_revision = 'b9d58e803208'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_purchase
    op.add_column('batch_purchase', sa.Column('order_file', sa.String(length=255), nullable=True))
    op.add_column('batch_purchase', sa.Column('order_parser_key', sa.String(length=100), nullable=True))


def downgrade():

    # batch_purchase
    op.drop_column('batch_purchase', 'order_parser_key')
    op.drop_column('batch_purchase', 'order_file')
