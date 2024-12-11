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
Database Sessions
"""

import logging

import sqlalchemy
from sqlalchemy import orm


log = logging.getLogger(__name__)


class SessionBase(orm.Session):
    """
    Custom SQLAlchemy session base class, which adds some
    convenience methods related to the SQLAlchemy-Continuum
    integration.

    You should not instantiate this class directly; instead just
    use :class:`Session`.

    :param continuum_user: Optional user for Continuum versioning
       authorship.  If specified, the value is passed to
       :meth:`set_continuum_user()`.
    """

    def __init__(
            self,
            rattail_config=None,
            rattail_record_changes=None,
            continuum_user=None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.rattail_config = rattail_config

        # maybe record changes
        if rattail_record_changes is None:
            rattail_record_changes = getattr(self.bind, 'rattail_record_changes', False)
        if rattail_record_changes:
            from rattail.db.changes import record_changes
            record_changes(self, config=self.rattail_config)
        else:
            self.rattail_record_changes = False

        if continuum_user is None:
            self.continuum_user = None
        else:
            self.set_continuum_user(continuum_user)

        # maybe log the current db pool status
        if getattr(self.bind, 'rattail_log_pool_status', False):
            log.debug(self.bind.pool.status())

    def set_continuum_user(self, user_info):
        """
        Set the effective Continuum user for the session.

        :param user_info: May be a
          :class:`~rattail.db.model.users.User` instance, or the
          ``uuid`` or ``username`` for one.
        """
        if self.rattail_config:
            app = self.rattail_config.get_app()
            model = app.model
        else:
            from rattail.db import model

        if isinstance(user_info, model.User):
            user = self.merge(user_info)
        else:
            user = self.get(model.User, user_info)
            if not user:
                try:
                    user = self.query(model.User).filter_by(username=user_info).one()
                except orm.exc.NoResultFound:
                    user = None
        self.continuum_user = user


Session = orm.sessionmaker(class_=SessionBase, rattail_config=None, expire_on_commit=False)
