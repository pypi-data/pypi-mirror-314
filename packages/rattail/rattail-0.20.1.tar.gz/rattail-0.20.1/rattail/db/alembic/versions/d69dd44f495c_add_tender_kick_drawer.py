# -*- coding: utf-8; -*-
"""add tender.kick_drawer

Revision ID: d69dd44f495c
Revises: 9cc5b433fb1d
Create Date: 2023-10-06 20:06:56.557531

"""

# revision identifiers, used by Alembic.
revision = 'd69dd44f495c'
down_revision = '9cc5b433fb1d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # tender
    op.add_column('tender', sa.Column('kick_drawer', sa.Boolean(), nullable=True))
    op.add_column('tender', sa.Column('disabled', sa.Boolean(), nullable=True))
    op.add_column('tender_version', sa.Column('kick_drawer', sa.Boolean(), autoincrement=False, nullable=True))
    op.add_column('tender_version', sa.Column('disabled', sa.Boolean(), autoincrement=False, nullable=True))

    # batch_pos
    op.alter_column('batch_pos', 'tax1_total', new_column_name='tax_total')
    op.drop_column('batch_pos', 'tax2_total')

    # batch_pos_tax
    op.create_table('batch_pos_tax',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('batch_uuid', sa.String(length=32), nullable=False),
                    sa.Column('tax_uuid', sa.String(length=32), nullable=True),
                    sa.Column('tax_code', sa.String(length=30), nullable=False),
                    sa.Column('tax_rate', sa.Numeric(precision=7, scale=5), nullable=False),
                    sa.Column('tax_total', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.ForeignKeyConstraint(['batch_uuid'], ['batch_pos.uuid'], name='batch_pos_tax_fk_batch'),
                    sa.ForeignKeyConstraint(['tax_uuid'], ['tax.uuid'], name='batch_pos_tax_fk_tax'),
                    sa.PrimaryKeyConstraint('uuid')
                    )

    # batch_pow_row
    op.drop_column('batch_pos_row', 'tax2')
    op.drop_column('batch_pos_row', 'tax1')
    op.add_column('batch_pos_row', sa.Column('tax_code', sa.String(length=30), nullable=True))
    op.add_column('batch_pos_row', sa.Column('tender_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('batch_pos_row_fk_tender', 'batch_pos_row', 'tender', ['tender_uuid'], ['uuid'])


def downgrade():

    # batch_pos_row
    op.drop_constraint('batch_pos_row_fk_tender', 'batch_pos_row', type_='foreignkey')
    op.drop_column('batch_pos_row', 'tender_uuid')
    op.drop_column('batch_pos_row', 'tax_code')
    op.add_column('batch_pos_row', sa.Column('tax1', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('batch_pos_row', sa.Column('tax2', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # batch_pos_tax
    op.drop_table('batch_pos_tax')

    # batch_pos
    op.add_column('batch_pos', sa.Column('tax2_total', sa.NUMERIC(precision=9, scale=2), autoincrement=False, nullable=True))
    op.alter_column('batch_pos', 'tax_total', new_column_name='tax1_total')

    # tender
    op.drop_column('tender_version', 'disabled')
    op.drop_column('tender_version', 'kick_drawer')
    op.drop_column('tender', 'disabled')
    op.drop_column('tender', 'kick_drawer')
