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
DataSync Configuration
"""

import re
import logging
import warnings

from rattail.config import ConfigProfile
from rattail.exceptions import ConfigurationError

from rattail.datasync.watchers import NullWatcher


log = logging.getLogger(__name__)


class DataSyncProfile(ConfigProfile):
    """
    Simple class to hold configuration for a DataSync "profile".  Each profile
    determines which database(s) will be watched for new changes, and which
    consumer(s) will then be instructed to process the changes.

    .. todo::
       This clearly needs more documentation.
    """
    section = 'rattail.datasync'

    def __init__(self, *args, **kwargs):
        load_disabled_consumers = kwargs.pop('load_disabled_consumers', False)
        super().__init__(*args, **kwargs)

        self.watcher_spec = self._config_string('watcher.spec')
        if not self.watcher_spec:
            # TODO: remove this fallback someday, since it won't work
            # with newer config logic
            self.watcher_spec = self._config_string('watcher', ignore_ambiguous=True)
            if self.watcher_spec:
                warnings.warn(f"URGENT: instead of '{self.section}.{self.prefix}.watcher', "
                              f"you should set '{self.section}.{self.prefix}.watcher.spec'",
                              DeprecationWarning, stacklevel=2)
            else:
                raise RuntimeError("no watcher spec defined")

        if self.watcher_spec == 'null':
            self.watcher = NullWatcher(self.config, self.key)
            self.watcher_kwargs = {}

        else:
            kwargs = {}

            # additional watcher kwargs will be read *directly* from
            # either the config file, or DB settings table
            handler = self.app.get_datasync_handler()
            if handler.should_use_profile_settings():

                # DB settings it is
                model = self.model
                with self.app.short_session() as s:
                    settings = s.query(model.Setting)\
                                .filter(model.Setting.name.like('rattail.datasync.{}.watcher.kwarg.%'.format(self.key)))\
                                .all()
                    for setting in settings:
                        name = setting.name.split('watcher.kwarg.')[1]
                        kwargs[name] = setting.value

            else: # config file

                pattern = re.compile(r'^{}\.watcher\.kwarg\.(?P<keyword>\w+)$'.format(self.key))
                settings = self.config.get_dict(self.section)
                for key in settings:
                    match = pattern.match(key)
                    if match:
                        keyword = match.group('keyword')
                        kwargs[keyword] = settings[key]

            # only capture "explicitly configured" watcher kwargs..
            # (nb. this is used for configuration of the kwargs)
            self.watcher_kwargs = dict(kwargs)

            # ..whereas in practice we also add one for the dbkey
            dbkey = self._config_string('watcher.db', default='default')
            kwargs['dbkey'] = dbkey

            # make the watcher
            factory = self.app.load_object(self.watcher_spec)
            self.watcher = factory(self.config, self.key, **kwargs)

        self.watcher.delay = self._config_int('watcher.delay', default=self.watcher.delay)
        self.watcher.retry_attempts = self._config_int('watcher.retry_attempts', default=self.watcher.retry_attempts)
        self.watcher.retry_delay = self._config_int('watcher.retry_delay', default=self.watcher.retry_delay)
        self.watcher.default_runas = self._config_string('consumers.runas')

        consumers = self._config_list('consumers.list')
        if not consumers:
            consumers = self._config_list('consumers', ignore_ambiguous=True)
            if consumers:
                warnings.warn(f"URGENT: instead of 'rattail.datasync.{self.key}.consumers', "
                              f"you should set 'rattail.datasync.{self.key}.consumers.list'",
                              DeprecationWarning, stacklevel=2)

        if consumers == ['self']:
            self.watcher.consumes_self = True
        else:
            self.watcher.consumes_self = False
            self.consumer_delay = self._config_int('consumer_delay', default=1)
            self.consumers = self.normalize_consumers(self.watcher.default_runas,
                                                      include_disabled=load_disabled_consumers)
            self.watcher.consumer_stub_keys = [c.key for c in self.consumers]

    def normalize_consumers(self, default_runas, include_disabled=False):
        consumers = []
        if include_disabled:
            enabled = get_consumer_keys(self.config, self.key,
                                        include_disabled=False)
        for key in get_consumer_keys(self.config, self.key,
                                     include_disabled=include_disabled):

            consumer_spec = self._config_string(f'consumer.{key}.spec')
            if not consumer_spec:
                consumer_spec = self._config_string(f'consumer.{key}', ignore_ambiguous=True)
                if consumer_spec:
                    warnings.warn(f"URGENT: instead of '{self.section}.{self.prefix}.consumer.{key}', "
                                  f"you should set '{self.section}.{self.prefix}.consumer.{key}.spec'",
                                  DeprecationWarning, stacklevel=2)
                else:
                    raise RuntimeError(f"must define '{self.section}.{self.prefix}.consumer.{key}.spec'")

            if consumer_spec == 'null':
                consumer_spec = 'rattail.datasync.consumers:NullTestConsumer'

            dbkey = self._config_string('consumer.{}.db'.format(key),
                                        default='default')
            runas = self._config_string('consumer.{}.runas'.format(key))
            try:
                factory = self.app.load_object(consumer_spec)
                consumer = factory(self.config, key, dbkey=dbkey,
                                   runas=runas or default_runas,
                                   watcher=self.watcher)
            except:
                log.debug("failed to load '%s' consumer for '%s' profile",
                          key, self.key, exc_info=True)
                if not include_disabled:
                    raise
            else:
                consumer.spec = consumer_spec
                consumer.delay = self._config_int(
                    'consumer.{}.delay'.format(key),
                    default=self.consumer_delay)
                consumer.retry_attempts = self._config_int(
                    'consumer.{}.retry_attempts'.format(key),
                    default=consumer.retry_attempts)
                consumer.retry_delay = self._config_int(
                    'consumer.{}.retry_delay'.format(key),
                    default=consumer.retry_delay)
                if include_disabled:
                    consumer.enabled = key in enabled
                consumers.append(consumer)
        return consumers


def get_consumer_keys(config, profile_key, include_disabled=False):

    # start with the primary set of consumer keys
    keys = config.getlist('rattail.datasync', f'{profile_key}.consumers.list')
    if not keys:
        keys = config.getlist('rattail.datasync', f'{profile_key}.consumers',
                              ignore_ambiguous=True)
        if keys:
            warnings.warn(f"URGENT: instead of 'rattail.datasync.{profile_key}.consumers', "
                          f"you should set 'rattail.datasync.{profile_key}.consumers.list'",
                          DeprecationWarning, stacklevel=2)
        else:
            keys = []

    if include_disabled:

        # first look in config file options
        settings = config.get_dict('rattail.datasync')
        pattern = re.compile(r'^{}\.consumer\.([^.]+)\.spec$'.format(profile_key))
        for key in settings:

            # find all consumers with spec defined
            match = pattern.match(key)
            if match:
                keys.append(match.group(1))

        # maybe also look for config settings in DB
        if config.usedb:
            app = config.get_app()
            model = app.model
            session = app.make_session()
            settings = session.query(model.Setting)\
                              .filter(model.Setting.name.like(f'rattail.datasync.{profile_key}.consumer.%.spec'))\
                              .all()
            pattern = re.compile(r'^rattail\.datasync\.{}\.consumer\.(.+)\.spec$')
            for setting in settings:
                match = pattern.match(setting.name)
                if match:
                    keys.append(match.group(1))
            session.close()

    return list(sorted(set(keys)))


def get_profile_keys(config, include_disabled=False):
    """
    Returns a list of profile keys used in the DataSync configuration.
    """
    # start with the primary set of watcher keys
    keys = config.getlist('rattail.datasync', 'watch',
                          default=[])

    if include_disabled:

        # first look in config file options
        settings = config.get_dict('rattail.datasync')
        pattern = re.compile(r'^(\S+)\.watcher\.spec$')
        for key in settings:

            # find all profiles with watcher defined
            match = pattern.match(key)
            if match:
                keys.append(match.group(1))

        # maybe also look for config settings in DB
        if config.usedb:
            app = config.get_app()
            model = app.model
            session = app.make_session()
            settings = session.query(model.Setting)\
                              .filter(model.Setting.name.like('rattail.datasync.%.watcher.spec'))\
                              .all()
            for setting in settings:
                parts = setting.name.split('.')
                keys.append('.'.join(parts[2:-2]))
            session.close()

    return list(sorted(set(keys)))


def load_profiles(config, include_disabled=False, ignore_problems=False):
    """
    Load all DataSync profiles defined within configuration.

    :param include_disabled: If true, then disabled profiles will be
       included in the return value; otherwise only currently-enabled
       profiles are returned.
    """
    # Make sure we have a top-level directive.
    keys = get_profile_keys(config, include_disabled=include_disabled)
    if not keys and not ignore_problems:
        raise ConfigurationError(
            "The DataSync configuration does not specify any profiles "
            "to be watched.  Please defined the 'watch' option within "
            "the [rattail.datasync] section of your config file.")

    if include_disabled:
        enabled = get_profile_keys(config, include_disabled=False)

    profiles = {}
    for key in keys:

        if include_disabled:
            try:
                profile = DataSyncProfile(config, key,
                                          load_disabled_consumers=True)
            except Exception as error:
                log.warning("could not create '%s' profile", key, exc_info=True)
                pass
            else:
                profile.enabled = key in enabled
                profiles[key] = profile

        else:
            profile = DataSyncProfile(config, key)
            profile.enabled = True
            profiles[key] = profile

    return profiles
