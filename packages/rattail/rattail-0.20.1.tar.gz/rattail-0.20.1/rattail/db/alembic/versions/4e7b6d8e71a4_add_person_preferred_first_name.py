# -*- coding: utf-8; -*-
"""add person.preferred_first_name

Revision ID: 4e7b6d8e71a4
Revises: 11dd4ffbe8c9
Create Date: 2024-04-01 17:01:40.901202

"""

# revision identifiers, used by Alembic.
revision = '4e7b6d8e71a4'
down_revision = '11dd4ffbe8c9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # person
    op.add_column('person', sa.Column('preferred_first_name', sa.String(length=50), nullable=True))
    op.add_column('person_version', sa.Column('preferred_first_name', sa.String(length=50), autoincrement=False, nullable=True))


def downgrade():

    # person
    op.drop_column('person_version', 'preferred_first_name')
    op.drop_column('person', 'preferred_first_name')
