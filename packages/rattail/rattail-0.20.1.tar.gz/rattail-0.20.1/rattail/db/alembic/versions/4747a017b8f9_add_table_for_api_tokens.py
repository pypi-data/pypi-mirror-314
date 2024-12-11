# -*- coding: utf-8; -*-
"""add table for API Tokens

Revision ID: 4747a017b8f9
Revises: 0aeaac17cd6e
Create Date: 2023-05-14 11:18:12.265992

"""

# revision identifiers, used by Alembic.
revision = '4747a017b8f9'
down_revision = '0aeaac17cd6e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # user_api_token
    op.create_table('user_api_token',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('user_uuid', sa.String(length=32), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=False),
                    sa.Column('token_string', sa.String(length=255), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], name='user_api_token_fk_user'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('user_api_token_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('user_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('description', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('token_string', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_user_api_token_version_end_transaction_id'), 'user_api_token_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_user_api_token_version_operation_type'), 'user_api_token_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_user_api_token_version_transaction_id'), 'user_api_token_version', ['transaction_id'], unique=False)


def downgrade():

    # user_api_token
    op.drop_index(op.f('ix_user_api_token_version_transaction_id'), table_name='user_api_token_version')
    op.drop_index(op.f('ix_user_api_token_version_operation_type'), table_name='user_api_token_version')
    op.drop_index(op.f('ix_user_api_token_version_end_transaction_id'), table_name='user_api_token_version')
    op.drop_table('user_api_token_version')
    op.drop_table('user_api_token')
