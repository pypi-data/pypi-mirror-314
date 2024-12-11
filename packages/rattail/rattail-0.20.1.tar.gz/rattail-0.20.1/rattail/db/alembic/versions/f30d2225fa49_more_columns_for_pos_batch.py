# -*- coding: utf-8; -*-
"""more columns for pos batch

Revision ID: f30d2225fa49
Revises: 6dd836b9829a
Create Date: 2023-09-26 15:31:45.927210

"""

# revision identifiers, used by Alembic.
revision = 'f30d2225fa49'
down_revision = '6dd836b9829a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # tender
    op.create_table('tender',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('code', sa.String(length=10), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('tender_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('code', sa.String(length=10), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('notes', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_tender_version_end_transaction_id'), 'tender_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_tender_version_operation_type'), 'tender_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_tender_version_transaction_id'), 'tender_version', ['transaction_id'], unique=False)

    # batch_pos
    op.drop_column('batch_pos', 'start_time')
    op.add_column('batch_pos', sa.Column('terminal_id', sa.String(length=20), nullable=True))
    op.add_column('batch_pos', sa.Column('cashier_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('batch_pos_fk_cashier', 'batch_pos', 'employee', ['cashier_uuid'], ['uuid'])
    op.add_column('batch_pos', sa.Column('customer_is_member', sa.Boolean(), nullable=True))
    op.add_column('batch_pos', sa.Column('customer_is_employee', sa.Boolean(), nullable=True))
    op.add_column('batch_pos', sa.Column('tender_total', sa.Numeric(precision=9, scale=2), nullable=True))
    # nb. hack to get nullable=False for training_mode
    op.add_column('batch_pos', sa.Column('training_mode', sa.Boolean(), nullable=True))
    batch = sa.sql.table('batch_pos', sa.sql.column('training_mode'))
    op.execute(batch.update().values({'training_mode': False}))
    op.alter_column('batch_pos', 'training_mode', nullable=False, existing_type=sa.Boolean())

    # batch_pos_row
    op.add_column('batch_pos_row', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('user_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('batch_pos_row_fk_user', 'batch_pos_row', 'user', ['user_uuid'], ['uuid'])
    op.add_column('batch_pos_row', sa.Column('upc', rattail.db.types.GPCType(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('item_id', sa.String(length=20), nullable=True))
    op.add_column('batch_pos_row', sa.Column('brand_name', sa.String(length=100), nullable=True))
    op.alter_column('batch_pos_row', 'description', existing_type=sa.VARCHAR(length=60),
                    type_=sa.String(length=255), existing_nullable=True)
    op.add_column('batch_pos_row', sa.Column('size', sa.String(length=255), nullable=True))
    op.add_column('batch_pos_row', sa.Column('full_description', sa.String(length=255), nullable=True))
    op.add_column('batch_pos_row', sa.Column('department_number', sa.Integer(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('department_name', sa.String(length=30), nullable=True))
    op.add_column('batch_pos_row', sa.Column('subdepartment_number', sa.Integer(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('subdepartment_name', sa.String(length=30), nullable=True))
    op.add_column('batch_pos_row', sa.Column('foodstamp_eligible', sa.Boolean(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('sold_by_weight', sa.Boolean(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('cost', sa.Numeric(precision=8, scale=3), nullable=True))
    op.add_column('batch_pos_row', sa.Column('tax1', sa.Boolean(), nullable=True))
    op.add_column('batch_pos_row', sa.Column('tax2', sa.Boolean(), nullable=True))
    op.drop_column('batch_pos_row', 'tax2_total')
    op.drop_column('batch_pos_row', 'tax1_total')
    op.add_column('batch_pos_row', sa.Column('tender_total', sa.Numeric(precision=9, scale=2), nullable=True))


def downgrade():

    # batch_pos_row
    op.drop_column('batch_pos_row', 'tender_total')
    op.add_column('batch_pos_row', sa.Column('tax1_total', sa.NUMERIC(precision=9, scale=2), autoincrement=False, nullable=True))
    op.add_column('batch_pos_row', sa.Column('tax2_total', sa.NUMERIC(precision=9, scale=2), autoincrement=False, nullable=True))
    op.drop_column('batch_pos_row', 'tax2')
    op.drop_column('batch_pos_row', 'tax1')
    op.drop_column('batch_pos_row', 'cost')
    op.drop_column('batch_pos_row', 'sold_by_weight')
    op.drop_column('batch_pos_row', 'foodstamp_eligible')
    op.drop_column('batch_pos_row', 'subdepartment_name')
    op.drop_column('batch_pos_row', 'subdepartment_number')
    op.drop_column('batch_pos_row', 'department_name')
    op.drop_column('batch_pos_row', 'department_number')
    op.drop_column('batch_pos_row', 'full_description')
    op.drop_column('batch_pos_row', 'size')
    op.alter_column('batch_pos_row', 'description', existing_type=sa.String(length=255),
                    type_=sa.VARCHAR(length=60), existing_nullable=True)
    op.drop_column('batch_pos_row', 'brand_name')
    op.drop_column('batch_pos_row', 'item_id')
    op.drop_column('batch_pos_row', 'upc')
    op.drop_constraint('batch_pos_row_fk_user', 'batch_pos_row', type_='foreignkey')
    op.drop_column('batch_pos_row', 'user_uuid')
    op.drop_column('batch_pos_row', 'timestamp')

    # batch_pos
    op.drop_column('batch_pos', 'customer_is_employee')
    op.drop_column('batch_pos', 'customer_is_member')
    op.drop_constraint('batch_pos_fk_cashier', 'batch_pos', type_='foreignkey')
    op.drop_column('batch_pos', 'cashier_uuid')
    op.drop_column('batch_pos', 'training_mode')
    op.drop_column('batch_pos', 'tender_total')
    op.drop_column('batch_pos', 'terminal_id')
    op.add_column('batch_pos', sa.Column('start_time', sa.DateTime(), nullable=True))

    # tender
    op.drop_index(op.f('ix_tender_version_transaction_id'), table_name='tender_version')
    op.drop_index(op.f('ix_tender_version_operation_type'), table_name='tender_version')
    op.drop_index(op.f('ix_tender_version_end_transaction_id'), table_name='tender_version')
    op.drop_table('tender_version')
    op.drop_table('tender')
