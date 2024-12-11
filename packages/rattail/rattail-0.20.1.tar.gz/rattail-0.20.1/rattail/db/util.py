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
Database Utilities
"""

import decimal
import re
import pprint
import logging
import warnings

from rattail.util import make_uuid


log = logging.getLogger(__name__)


##############################
# people
##############################

def normalize_full_name(first_name, last_name):
    """
    Normalize the given first and last name to a "full" name value.  The
    fallback return value is an empty string.
    """
    first_name = (first_name or '').strip()
    last_name = (last_name or '').strip()
    if first_name and last_name:
        return "{} {}".format(first_name, last_name)
    if first_name:
        return first_name
    if last_name:
        return last_name
    return ''


##############################
# phone numbers
##############################

class PhoneValidator(object):
    """
    Simple validator, used to ensure a phone number matches the general
    expected pattern.
    """
    # NOTE: this was stolen from FormEncode
    _phoneRE = re.compile(r'^\s*(?:1-)?(\d\d\d)[\- \.]?(\d\d\d)[\- \.]?(\d\d\d\d)(?:\s*ext\.?\s*(\d+))?\s*$', re.I)

    def __init__(self, error=False):
        self.error = error

    def validate(self, number):
        if number:
            if not self._phoneRE.search(number):
                raise ValueError("Phone number is not valid")
            return number


def validate_phone_number(number, error=False):
    """
    Validate a single phone number.
    """
    validator = PhoneValidator(error=error)
    return validator.validate(number)


def normalize_phone_number(number):
    """
    Normalize a phone number to digits only.
    """
    if number is not None:
        return re.sub(r'\D', '', number)


def format_phone_number(number):
    """
    Returns a phone number in ``(XXX) XXX-XXXX`` format if possible; otherwise
    returns the argument unaltered.
    """
    original, number = number, normalize_phone_number(number)
    if number and len(number) == 10:
        return '({}) {}-{}'.format(number[:3], number[3:6], number[6:])
    return original


##############################
# products
##############################

def make_full_description(brand_name, description, size):
    """
    Combine the given field values into a complete description.
    """
    fields = [
        brand_name or '',
        description or '',
        size or '']
    fields = [f.strip() for f in fields if f.strip()]
    return ' '.join(fields)


##############################
# database
##############################

try:
    import sqlalchemy as sa
    from sqlalchemy import orm
    from sqlalchemy.ext.associationproxy import ASSOCIATION_PROXY
    from wuttjamaican.db import util as base
except ImportError:
    pass
else:

    class CounterMagic(object):
        """
        Provides magic counter values, to simulate PostgreSQL sequence.
        """

        def __init__(self, config):
            self.config = config
            self.metadata = sa.MetaData()

        def next_value(self, session, key):
            """
            Increment and return the next counter value for given key.
            """
            engine = session.bind
            table = sa.Table('counter_{}'.format(key), self.metadata,
                             sa.Column('value', sa.Integer(), primary_key=True))
            table.create(engine, checkfirst=True)
            with engine.begin() as cxn:
                result = cxn.execute(table.insert())
                return result.lastrowid


    class QuerySequence(object):
        """
        Simple wrapper for a SQLAlchemy (or Django, or other?) query, to make it
        sort of behave like a normal sequence, as much as needed to e.g. make an
        importer happy.
        """

        def __init__(self, query):
            self.query = query

        def __len__(self):
            try:
                return len(self.query)
            except TypeError:
                return self.query.count()

        def __iter__(self):
            return iter(self.query)


    def short_session(
            session=None,
            Session=None,
            commit=False,
            factory=None,
            config=None):
        """
        Compatibility wrapper around
        :class:`wuttjamaican:wuttjamaican.db.sess.short_session`.

        Note that this wrapper is a function whereas the upsream version
        is a proper context manager (class).  So calling this function
        will return a new instance of the upsream class.

        You should always specify keyword arguments when calling this
        function, since the arg order is different between this function
        and the upstream class.  And note that this function will
        eventually be deprecated and removed, so new code should call
        upstream directly.
        """
        from wuttjamaican.db import short_session

        warnings.warn("rattail.db.util.short_session() is deprecated; "
                      "please use wuttjamaican.db.short_session() instead",
                      DeprecationWarning, stacklevel=2)

        if not factory and Session:
            warnings.warn("passing a 'Session' kwarg is deprecated; "
                          "please pass 'factory' instead",
                          DeprecationWarning, stacklevel=2)
            factory = Session

        if not session and not factory and not config:
            from rattail.db import Session
            factory = Session

        return short_session(config=config, factory=factory, session=session, commit=commit)


    def finalize_session(session, dry_run=False, success=True):
        """
        Wrap up the given session, per the given arguments.  This is meant
        to provide a simple convenience, for commands which must do work
        within a DB session, but would like to support a "dry run" mode.
        """
        if dry_run:
            session.rollback()
            log.info("dry run, so transaction was aborted")
        elif success:
            session.commit()
            log.info("transaction was committed")
        else:
            session.rollback()
            log.warning("action failed, so transaction was rolled back")
        session.close()


    def get_fieldnames(config, obj, columns=True, proxies=True,
                       relations=False):
        """
        Produce a simple list of fieldnames for the given class,
        reflecting its table columns as well as any association proxies,
        and optionally, relationships.

        :param obj: Either a class or instance of a class, which derives
           from the base model class.

        :param columns: Whether or not to include simple columns.

        :param relations: Whether or not to include fields which represent
           relationships to other models.  If ``False`` (the default) then
           only "simple" fields will be included.

        :param proxies: Whether or not to include association proxy fields.
        """
        if isinstance(obj, type):
            cls = obj
        else:
            cls = obj.__class__

        mapper = orm.class_mapper(cls)
        fields = []

        # columns + relations
        prop_classes = []
        if columns:
            prop_classes.append(orm.ColumnProperty)
        if relations:
            prop_classes.append(orm.RelationshipProperty)
        if prop_classes:
            prop_classes = tuple(prop_classes)
            fields.extend([prop.key for prop in mapper.iterate_properties
                           if isinstance(prop, prop_classes)
                           and not prop.key.startswith('_')
                           and prop.key != 'versions'])

        # proxies
        if proxies:
            for key, desc in sa.inspect(cls).all_orm_descriptors.items():
                if desc.extension_type == ASSOCIATION_PROXY:

                    # must avoid association proxies which in turn use
                    # relationships, unless those are wanted by caller
                    if not relations:
                        # TODO: this probably needs help, i stumbled thru it..
                        prop = sa.inspect(desc.for_class(cls).target_class)\
                                 .get_property(desc.value_attr)
                        if isinstance(prop, orm.RelationshipProperty):
                            continue

                    fields.append(key)

        return fields


    def maxlen(attr):
        """
        Return the maximum length for the given attribute.
        """
        if len(attr.property.columns) == 1:
            type_ = attr.property.columns[0].type
            return getattr(type_, 'length', None)


    def maxval(attr):
        """
        Return the maximum value possible for the given attribute.
        """
        if len(attr.property.columns) == 1:
            typ = attr.property.columns[0].type

            if isinstance(typ, sa.Numeric) and not isinstance(typ, sa.Float):
                maxint = pow(10, (typ.precision - typ.scale)) - 1
                return decimal.Decimal('{}.{}'.format(maxint,
                                                      '9' * typ.scale))


    def make_topo_sortkey(model, metadata=None):
        """
        Returns a function suitable for use as a ``key`` kwarg to a standard Python
        sorting call.  This key function will expect a single class mapper and
        return a sequence number associated with that model.  The sequence is
        determined by SQLAlchemy's topological table sorting.
        """
        if metadata is None:
            metadata = model.Base.metadata

        tables = {}
        for i, table in enumerate(metadata.sorted_tables, 1):
            tables[table.name] = i

        # log.debug("topo sortkeys for '{}' will be:\n{}".format(model.__name__, pprint.pformat(
        #     [(i, name) for name, i in sorted(tables.items(), key=lambda t: t[1])])))

        def sortkey(name):
            if hasattr(model, name):
                mapper = orm.class_mapper(getattr(model, name))
                return tuple(tables[t.name] for t in mapper.tables)
            else:
                return tuple()

        return sortkey


    def uuid_column(*args, **kwargs):
        """
        Returns a UUID column for use as a table's primary key.

        See also :func:`wuttjamaican:wuttjamaican.db.util.uuid_column()`.

        We override the upstream logic (for now) to ensure we stick with
        ``String(length=32)`` for the column data type, whereas upstream
        may deviate in the future.
        """
        if not args:
            args = (sa.String(length=32),)
        kwargs.setdefault('default', make_uuid)
        return base.uuid_column(*args, **kwargs)


    def uuid_fk_column(target_column, *args, **kwargs):
        """
        Returns a UUID column for use as a foreign key to another table.

        :param target_column: Name of the table column on the remote side,
           e.g. ``'user.uuid'``.

        See also :func:`wuttjamaican:wuttjamaican.db.util.uuid_fk_column()`.

        We override the upstream logic (for now) to ensure we stick with
        ``String(length=32)`` for the column data type, whereas upstream
        may deviate in the future.
        """
        if not args:
            args = (sa.String(length=32), sa.ForeignKey(target_column))
        return base.uuid_fk_column(target_column, *args, **kwargs)
