# -*- coding: utf-8; -*-
"""fix equity_payments

Revision ID: 310080aaa346
Revises: 093db8c16e7d
Create Date: 2023-08-08 18:08:53.588048

"""

# revision identifiers, used by Alembic.
revision = '310080aaa346'
down_revision = '093db8c16e7d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types
from sqlalchemy.dialects import postgresql


def upgrade():

    # member_equity_payment_version
    op.alter_column('member_equity_payment_version', 'member_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('member_equity_payment_version', 'amount',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=True)
    op.alter_column('member_equity_payment_version', 'received',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)


def downgrade():

    # member_equity_payment_version
    op.alter_column('member_equity_payment_version', 'received',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('member_equity_payment_version', 'amount',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=False)
    op.alter_column('member_equity_payment_version', 'member_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
