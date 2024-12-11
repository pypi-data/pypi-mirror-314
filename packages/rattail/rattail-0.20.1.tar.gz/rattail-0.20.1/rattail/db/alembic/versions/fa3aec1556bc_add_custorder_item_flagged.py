# -*- coding: utf-8; -*-
"""add custorder_item.flagged

Revision ID: fa3aec1556bc
Revises: 86b00e66b83e
Create Date: 2023-09-10 14:33:56.552430

"""

# revision identifiers, used by Alembic.
revision = 'fa3aec1556bc'
down_revision = '86b00e66b83e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # custorder_item
    op.add_column('custorder_item', sa.Column('special_order', sa.Boolean(), nullable=True))
    op.add_column('custorder_item', sa.Column('flagged', sa.Boolean(), nullable=True))
    op.add_column('custorder_item', sa.Column('contact_attempts', sa.Integer(), nullable=True))
    op.add_column('custorder_item', sa.Column('last_contacted', sa.DateTime(), nullable=True))

    # batch_custorder_row
    op.add_column('batch_custorder_row', sa.Column('special_order', sa.Boolean(), nullable=True))


def downgrade():

    # batch_custorder_row
    op.drop_column('batch_custorder_row', 'special_order')

    # custorder_item
    op.drop_column('custorder_item', 'last_contacted')
    op.drop_column('custorder_item', 'contact_attempts')
    op.drop_column('custorder_item', 'flagged')
    op.drop_column('custorder_item', 'special_order')
