# -*- coding: utf-8 -*-
"""add VendorSampleFile

Revision ID: e206b9457091
Revises: 31b0b868d6f0
Create Date: 2023-02-22 18:55:50.567493

"""

# revision identifiers, used by Alembic.
revision = 'e206b9457091'
down_revision = '31b0b868d6f0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # vendor_sample_file
    op.create_table('vendor_sample_file',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('vendor_uuid', sa.String(length=32), nullable=False),
                    sa.Column('file_type', sa.String(length=100), nullable=False),
                    sa.Column('filename', sa.String(length=100), nullable=False),
                    sa.Column('bytes', sa.LargeBinary(), nullable=False),
                    sa.Column('effective_date', sa.Date(), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('created_by_uuid', sa.String(length=32), nullable=False),
                    sa.ForeignKeyConstraint(['created_by_uuid'], ['user.uuid'], name='vendor_sample_file_fk_user'),
                    sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'], name='vendor_sample_file_fk_vendor'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('vendor_sample_file_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('vendor_uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('file_type', sa.String(length=100), autoincrement=False, nullable=False),
                    sa.Column('filename', sa.String(length=100), autoincrement=False, nullable=False),
                    sa.Column('effective_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('notes', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('created_by_uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_vendor_sample_file_version_end_transaction_id'), 'vendor_sample_file_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_vendor_sample_file_version_operation_type'), 'vendor_sample_file_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_vendor_sample_file_version_transaction_id'), 'vendor_sample_file_version', ['transaction_id'], unique=False)


def downgrade():

    # vendor_sample_file
    op.drop_index(op.f('ix_vendor_sample_file_version_transaction_id'), table_name='vendor_sample_file_version')
    op.drop_index(op.f('ix_vendor_sample_file_version_operation_type'), table_name='vendor_sample_file_version')
    op.drop_index(op.f('ix_vendor_sample_file_version_end_transaction_id'), table_name='vendor_sample_file_version')
    op.drop_table('vendor_sample_file_version')
    op.drop_table('vendor_sample_file')
