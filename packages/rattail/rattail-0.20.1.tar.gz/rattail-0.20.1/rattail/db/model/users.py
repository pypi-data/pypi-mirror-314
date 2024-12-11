# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data Models for Users & Permissions
"""

import datetime
import warnings

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy

from rattail.db.model import Base, uuid_column, uuid_fk_column, getset_factory, Person
 

class Role(Base):
    """
    Represents a role within the system; used to manage permissions.
    """
    __tablename__ = 'role'
    __versioned__ = {}

    uuid = uuid_column()

    name = sa.Column(sa.String(length=100), nullable=False, unique=True, doc="""
    Name for the role.  Each role must have a name, which must be unique.
    """)

    adminish = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating that the role is "admin-ish" - i.e. only users who
    belong to the true Administrator role, should be allowed to
    (un)assign users to this role.
    """)

    session_timeout = sa.Column(sa.Integer(), nullable=True, doc="""
    Optional session timeout value for the role, in seconds.  If this is set to
    zero, the role's users will have no session timeout.  A value of ``None``
    means the role has no say in the timeout.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Any arbitrary notes for the role.
    """)

    sync_me = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating that the Role - its primary attributes, and list
    of permissions - should be synced across all nodes.

    So if set, when the role changes at one node then that change
    should propagate to all other nodes.

    Note that this does *not* include the user list by default; see
    :attr:`sync_users` to add that.

    Note that if this flag is set, the role will be synced to *all*
    nodes regardless of node type.  See also :attr:`node_type`.
    """)

    sync_users = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating that the user list for the role should be synced
    across all nodes.  This has no effect unless :attr:`sync_me` is
    also set.

    Note that if this flag is set, the role's user list will be synced
    to *all* nodes regardless of node type.  See also
    :attr:`node_type`.
    """)

    node_type = sa.Column(sa.String(length=100), nullable=True, doc="""
    Type of node for which this role is applicable.  This is probably
    only useful if the :attr:`sync_me` flag is set.

    If set, this value must match a node's configured type, or else it
    will be ignored by that node.  See also
    :meth:`~rattail.config.RattailConfig.node_type()` for how a node's
    type is determined.  If there is no value set for this field then
    the role will be honored by all nodes in which it exists (which is
    just one unless ``sync_me`` is set, in which case all nodes would
    have it).

    It is useful in combination with ``sync_me`` in that it allows a
    certain role to be "global" (synced) and yet only be "effective"
    for certain nodes.  Probably the most common scenario is where you
    have a host node and several store nodes, and you want to manage
    the store roles "globally" but avoid granting unwanted access to
    the host node.  So you'd set the ``sync_me`` flag but also set
    ``node_type`` to e.g. ``'store'``.
    """)

    _users = orm.relationship(
        'UserRole',
        cascade='all, delete-orphan',
        back_populates='role',
        cascade_backrefs=False)

    users = association_proxy(
        '_users', 'user',
        creator=lambda u: UserRole(user=u),
        getset_factory=getset_factory)

    def __str__(self):
        return self.name or ''


class Permission(Base):
    """
    Represents permission a role has to do a particular thing.
    """
    __tablename__ = 'permission'
    # __versioned__ = {}

    role_uuid = uuid_fk_column('role.uuid', primary_key=True, nullable=False)

    permission = sa.Column(sa.String(length=254), primary_key=True)

    def __str__(self):
        return self.permission or ''


Role._permissions = orm.relationship(
    Permission, backref='role',
    cascade='save-update, merge, delete, delete-orphan')

Role.permissions = association_proxy(
    '_permissions', 'permission',
    creator=lambda p: Permission(permission=p),
    getset_factory=getset_factory)


class User(Base):
    """
    Represents a user of the system.

    This may or may not correspond to a real person, i.e. some users may exist
    solely for automated tasks.
    """
    __tablename__ = 'user'
    __table_args__ = (
        sa.Index('user_ix_person', 'person_uuid'),
    )
    __versioned__ = {'exclude': ['password', 'salt', 'last_login']}

    uuid = uuid_column()
    username = sa.Column(sa.String(length=25), nullable=False, unique=True)
    password = sa.Column(sa.String(length=60))
    salt = sa.Column(sa.String(length=29))

    person_uuid = uuid_fk_column('person.uuid', nullable=True)
    person = orm.relationship(
        Person,
        uselist=False,
        doc="""
        Reference to the person whose user account this is.
        """,
        backref=orm.backref(
            'users',
            cascade_backrefs=False,
            doc="""
            List of user accounts for the person.  Typically there is
            only one user account per person, but technically multiple
            are allowed.
            """))

    active = sa.Column(sa.Boolean(), nullable=False, default=True, doc="""
    Whether the user is active, e.g. allowed to log in via the UI.
    """)

    active_sticky = sa.Column(sa.Boolean(), nullable=True, doc="""
    Optional flag, motivation behind which is as follows: If you import user
    accounts from another system, esp. on a regular basis, you might be keeping
    the :attr:`active` flag in sync along with that.  But in some cases you
    might want to *not* keep the active flag in sync, for certain accounts.
    Hence this "active sticky" flag, which may be used to mark certain accounts
    as off-limits from the general active flag sync.
    """)

    prevent_password_change = sa.Column(sa.Boolean(), nullable=True, doc="""
    If set, this user cannot change their own password, *and* the
    password is not editable when e.g. a manager edits this user
    record.  So if set, only root can change this user's password.
    """)

    local_only = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the user account is somehow specific to the "local" app
    node etc. and should not be synced elsewhere.
    """)

    last_login = sa.Column(sa.DateTime(), nullable=True, doc="""
    Timestamp when user last logged into the system.
    """)

    def __str__(self):
        if self.person and str(self.person):
            return str(self.person)
        return self.username or ''

    @property
    def display_name(self):
        """
        Display name for the user.
        
        Returns :attr:`Person.display_name` if available; otherwise returns
        :attr:`username`.
        """
        if self.person and self.person.display_name:
            return self.person.display_name
        return self.username

    @property
    def employee(self):
        """
        DEPRECATED

        Reference to the :class:`Employee` associated with the user, if any.
        """
        warnings.warn("user.employee is deprecated; please use "
                      "app.get_employee(user) instead",
                      DeprecationWarning, stacklevel=2)
        if self.person:
            return self.person.employee

    def get_short_name(self):
        """
        Returns "short name" for the user.  This is for convenience of mobile
        view, at least...
        """
        warnings.warn("user.get_short_name() is deprecated; please use "
                      "AuthHandler.get_short_display_name(user) instead",
                      DeprecationWarning, stacklevel=2)

        # TODO: this should reference employee.short_name
        employee = self.employee
        if employee and employee.display_name:
            return employee.display_name

        person = self.person
        if person:
            if person.first_name and person.last_name:
                return "{} {}.".format(person.first_name, person.last_name[0])
            if person.first_name:
                return person.first_name

        return self.username

    def get_email_address(self):
        """
        DEPRECATED

        Returns the primary email address for the user (as unicode string), or
        ``None``.  Note that currently there is no direct association between a
        User and an EmailAddress, so the Person and Customer relationships are
        navigated in an attempt to locate an address.
        """
        warnings.warn("user.get_email_address() is deprecated; please "
                      "use app.get_contact_email_address(user) instead",
                      DeprecationWarning, stacklevel=2)
        if self.person:
            if self.person.email:
                return self.person.email.address
            for customer in self.person.customers:
                if customer.email:
                    return customer.email.address

    @property
    def email_address(self):
        """
        DEPRECATED

        Convenience attribute which invokes :meth:`get_email_address()`.

        .. note::
           The implementation of this may change some day, e.g. if the User is
           given an association to EmailAddress in the data model.
        """
        warnings.warn("user.email_address is deprecated; please "
                      "use app.get_contact_email_address(user) instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_email_address()

    def is_admin(self):
        """
        DEPRECATED; use
        :meth:`rattail.auth.AuthHandler.user_is_admin()` instead.
        """
        warnings.warn("user.is_admin() is deprecated; "
                      "please use AuthHandler.user_is_admin(user) instead",
                      DeprecationWarning, stacklevel=2)

        from rattail.db.auth import administrator_role

        session = orm.object_session(self)
        return administrator_role(session) in self.roles

    def record_event(self, type_code, **kwargs):
        kwargs['type_code'] = type_code
        self.events.append(UserEvent(**kwargs))


Person.make_proxy(User, 'person', 'first_name')
Person.make_proxy(User, 'person', 'last_name')
Person.make_proxy(User, 'person', 'display_name')


class UserRole(Base):
    """
    Represents the association between a :class:`User` and a :class:`Role`.
    """
    __tablename__ = 'user_x_role'
    __versioned__ = {}

    uuid = uuid_column()
    user_uuid = uuid_fk_column('user.uuid', nullable=False)

    role_uuid = uuid_fk_column('role.uuid', nullable=False)
    role = orm.relationship(Role, back_populates='_users')


User._roles = orm.relationship(
    UserRole, backref='user',
    cascade='all, delete-orphan')

User.roles = association_proxy(
    '_roles', 'role',
    creator=lambda r: UserRole(role=r),
    getset_factory=getset_factory)


class UserEvent(Base):
    """
    Represents an event associated with a user.
    """
    __tablename__ = 'user_event'
    __table_args__ = (
        sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'],
                                name='user_event_fk_user'),
    )

    uuid = uuid_column()

    user_uuid = sa.Column(sa.String(length=32), nullable=False)
    user = orm.relationship(
        User,
        doc="""
        Reference to the user whose event this is.
        """,
        backref=orm.backref(
            'events',
            cascade='all, delete-orphan',
            cascade_backrefs=False,
            doc="""
            Sequence of events for the user.
            """))

    type_code = sa.Column(sa.Integer(), nullable=False, doc="""
    Type code for the event.
    """)

    occurred = sa.Column(sa.DateTime(), nullable=True, default=datetime.datetime.utcnow, doc="""
    Timestamp at which the event occurred.
    """)


class UserAPIToken(Base):
    """
    User authentication token for use with Tailbone API
    """
    __tablename__ = 'user_api_token'
    __table_args__ = (
        sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'],
                                name='user_api_token_fk_user'),
    )
    __versioned__ = {}
    model_title = "API Token"
    model_title_plural = "API Tokens"

    uuid = uuid_column()

    user_uuid = sa.Column(sa.String(length=32), nullable=False, doc="""
    Reference to the User associated with the token.
    """)
    user = orm.relationship(
        'User',
        doc="""
        Reference to the User associated with the token.
        """,
        backref=orm.backref(
            'api_tokens',
            cascade_backrefs=False,
            order_by='UserAPIToken.created',
            doc="""
            List of API tokens for the user.
            """))

    description = sa.Column(sa.String(length=255), nullable=False, doc="""
    Description of the token.
    """)

    token_string = sa.Column(sa.String(length=255), nullable=False, doc="""
    Token string, to be used by API clients.
    """)

    created = sa.Column(sa.DateTime(), nullable=False, default=datetime.datetime.utcnow, doc="""
    Date/time when the token was created.
    """)

    def __str__(self):
        return self.description or ""
