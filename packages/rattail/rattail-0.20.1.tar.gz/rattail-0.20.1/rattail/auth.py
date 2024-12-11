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
Auth Handler

See also :doc:`rattail-manual:base/handlers/other/auth`.
"""

import secrets
import warnings

from sqlalchemy import orm
import sqlalchemy_continuum as continuum

from wuttjamaican import auth as base

from rattail.app import MergeMixin


class RattailAuthHandler(base.AuthHandler, MergeMixin):
    """
    Default :term:`auth handler` for Rattail.

    This is a subclass of :class:`wuttjamaican.auth.AuthHandler` but
    adds various methods and logic for Rattail.
    """

    ##############################
    # override methods
    ##############################

    def delete_user(self, user, **kwargs):
        """
        Delete the given user account.  Use with caution!  As this
        generally cannot be undone.

        Default behavior here is of course to delete the account, but
        it also tries to remove the user association from various
        places, in particular the continuum transactions table.

        .. warning::

           Please note that if the user was associated with any
           continuum transactions, the "author" for those transactions
           will be set to null.

        Depending on the DB schema and data present, deleting the user
        may still fail with an error (i.e. if the user is still
        referenced by other tables).
        """
        session = self.app.get_session(user)

        # TODO: once we can move the versioning to wuttjamaican, we
        # can stop overriding this method altogether

        # disassociate user from transactions
        if self.config.versioning_has_been_enabled:
            self.remove_user_from_continuum_transactions(user)

        session.delete(user)

        # TODO: should make sure no callers are expecting this!
        return True

    # nb. must use simple string here, instead of proper UUID
    def get_role_administrator(self, session, **kwargs):
        """ """
        return self._special_role(session, 'd937fa8a965611dfa0dd001143047286',
                                  "Administrator")

    # nb. must use simple string here, instead of proper UUID
    def get_role_anonymous(self, session, **kwargs):
        """ """
        return self._special_role(session, 'f8a27c98965a11dfaff7001143047286',
                                  "Anonymous")

    # nb. must use simple string here, instead of proper UUID
    def get_role_authenticated(self, session, **kwargs):
        """ """
        return self._special_role(session, 'b765a9cc331a11e6ac2a3ca9f40bc550',
                                  "Authenticated")

    ##############################
    # extra methods
    ##############################

    def authenticate_user_token(self, session, token):
        """
        Authenticate the given user API token string, and if valid,
        return the corresponding User object.
        """
        model = self.app.model

        try:
            token = session.query(model.UserAPIToken)\
                           .filter(model.UserAPIToken.token_string == token)\
                           .one()
        except orm.exc.NoResultFound:
            pass
        else:
            user = token.user
            if user.active:
                return user

    def get_short_display_name(self, user, **kwargs):
        """
        Returns "short display name" for the user.  This is for
        convenience of mobile view, at least...
        """
        # TODO: this should reference employee.short_name
        employee = self.app.get_employee(user)
        if employee and employee.display_name:
            return employee.display_name

        person = self.app.get_person(user)
        if person:
            if person.first_name and person.last_name:
                return "{} {}.".format(person.first_name, person.last_name[0])
            if person.first_name:
                return person.first_name

        return user.username

    def generate_raw_api_token(self):
        """
        Generate a new *raw* API token string.
        """
        return secrets.token_urlsafe()

    def add_api_token(self, user, description, **kwargs):
        """
        Add a new API token for the user.
        """
        model = self.app.model
        session = self.app.get_session(user)

        # generate raw API token, in the form required for use within
        # the API client
        token_string = self.generate_raw_api_token()

        # create DB record for the token
        token = model.UserAPIToken(
            user=user,
            description=description,
            token_string=token_string)
        session.add(token)

        return token

    def delete_api_token(self, token, **kwargs):
        """
        Delete a new API token for the user.
        """
        session = self.app.get_session(token)
        session.delete(token)

    def get_merge_preview_fields(self, **kwargs):
        """
        Returns a sequence of fields which will be used during a merge
        preview.
        """
        F = self.make_merge_field
        return [
            F('uuid'),
            F('username'),
            F('person_uuid', coalesce=True),
            F('person_name', coalesce=True),
            F('role_count'),    # coalesced manually
            F('active', coalesce=True),
            F('sent_message_count', additive=True),
            F('received_message_count', additive=True),
        ]

    def get_merge_preview_data(self, user, **kwargs):
        return {
            'uuid': user.uuid,
            'username': user.username,
            'person_uuid': user.person_uuid,
            'person_name': user.person.display_name if user.person else None,
            '_roles': user.roles, # needed for final role count
            'role_count': len(user.roles),
            'active': user.active,
            'sent_message_count': len(user.sent_messages),
            'received_message_count': len(user._messages),
        }

    def get_merge_resulting_data(self, removing, keeping, **kwargs):
        result = super().get_merge_resulting_data(removing, keeping, **kwargs)

        # nb. must "manually" coalesce the role count
        result['role_count'] = len(set(removing['_roles'] + keeping['_roles']))

        return result

    def why_not_merge(self, removing, keeping, **kwargs):

        if removing.sent_messages:
            return "Cannot (yet) remove a user who has sent messages"

        if removing._messages:
            return "Cannot (yet) remove a user who has received messages"

        if removing._roles:
            return "Cannot (yet) remove a user who is assigned to roles"

    def merge_update_keeping_object(self, removing, keeping):
        super().merge_update_keeping_object(removing, keeping)
        session = self.app.get_session(keeping)
        model = self.app.model

        # update any notes authored by old user, to reflect new user
        notes = session.query(model.Note)\
                       .filter(model.Note.created_by == removing)\
                       .all()
        for note in notes:
            note.created_by = keeping

    def remove_user_from_continuum_transactions(self, user):
        """
        Remove the given user from all Continuum transactions,
        i.e. all data versioning tables.

        You probably will not need to invoke this directly; it is
        invoked as needed from within :meth:`delete_user()`.

        :param user: A :class:`~rattail.db.model.users.User` instance
           which should be purged from the versioning tables.
        """
        session = self.app.get_session(user)
        model = self.app.model

        # remove the user from any continuum transactions
        # nb. we can use "any" model class here, to obtain Transaction
        Transaction = continuum.transaction_class(model.User)
        transactions = session.query(Transaction)\
                              .filter(Transaction.user_id == user.uuid)\
                              .all()
        for txn in transactions:
            txn.user_id = None

    ##############################
    # deprecated methods
    ##############################

    def cache_permissions(self, *args, **kwargs): # pragma: no cover
        warnings.warn("method is deprecated, please use "
                      "get_permissions() method instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_permissions(*args, **kwargs)

    def generate_preferred_username(self, *args, **kwargs):
        """ """
        warnings.warn("generate_preferred_username() is deprecated; "
                      "please use make_preferred_username() instead",
                      DeprecationWarning, stacklevel=2)
        return self.make_preferred_username(*args, **kwargs)

    def generate_unique_username(self, session, **kwargs):
        """ """
        warnings.warn("generate_unique_username() is deprecated; "
                      "please use make_unique_username() instead",
                      DeprecationWarning, stacklevel=2)
        return self.make_unique_username(session, **kwargs)

    def generate_username(self, *args, **kwargs): # pragma: no cover
        """ """
        warnings.warn("method is deprecated, please use "
                      "generate_preferred_username() method instead",
                      DeprecationWarning, stacklevel=2)
        return self.generate_preferred_username(*args, **kwargs)

    def get_email_address(self, user, **kwargs):
        """ """
        warnings.warn("auth.get_email_address(user) is deprecated; please "
                      "use app.get_contact_email_address(user) instead",
                      DeprecationWarning, stacklevel=2)
        return self.app.get_contact_email_address(user)

    # nb. technically the method is not deprecated, just a kwarg
    def get_permissions(self, *args, **kwargs):
        """ """
        if 'include_guest' in kwargs:
            warnings.warn("the include_guest param is deprecated; "
                          "please use include_anonymous instead",
                          DeprecationWarning, stacklevel=2)
            kwargs.setdefault('include_anonymous', kwargs.pop('include_guest'))
        return super().get_permissions(*args, **kwargs)

    # nb. technically the method is not deprecated, just a kwarg
    def has_permission(self, *args, **kwargs):
        """ """
        if 'include_guest' in kwargs:
            warnings.warn("the include_guest param is deprecated; "
                          "please use include_anonymous instead",
                          DeprecationWarning, stacklevel=2)
            kwargs.setdefault('include_anonymous', kwargs.pop('include_guest'))
        return super().has_permission(*args, **kwargs)

    ##############################
    # internal methods
    ##############################

    def _role_is_pertinent(self, role):
        if role.node_type:
            if role.node_type == self.config.node_type():
                return True
            return False
        return True


class AuthHandler(RattailAuthHandler):

    def __init__(self, *args, **kwargs):
        warnings.warn("rattail.auth.AuthHandler is deprecated; "
                      "please use RattailAuthHandler instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
