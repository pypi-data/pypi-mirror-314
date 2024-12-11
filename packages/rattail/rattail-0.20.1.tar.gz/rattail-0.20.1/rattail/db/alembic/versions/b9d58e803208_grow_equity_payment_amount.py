# -*- coding: utf-8; -*-
"""grow equity payment amount

Revision ID: b9d58e803208
Revises: f6e95c74d8db
Create Date: 2024-08-13 10:59:47.778670

"""

# revision identifiers, used by Alembic.
revision = 'b9d58e803208'
down_revision = 'f6e95c74d8db'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # member_equity_payment
    op.alter_column('member_equity_payment', 'amount',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=False)
    op.alter_column('member_equity_payment_version', 'amount',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=True)


def downgrade():

    # member_equity_payment
    op.alter_column('member_equity_payment_version', 'amount',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.NUMERIC(precision=7, scale=2),
               existing_nullable=True)
    op.alter_column('member_equity_payment', 'amount',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.NUMERIC(precision=7, scale=2),
               existing_nullable=False)
