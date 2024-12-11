# -*- coding: utf-8; -*-
"""add MemberEquityPayment

Revision ID: e00841e2deb2
Revises: a4ac7985cfa6
Create Date: 2023-06-18 11:59:41.256360

"""

# revision identifiers, used by Alembic.
revision = 'e00841e2deb2'
down_revision = 'a4ac7985cfa6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # member_equity_payment
    op.create_table('member_equity_payment',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('member_uuid', sa.String(length=32), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=7, scale=2), nullable=False),
                    sa.Column('received', sa.DateTime(), nullable=False),
                    sa.Column('description', sa.String(length=100), nullable=True),
                    sa.Column('transaction_identifier', sa.String(length=100), nullable=True),
                    sa.ForeignKeyConstraint(['member_uuid'], ['member.uuid'], name='member_equity_payment_fk_member'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('member_equity_payment_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('member_uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('amount', sa.Numeric(precision=7, scale=2), autoincrement=False, nullable=False),
                    sa.Column('received', sa.DateTime(), autoincrement=False, nullable=False),
                    sa.Column('description', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('transaction_identifier', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_member_equity_payment_version_end_transaction_id'), 'member_equity_payment_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_member_equity_payment_version_operation_type'), 'member_equity_payment_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_member_equity_payment_version_transaction_id'), 'member_equity_payment_version', ['transaction_id'], unique=False)


def downgrade():

    # member_equity_payment
    op.drop_index(op.f('ix_member_equity_payment_version_transaction_id'), table_name='member_equity_payment_version')
    op.drop_index(op.f('ix_member_equity_payment_version_operation_type'), table_name='member_equity_payment_version')
    op.drop_index(op.f('ix_member_equity_payment_version_end_transaction_id'), table_name='member_equity_payment_version')
    op.drop_table('member_equity_payment_version')
    op.drop_table('member_equity_payment')
