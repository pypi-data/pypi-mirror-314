# -*- coding: utf-8; -*-
"""add POSBatch

Revision ID: 6dd836b9829a
Revises: fa3aec1556bc
Create Date: 2023-09-23 09:10:07.049227

"""

# revision identifiers, used by Alembic.
revision = '6dd836b9829a'
down_revision = 'fa3aec1556bc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_pos
    op.create_table('batch_pos',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('created_by_uuid', sa.String(length=32), nullable=False),
                    sa.Column('cognized', sa.DateTime(), nullable=True),
                    sa.Column('cognized_by_uuid', sa.String(length=32), nullable=True),
                    sa.Column('rowcount', sa.Integer(), nullable=True),
                    sa.Column('complete', sa.Boolean(), nullable=False),
                    sa.Column('executed', sa.DateTime(), nullable=True),
                    sa.Column('executed_by_uuid', sa.String(length=32), nullable=True),
                    sa.Column('purge', sa.Date(), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('params', rattail.db.types.JSONTextDict(), nullable=True),
                    sa.Column('extra_data', sa.Text(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.Column('store_id', sa.String(length=10), nullable=True),
                    sa.Column('store_uuid', sa.String(length=32), nullable=True),
                    sa.Column('start_time', sa.DateTime(), nullable=True),
                    sa.Column('customer_uuid', sa.String(length=32), nullable=True),
                    sa.Column('sales_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('tax1_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('tax2_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('void', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['cognized_by_uuid'], ['user.uuid'], name='batch_pos_fk_cognized_by'),
                    sa.ForeignKeyConstraint(['created_by_uuid'], ['user.uuid'], name='batch_pos_fk_created_by'),
                    sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='batch_pos_fk_customer'),
                    sa.ForeignKeyConstraint(['executed_by_uuid'], ['user.uuid'], name='batch_pos_fk_executed_by'),
                    sa.ForeignKeyConstraint(['store_uuid'], ['store.uuid'], name='batch_pos_fk_store'),
                    sa.PrimaryKeyConstraint('uuid')
                    )

    # batch_pos_row
    op.create_table('batch_pos_row',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('batch_uuid', sa.String(length=32), nullable=False),
                    sa.Column('sequence', sa.Integer(), nullable=False),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('removed', sa.Boolean(), nullable=False),
                    sa.Column('row_type', sa.String(length=32), nullable=True),
                    sa.Column('item_entry', sa.String(length=32), nullable=True),
                    sa.Column('product_uuid', sa.String(length=32), nullable=True),
                    sa.Column('description', sa.String(length=60), nullable=True),
                    sa.Column('quantity', sa.Numeric(precision=8, scale=2), nullable=True),
                    sa.Column('reg_price', sa.Numeric(precision=8, scale=3), nullable=True),
                    sa.Column('txn_price', sa.Numeric(precision=8, scale=3), nullable=True),
                    sa.Column('sales_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('tax1_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('tax2_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.ForeignKeyConstraint(['batch_uuid'], ['batch_pos.uuid'], name='batch_pos_row_fk_batch_uuid'),
                    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], name='batch_pos_row_fk_item'),
                    sa.PrimaryKeyConstraint('uuid')
                    )


def downgrade():

    # batch_pos*
    op.drop_table('batch_pos_row')
    op.drop_table('batch_pos')
