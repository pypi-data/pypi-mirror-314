# -*- coding: utf-8; -*-
"""fix vendor sample file version table

Revision ID: 0aeaac17cd6e
Revises: 524373deb98e
Create Date: 2023-05-08 21:35:25.611702

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '0aeaac17cd6e'
down_revision = '524373deb98e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # vendor_sample_file
    op.alter_column('vendor_sample_file_version', 'vendor_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('vendor_sample_file_version', 'file_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('vendor_sample_file_version', 'filename',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('vendor_sample_file_version', 'created_by_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)


def downgrade():

    # vendor_sample_file
    op.alter_column('vendor_sample_file_version', 'created_by_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('vendor_sample_file_version', 'filename',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('vendor_sample_file_version', 'file_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('vendor_sample_file_version', 'vendor_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
