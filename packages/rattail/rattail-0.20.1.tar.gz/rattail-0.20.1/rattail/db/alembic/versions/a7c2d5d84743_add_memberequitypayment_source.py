# -*- coding: utf-8; -*-
"""add MemberEquityPayment.source

Revision ID: a7c2d5d84743
Revises: 310080aaa346
Create Date: 2023-09-07 17:33:19.223569

"""

# revision identifiers, used by Alembic.
revision = 'a7c2d5d84743'
down_revision = '310080aaa346'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # member_equity_payment
    op.add_column('member_equity_payment', sa.Column('source', sa.String(length=50), nullable=True))
    op.add_column('member_equity_payment_version', sa.Column('source', sa.String(length=50), autoincrement=False, nullable=True))


def downgrade():

    # member_equity_payment
    op.drop_column('member_equity_payment_version', 'source')
    op.drop_column('member_equity_payment', 'source')
