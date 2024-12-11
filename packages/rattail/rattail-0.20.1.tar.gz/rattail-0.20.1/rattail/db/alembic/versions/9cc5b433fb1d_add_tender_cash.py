# -*- coding: utf-8; -*-
"""add tender.cash

Revision ID: 9cc5b433fb1d
Revises: dd1a440a93f1
Create Date: 2023-10-01 18:43:13.587891

"""

# revision identifiers, used by Alembic.
revision = '9cc5b433fb1d'
down_revision = 'dd1a440a93f1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # tender
    op.add_column('tender', sa.Column('is_cash', sa.Boolean(), nullable=True))
    op.add_column('tender', sa.Column('allow_cash_back', sa.Boolean(), nullable=True))
    op.add_column('tender_version', sa.Column('is_cash', sa.Boolean(), autoincrement=False, nullable=True))
    op.add_column('tender_version', sa.Column('allow_cash_back', sa.Boolean(), autoincrement=False, nullable=True))


def downgrade():

    # tender
    op.drop_column('tender_version', 'allow_cash_back')
    op.drop_column('tender_version', 'is_cash')
    op.drop_column('tender', 'allow_cash_back')
    op.drop_column('tender', 'is_cash')
