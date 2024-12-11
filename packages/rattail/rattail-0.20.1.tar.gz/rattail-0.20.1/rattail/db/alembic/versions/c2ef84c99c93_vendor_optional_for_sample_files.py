# -*- coding: utf-8; -*-
"""vendor optional for sample files

Revision ID: c2ef84c99c93
Revises: 6f0659414074
Create Date: 2024-11-02 19:36:53.780559

"""

# revision identifiers, used by Alembic.
revision = 'c2ef84c99c93'
down_revision = '6f0659414074'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # vendor_sample_file
    op.alter_column('vendor_sample_file', 'vendor_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)


def downgrade():

    # vendor_sample_file
    op.alter_column('vendor_sample_file', 'vendor_uuid',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
