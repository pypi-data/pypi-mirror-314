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
Org Handler
"""

from sqlalchemy import orm

from wuttjamaican.app import GenericHandler


class OrgHandler(GenericHandler):
    """
    Base class and default implementation for org handlers.

    This is meant to provide logic around the "organization" - for
    instance stores and departments.
    """

    def get_store(self, session, key):
        """
        Locate and return a store for the given key, if possible.

        First the key is assumed to be a ``Store.id`` value.  If no
        matches are found, then it looks for a special setting in the
        database.  If one is found, ``get_store()`` is called again
        with its value.

        :param session: Active database session.

        :param key: Value to use when searching for the store.

        :returns: The :class:`~rattail.db.model.Store` instance if
           found; otherwise ``None``.
        """
        model = self.app.model

        # Store.uuid match?
        store = session.get(model.Store, key)
        if store:
            return store

        # Store.id match?
        try:
            return session.query(model.Store).filter_by(id=key).one()
        except orm.exc.NoResultFound:
            pass

        # try settings, if value then recurse.
        key = self.app.get_setting(session, f'rattail.store.{key}')
        if key:
            return self.get_store(session, key)

    def get_department(self, session, key):
        """
        Locate and return a department for the given key, if possible.

        First the key is assumed to be a ``Department.number`` value.
        If no matches are found, then it looks for a special setting
        in the database.  If one is found, ``get_department()`` is
        called again with its value.

        :param session: Active database session.

        :param key: Value to use when searching for the department.

        :returns: The :class:`~rattail.db.model.Department` instance
           if found; otherwise ``None``.
        """
        model = self.app.model

        # Department.uuid match?
        department = session.get(model.Department, str(key))
        if department:
            return department

        # Department.number match?
        if isinstance(key, int) or key.isdigit():
            try:
                return session.query(model.Department).filter_by(number=key).one()
            except orm.exc.NoResultFound:
                pass

        # try settings, if value then recurse.
        key = self.app.get_setting(session, f'rattail.department.{key}')
        if key is not None:
            return self.get_department(session, key)

    def get_subdepartment(self, session, key):
        """
        Locate and return a subdepartment for the given key, if
        possible.

        First the key is assumed to be a ``Subdepartment.number``
        value.  If no matches are found, then it looks for a special
        setting in the database.  If one is found,
        ``get_subdepartment()`` is called again with its value.

        :param session: Active database session.

        :param key: Value to use when searching for the subdepartment.

        :returns: The :class:`~rattail.db.model.Subdepartment`
           instance if found; otherwise ``None``.
        """
        model = self.app.model

        # Subdepartment.uuid match?
        subdepartment = session.get(model.Subdepartment, str(key))
        if subdepartment:
            return subdepartment

        # Subdepartment.number match?
        if isinstance(key, int) or key.isdigit():
            try:
                return session.query(model.Subdepartment).filter_by(number=key).one()
            except orm.exc.NoResultFound:
                pass

        # try settings, if value then recurse.
        key = self.app.get_setting(session, f'rattail.subdepartment.{key}')
        if key is not None:
            return self.get_subdepartment(session, key)
