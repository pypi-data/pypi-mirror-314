# -*- coding: utf-8; -*-
"""rename constraints per wutta

Revision ID: f6e95c74d8db
Revises: 4e7b6d8e71a4
Create Date: 2024-07-14 14:09:27.178397

"""

# revision identifiers, used by Alembic.
revision = 'f6e95c74d8db'
down_revision = '4e7b6d8e71a4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # uq_role_name
    op.drop_constraint('role_uq_name', 'role', type_='unique')
    op.create_unique_constraint(op.f('uq_role_name'), 'role', ['name'])

    # fk_permission_role_uuid_role
    op.drop_constraint('permission_fk_role', 'permission', type_='foreignkey')
    op.create_foreign_key('fk_permission_role_uuid_role',
                          'permission', 'role',
                          ['role_uuid'], ['uuid'])

    # fk_user_person_uuid_person
    op.drop_constraint('user_fk_person', 'user', type_='foreignkey')
    op.create_foreign_key('fk_user_person_uuid_person',
                          'user', 'person',
                          ['person_uuid'], ['uuid'])

    # uq_user_username
    op.drop_constraint('user_uq_username', 'user', type_='unique')
    op.create_unique_constraint(op.f('uq_user_username'), 'user', ['username'])

    # fk_user_x_role_role_uuid_role
    op.drop_constraint('user_x_role_fk_role', 'user_x_role', type_='foreignkey')
    op.create_foreign_key('fk_user_x_role_role_uuid_role',
                          'user_x_role', 'role',
                          ['role_uuid'], ['uuid'])

    # fk_user_x_role_user_uuid_user
    op.drop_constraint('user_x_role_fk_user', 'user_x_role', type_='foreignkey')
    op.create_foreign_key('fk_user_x_role_user_uuid_user',
                          'user_x_role', 'user',
                          ['user_uuid'], ['uuid'])


def downgrade():

    # fk_user_x_role_user_uuid_user
    op.drop_constraint('fk_user_x_role_user_uuid_user', 'user_x_role', type_='foreignkey')
    op.create_foreign_key('user_x_role_fk_user',
                          'user_x_role', 'user',
                          ['user_uuid'], ['uuid'])

    # fk_user_x_role_role_uuid_role
    op.drop_constraint('fk_user_x_role_role_uuid_role', 'user_x_role', type_='foreignkey')
    op.create_foreign_key('user_x_role_fk_role',
                          'user_x_role', 'role',
                          ['role_uuid'], ['uuid'])

    # uq_user_username
    op.drop_constraint(op.f('uq_user_username'), 'user', type_='unique')
    op.create_unique_constraint('user_uq_username', 'user', ['username'])

    # fk_user_person_uuid_person
    op.drop_constraint('fk_user_person_uuid_person', 'user', type_='foreignkey')
    op.create_foreign_key('user_fk_person',
                          'user', 'person',
                          ['person_uuid'], ['uuid'])

    # fk_permission_role_uuid_role
    op.drop_constraint('fk_permission_role_uuid_role', 'permission', type_='foreignkey')
    op.create_foreign_key('permission_fk_role',
                          'permission', 'role',
                          ['role_uuid'], ['uuid'])

    # uq_role_name
    op.drop_constraint(op.f('uq_role_name'), 'role', type_='unique')
    op.create_unique_constraint('role_uq_name', 'role', ['name'])
