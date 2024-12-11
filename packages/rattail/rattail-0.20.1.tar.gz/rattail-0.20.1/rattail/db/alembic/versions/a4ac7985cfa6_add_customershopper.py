# -*- coding: utf-8; -*-
"""add CustomerShopper

Revision ID: a4ac7985cfa6
Revises: 2ff00a7cb734
Create Date: 2023-06-06 20:55:28.816311

"""

# revision identifiers, used by Alembic.
revision = 'a4ac7985cfa6'
down_revision = '2ff00a7cb734'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # customer
    op.add_column('customer', sa.Column('account_holder_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('customer_fk_account_holder', 'customer', 'person', ['account_holder_uuid'], ['uuid'])
    op.add_column('customer_version', sa.Column('account_holder_uuid', sa.String(length=32), autoincrement=False, nullable=True))

    # customer_shopper
    op.create_table('customer_shopper',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('customer_uuid', sa.String(length=32), nullable=False),
                    sa.Column('person_uuid', sa.String(length=32), nullable=False),
                    sa.Column('shopper_number', sa.Integer(), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='customer_shopper_fk_customer'),
                    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], name='customer_shopper_fk_person'),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('customer_uuid', 'shopper_number', name='customer_shopper_uq_shopper_number')
                    )
    op.create_index('customer_shopper_ix_customer', 'customer_shopper', ['customer_uuid'], unique=False)
    op.create_index('customer_shopper_ix_person', 'customer_shopper', ['person_uuid'], unique=False)
    op.create_table('customer_shopper_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('customer_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('person_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('shopper_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_customer_shopper_version_end_transaction_id'), 'customer_shopper_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_customer_shopper_version_operation_type'), 'customer_shopper_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_customer_shopper_version_transaction_id'), 'customer_shopper_version', ['transaction_id'], unique=False)

    # customer_shopper_history
    op.create_table('customer_shopper_history',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('shopper_uuid', sa.String(length=32), nullable=False),
                    sa.Column('start_date', sa.Date(), nullable=True),
                    sa.Column('end_date', sa.Date(), nullable=True),
                    sa.ForeignKeyConstraint(['shopper_uuid'], ['customer_shopper.uuid'], name='customer_shopper_history_fk_shopper'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_index('customer_shopper_history_ix_shopper', 'customer_shopper_history', ['shopper_uuid'], unique=False)
    op.create_table('customer_shopper_history_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('shopper_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('start_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('end_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_customer_shopper_history_version_end_transaction_id'), 'customer_shopper_history_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_customer_shopper_history_version_operation_type'), 'customer_shopper_history_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_customer_shopper_history_version_transaction_id'), 'customer_shopper_history_version', ['transaction_id'], unique=False)


def downgrade():

    # customer_shopper_history
    op.drop_index(op.f('ix_customer_shopper_history_version_transaction_id'), table_name='customer_shopper_history_version')
    op.drop_index(op.f('ix_customer_shopper_history_version_operation_type'), table_name='customer_shopper_history_version')
    op.drop_index(op.f('ix_customer_shopper_history_version_end_transaction_id'), table_name='customer_shopper_history_version')
    op.drop_table('customer_shopper_history_version')
    op.drop_index('customer_shopper_history_ix_shopper', table_name='customer_shopper_history')
    op.drop_table('customer_shopper_history')

    # customer_shopper
    op.drop_index(op.f('ix_customer_shopper_version_transaction_id'), table_name='customer_shopper_version')
    op.drop_index(op.f('ix_customer_shopper_version_operation_type'), table_name='customer_shopper_version')
    op.drop_index(op.f('ix_customer_shopper_version_end_transaction_id'), table_name='customer_shopper_version')
    op.drop_table('customer_shopper_version')
    op.drop_index('customer_shopper_ix_person', table_name='customer_shopper')
    op.drop_index('customer_shopper_ix_customer', table_name='customer_shopper')
    op.drop_table('customer_shopper')

    # customer
    op.drop_column('customer_version', 'account_holder_uuid')
    op.drop_constraint('customer_fk_account_holder', 'customer', type_='foreignkey')
    op.drop_column('customer', 'account_holder_uuid')
