# -*- coding: utf-8; -*-
"""add batch_pos.fs_total

Revision ID: 41a05b420280
Revises: e112f75359b3
Create Date: 2023-10-19 16:40:11.395986

"""

# revision identifiers, used by Alembic.
revision = '41a05b420280'
down_revision = 'e112f75359b3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # tender
    op.add_column('tender', sa.Column('is_foodstamp', sa.Boolean(), nullable=True))
    op.add_column('tender_version', sa.Column('is_foodstamp', sa.Boolean(), autoincrement=False, nullable=True))

    # batch_pos
    op.add_column('batch_pos', sa.Column('fs_total', sa.Numeric(precision=9, scale=2), nullable=True))
    op.add_column('batch_pos', sa.Column('fs_tender_total', sa.Numeric(precision=9, scale=2), nullable=True))


def downgrade():

    # batch_pos
    op.drop_column('batch_pos', 'fs_tender_total')
    op.drop_column('batch_pos', 'fs_total')

    # tender
    op.drop_column('tender_version', 'is_foodstamp')
    op.drop_column('tender', 'is_foodstamp')
