# -*- coding: utf-8; -*-
"""add PendingProduct.product

Revision ID: 86b00e66b83e
Revises: a7c2d5d84743
Create Date: 2023-09-09 21:37:39.905677

"""

# revision identifiers, used by Alembic.
revision = '86b00e66b83e'
down_revision = 'a7c2d5d84743'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # pending_product
    op.add_column('pending_product', sa.Column('product_uuid', sa.String(length=32), nullable=True))
    op.add_column('pending_product', sa.Column('resolved', sa.DateTime(), nullable=True))
    op.add_column('pending_product', sa.Column('resolved_by_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('pending_product_fk_product', 'pending_product', 'product', ['product_uuid'], ['uuid'])
    op.create_foreign_key('pending_product_fk_resolved_by', 'pending_product', 'user', ['resolved_by_uuid'], ['uuid'])


def downgrade():

    # pending_product
    op.drop_constraint('pending_product_fk_resolved_by', 'pending_product', type_='foreignkey')
    op.drop_constraint('pending_product_fk_product', 'pending_product', type_='foreignkey')
    op.drop_column('pending_product', 'resolved_by_uuid')
    op.drop_column('pending_product', 'resolved')
    op.drop_column('pending_product', 'product_uuid')
