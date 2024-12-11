# -*- coding: utf-8; -*-
"""add batch_pos_row.cur_price

Revision ID: e112f75359b3
Revises: 7f025fc530cc
Create Date: 2023-10-18 18:42:24.745734

"""

# revision identifiers, used by Alembic.
revision = 'e112f75359b3'
down_revision = '7f025fc530cc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_pos_row
    op.add_column('batch_pos_row', sa.Column('cur_price', sa.Numeric(precision=8, scale=3), nullable=True))
    op.add_column('batch_pos_row', sa.Column('cur_price_type', sa.Integer(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('cur_price_start', sa.DateTime(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('cur_price_end', sa.DateTime(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('txn_price_adjusted', sa.Boolean(), nullable=True))


def downgrade():

    # batch_pos_row
    op.drop_column('batch_pos_row', 'txn_price_adjusted')
    op.drop_column('batch_pos_row', 'cur_price_end')
    op.drop_column('batch_pos_row', 'cur_price_start')
    op.drop_column('batch_pos_row', 'cur_price_type')
    op.drop_column('batch_pos_row', 'cur_price')
