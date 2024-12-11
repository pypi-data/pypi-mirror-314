# -*- coding: utf-8; -*-
"""add batch_pos_row.void

Revision ID: dd1a440a93f1
Revises: 3ef6a60a8898
Create Date: 2023-09-30 19:54:34.473398

"""

# revision identifiers, used by Alembic.
revision = 'dd1a440a93f1'
down_revision = '3ef6a60a8898'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_pos_row
    # nb. hack to get nullable=False for void
    op.add_column('batch_pos_row', sa.Column('void', sa.Boolean(), nullable=True))
    row = sa.sql.table('batch_pos_row', sa.sql.column('void'))
    op.execute(row.update().values({'void': False}))
    op.alter_column('batch_pos_row', 'void', nullable=False, existing_type=sa.Boolean())


def downgrade():

    # batch_pos_row
    op.drop_column('batch_pos_row', 'void')
