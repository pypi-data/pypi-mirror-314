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
DEPRECATED: Authentication & Authorization

This entire module has been deprecated; please use the :term:`auth
handler` instead.
"""

import warnings

from passlib.context import CryptContext

from rattail.db import model


password_context = CryptContext(schemes=['bcrypt'])


def authenticate_user(session, userobj, password):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.authenticate_user()`
    instead.
    """
    warnings.warn("authenticate_user() function is deprecated; "
                  "please use AuthHandler.authenticate_user() instead",
                  DeprecationWarning, stacklevel=2)

    if isinstance(userobj, model.User):
        user = userobj
    else:
        user = session.query(model.User)\
                      .filter_by(username=userobj)\
                      .first()

    if user and user.active and user.password is not None:
        if password_context.verify(password, user.password):
            return user


def set_user_password(user, password):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.set_user_password()`
    instead.
    """
    warnings.warn("set_user_password() function is deprecated; "
                  "please use AuthHandler.set_user_password() instead",
                  DeprecationWarning, stacklevel=2)

    user.password = password_context.hash(password)


def special_role(session, uuid, name):
    """ """
    warnings.warn("special_role() function is deprecated; "
                  "please use AuthHandler._special_role() instead",
                  DeprecationWarning, stacklevel=2)

    role = session.get(model.Role, uuid)
    if not role:
        role = model.Role(uuid=uuid, name=name)
        session.add(role)
    return role


def administrator_role(session):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.get_role_administrator()`
    instead.
    """
    warnings.warn("administrator_role() function is deprecated; "
                  "please use AuthHandler.get_role_administrator() instead",
                  DeprecationWarning, stacklevel=2)

    return special_role(session, 'd937fa8a965611dfa0dd001143047286', 'Administrator')


def guest_role(session):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.get_role_anonymous()`
    instead.
    """
    warnings.warn("guest_role() function is deprecated; "
                  "please use AuthHandler.get_role_anonymous() instead",
                  DeprecationWarning, stacklevel=2)

    return special_role(session, 'f8a27c98965a11dfaff7001143047286', 'Guest')


def authenticated_role(session):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.get_role_authenticated()`
    instead.
    """
    warnings.warn("authenticated_role() function is deprecated; "
                  "please use AuthHandler.get_role_authenticated() instead",
                  DeprecationWarning, stacklevel=2)

    return special_role(session, 'b765a9cc331a11e6ac2a3ca9f40bc550', "Authenticated")


def grant_permission(role, permission):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.grant_permission()`
    instead.
    """
    warnings.warn("grant_permission() function is deprecated; "
                  "please use AuthHandler.grant_permission() instead",
                  DeprecationWarning, stacklevel=2)

    # TODO: Make this a `Role` method (or make `Role.permissions` a `set` so we
    # can do `role.permissions.add('some.perm')` ?).
    if permission not in role.permissions:
        role.permissions.append(permission)


def revoke_permission(role, permission):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.revoke_permission()`
    instead.
    """
    warnings.warn("revoke_permission() function is deprecated; "
                  "please use AuthHandler.revoke_permission() instead",
                  DeprecationWarning, stacklevel=2)

    if permission in role.permissions:
        role.permissions.remove(permission)


def has_permission(session, principal, permission, include_guest=True, include_authenticated=True):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.has_permission()`
    instead.
    """
    warnings.warn("has_permission() function is deprecated; "
                  "please use AuthHandler.has_permission() instead",
                  DeprecationWarning, stacklevel=2)

    if hasattr(principal, 'roles'):
        roles = list(principal.roles)
        if include_authenticated:
            roles.append(authenticated_role(session))
    elif principal is not None:
        roles = [principal]
    else:
        roles = []

    if include_guest:
        roles.append(guest_role(session))
    for role in roles:
        for perm in role.permissions:
            if perm == permission:
                return True
    return False


def cache_permissions(session, principal, include_guest=True, include_authenticated=True):
    """
    DEPRECATED; use
    :meth:`wuttjamaican:wuttjamaican.auth.AuthHandler.get_permissions()`
    instead.
    """
    warnings.warn("cache_permissions() function is deprecated; "
                  "please use AuthHandler.get_permissions() instead",
                  DeprecationWarning, stacklevel=2)

    # we will use any `roles` attribute which may be present.  in practice we
    # would be assuming a User in this case
    if hasattr(principal, 'roles'):
        roles = list(principal.roles)

        # here our User assumption gets a little more explicit
        if include_authenticated:
            roles.append(authenticated_role(session))

    # otherwise a non-null principal is assumed to be a Role
    elif principal is not None:
        roles = [principal]

    # fallback assumption is "no roles"
    else:
        roles = []

    # maybe include guest roles
    if include_guest:
        roles.append(guest_role(session))

    # build the permissions cache
    cache = set()
    for role in roles:
        cache.update(role.permissions)

    return cache
