# -*- coding: utf-8; -*-
"""add equity_payment.status_code

Revision ID: 17cd825534de
Revises: 41a05b420280
Create Date: 2023-11-05 16:33:27.646431

"""

# revision identifiers, used by Alembic.
revision = '17cd825534de'
down_revision = '41a05b420280'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # member_equity_payment
    op.add_column('member_equity_payment', sa.Column('status_code', sa.Integer(), nullable=True))
    op.add_column('member_equity_payment_version', sa.Column('status_code', sa.Integer(), autoincrement=False, nullable=True))


def downgrade():

    # member_equity_payment
    op.drop_column('member_equity_payment_version', 'status_code')
    op.drop_column('member_equity_payment', 'status_code')
