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
Database Configuration
"""

import logging
import warnings

from wuttjamaican.util import parse_bool
from wuttjamaican.db import get_engines as wutta_get_engines
from wuttjamaican.db.conf import make_engine_from_config as wutta_make_engine_from_config

from rattail.exceptions import SQLAlchemyNotInstalled


log = logging.getLogger(__name__)


def get_engines(config, section='rattail.db'):
    """
    DEPRECATED; please use
    :func:`wuttjamaican:wuttjamaican.db.conf.get_engines()` instead.
    """
    warnings.warn("rattail.db.config.get_engines() is deprecated; "
                  "please use wuttjamaican.db.get_engines() instead",
                  DeprecationWarning, stacklevel=2)
    return wutta_get_engines(config, section)


def get_default_engine(config, section='rattail.db'):
    """
    DEPRECATED; please use
    :func:`wuttjamaican:wuttjamaican.db.conf.get_engines()` instead.
    """
    warnings.warn("rattail.db.config.get_default_engine() is deprecated; "
                  "please use wuttjamaican.db.get_engines() instead",
                  DeprecationWarning, stacklevel=2)
    return wutta_get_engines(config, section).get('default')


# TODO: DEPRECATED - this should be removed soon
def configure_session(config, session):
    """ """
    if config.getbool('rattail.db', 'changes.record', usedb=False):
        warnings.warn("setting rattail.db.changes.record is deprecated; "
                      "please set per-engine .record_changes instead",
                      DeprecationWarning)

        from rattail.db.changes import record_changes
        record_changes(session, config=config)


def configure_versioning(config, force=False, manager=None, plugins=None, **kwargs):
    """
    Configure Continuum versioning.
    """
    if not (force or config.versioning_enabled()):
        return

    try:
        from sqlalchemy.orm import configure_mappers
        import sqlalchemy_continuum as continuum
        from sqlalchemy_continuum.plugins import TransactionMetaPlugin
        from rattail.db.continuum import versioning_manager, RattailPlugin
    except ImportError as error:
        raise SQLAlchemyNotInstalled(error)
    else:
        kwargs['manager'] = manager or versioning_manager
        if plugins:
            kwargs['plugins'] = plugins
        else:
            kwargs['plugins'] = [TransactionMetaPlugin(), RattailPlugin()]
        log.debug("enabling Continuum versioning")
        continuum.make_versioned(**kwargs)

        # TODO: is this the best way/place to confirm versioning?
        app = config.get_app()
        try:
            # TODO: not sure why but if we don't load app.model here,
            # for some reason the alembic upgrade command may fail, if
            # any app models include the 'active_history' feature?!
            model = app.model

            # but when confirming if versioning is working, we
            # definitely need to check a "native" model and not
            # anything from app.model, which may use a totally
            # different base class with no versioning (i.e. wutta)
            from rattail.db.model import User

            configure_mappers()
            transaction_class = continuum.transaction_class(User)
            config.versioning_has_been_enabled = True
        except continuum.ClassNotVersioned:
            raise RuntimeError("Versioning is enabled and configured, but is not functional!  "
                               "This probably means the code import sequence is faulty somehow.  "
                               "Please investigate ASAP.")


def make_engine_from_config(
        config_dict,
        prefix='sqlalchemy.',
        **kwargs):
    """
    This is the same as
    :func:`wuttjamaican:wuttjamaican.db.conf.make_engine_from_config()`
    except Rattail may customize the engine a bit further:

    The engine can be told to "record changes" for sake of
    datasync; for instance:

    .. code-block:: ini

       [rattail.db]
       default.url = sqlite:///
       default.record_changes = true

    And/or the engine can be told to log its SQLAlchemy connection
    pool status:

    .. code-block:: ini

       [rattail.db]
       default.url = sqlite:///
       default.log_pool_status = true
    """
    config_dict = dict(config_dict)

    # stash flag for recording changes
    record_changes = False
    key = f'{prefix}record_changes'
    if key in config_dict:
        record_changes = parse_bool(config_dict.pop(key))

    # stash flag for logging db pool status
    log_pool_status = False
    key = f'{prefix}log_pool_status'
    if key in config_dict:
        log_pool_status = parse_bool(config_dict.pop(key))

    # make engine per usual
    engine = wutta_make_engine_from_config(config_dict, prefix=prefix, **kwargs)

    # then apply flags from stash
    if record_changes:
        engine.rattail_record_changes = True
    if log_pool_status:
        engine.rattail_log_pool_status = log_pool_status

    return engine
