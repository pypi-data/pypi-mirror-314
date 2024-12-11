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
Core Data Stuff
"""

import warnings

import sqlalchemy as sa


def uuid_column(*args, **kwargs):
    """
    DEPRECATED; use :func:`rattail.db.util.uuid_column()`
    instead.
    """
    warnings.warn("rattail.db.core.uuid_column() is deprecated; "
                  "please use rattail.db.util.uuid_column() instead",
                  DeprecationWarning, stacklevel=2)

    from rattail.db.util import uuid_column
    return uuid_column(*args, **kwargs)


def filename_column(*args, **kwargs):
    """
    Returns a SQLAlchemy Column object suitable for representing a filename.
    """
    kwargs.setdefault('nullable', True)
    kwargs.setdefault('doc', "Base name of the data file.")
    return sa.Column(sa.String(length=255), *args, **kwargs)


def getset_factory(collection_class, proxy):
    """
    Get/set factory for SQLAlchemy association proxy attributes.
    """
    def getter(obj):
        if obj is None:
            return None
        return getattr(obj, proxy.value_attr)

    def setter(obj, val):
        setattr(obj, proxy.value_attr, val)

    return getter, setter
