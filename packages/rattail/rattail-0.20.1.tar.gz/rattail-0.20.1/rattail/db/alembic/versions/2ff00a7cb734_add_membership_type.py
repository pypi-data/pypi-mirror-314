# -*- coding: utf-8; -*-
"""add membership_type

Revision ID: 2ff00a7cb734
Revises: 4747a017b8f9
Create Date: 2023-06-06 12:11:21.922167

"""

# revision identifiers, used by Alembic.
revision = '2ff00a7cb734'
down_revision = '4747a017b8f9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # membership_type
    op.create_table('membership_type',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.String(length=20), nullable=True),
                    sa.Column('number', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('membership_type_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_membership_type_version_end_transaction_id'), 'membership_type_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_membership_type_version_operation_type'), 'membership_type_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_membership_type_version_transaction_id'), 'membership_type_version', ['transaction_id'], unique=False)

    # member
    op.add_column('member', sa.Column('membership_type_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('member_fk_membership_type', 'member', 'membership_type', ['membership_type_uuid'], ['uuid'])
    op.add_column('member_version', sa.Column('membership_type_uuid', sa.String(length=32), autoincrement=False, nullable=True))


def downgrade():

    # member
    op.drop_column('member_version', 'membership_type_uuid')
    op.drop_constraint('member_fk_membership_type', 'member', type_='foreignkey')
    op.drop_column('member', 'membership_type_uuid')

    # membership_type
    op.drop_index(op.f('ix_membership_type_version_transaction_id'), table_name='membership_type_version')
    op.drop_index(op.f('ix_membership_type_version_operation_type'), table_name='membership_type_version')
    op.drop_index(op.f('ix_membership_type_version_end_transaction_id'), table_name='membership_type_version')
    op.drop_table('membership_type_version')
    op.drop_table('membership_type')
