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
API for Organizational Models
"""

import warnings

from sqlalchemy.orm.exc import NoResultFound

from rattail.db import model


def get_department(session, key):
    """ DEPRECATED """
    warnings.warn("db.api.get_department() function is deprecated; "
                  "please use OrgHandler.get_department() method instead",
                  DeprecationWarning, stacklevel=2)

    # Department.uuid match?
    department = session.get(model.Department, str(key))
    if department:
        return department

    # Department.number match?
    if isinstance(key, int) or key.isdigit():
        try:
            return session.query(model.Department).filter_by(number=key).one()
        except NoResultFound:
            pass

    # Try settings, if value then recurse.
    from rattail.db.api import get_setting
    key = get_setting(session, 'rattail.department.{0}'.format(key))
    if key is None:
        return None
    return get_department(session, key)


# TODO: need to refactor this into the AppHandler, or..?
def get_subdepartment(session, key):
    """ DEPRECATED """
    warnings.warn("db.api.get_subdepartment() function is deprecated; "
                  "please use OrgHandler.get_subdepartment() method instead",
                  DeprecationWarning, stacklevel=2)

    # Subdepartment.uuid match?
    subdepartment = session.get(model.Subdepartment, key)
    if subdepartment:
        return subdepartment

    # Subdepartment.number match?
    if isinstance(key, int) or key.isdigit():
        try:
            return session.query(model.Subdepartment).filter_by(number=key).one()
        except NoResultFound:
            pass

    # Try settings, if value then recurse.
    from rattail.db.api import get_setting
    key = get_setting(session, 'rattail.subdepartment.{0}'.format(key))
    if key is None:
        return None
    return get_subdepartment(session, key)
