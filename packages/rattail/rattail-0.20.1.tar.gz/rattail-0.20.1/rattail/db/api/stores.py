# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
API for Store Models
"""

import warnings

from sqlalchemy.orm.exc import NoResultFound

from rattail.db import model


def get_store(session, key):
    """ DEPRECATED """
    warnings.warn("db.api.get_store() function is deprecated; "
                  "please use OrgHandler.get_store() method instead",
                  DeprecationWarning, stacklevel=2)

    # Store.uuid match?
    store = session.get(model.Store, key)
    if store:
        return store

    # Store.id match?
    try:
        return session.query(model.Store).filter_by(id=key).one()
    except NoResultFound:
        pass

    # Try settings, if value then recurse.
    from rattail.db.api import get_setting
    key = get_setting(session, 'rattail.store.{0}'.format(key))
    if key:
        return get_store(session, key)
