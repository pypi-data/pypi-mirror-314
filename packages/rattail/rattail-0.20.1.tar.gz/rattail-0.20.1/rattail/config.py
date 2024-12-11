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
Application Configuration
"""

import importlib
import os
import re
import sys
import warnings
import logging

from wuttjamaican.conf import (WuttaConfig, WuttaConfigExtension,
                               make_config as wutta_make_config,
                               generic_default_files)
from wuttjamaican.util import (parse_bool as wutta_parse_bool,
                               parse_list as wutta_parse_list)
from wuttjamaican.exc import ConfigurationError as WuttaConfigurationError

from rattail.exceptions import WindowsExtensionsNotInstalled, ConfigurationError


log = logging.getLogger(__name__)


def parse_bool(value): # pragma: no cover
    """ """
    warnings.warn("rattail.config.parse_bool() is deprecated; "
                  "please use wuttjamaican.util.parse_bool() instead",
                  DeprecationWarning, stacklevel=2)
    return wutta_parse_bool(value)


def parse_list(value): # pragma: no cover
    """ """
    warnings.warn("rattail.config.parse_list() is deprecated; "
                  "please use wuttjamaican.util.parse_list() instead",
                  DeprecationWarning, stacklevel=2)
    return wutta_parse_list(value)


class RattailConfig(WuttaConfig):
    """
    Configuration for Rattail apps.

    A single instance of this class is created on app startup, by way
    of calling :func:`rattail.config.make_config()`.

    This class is based on
    :class:`~wuttjamaican:wuttjamaican.conf.WuttaConfig` but adds many
    methods specific to Rattail.

    Some of the customizations supplied by this class are described
    below.

    .. attribute:: versioning_has_been_enabled

       Flag indicating whether SQLAlchemy-Continuum versioning has
       been enabled for the running app.  This gets set when
       :func:`~rattail.db.config.configure_versioning()` happens.
    """
    default_app_handler_spec = 'rattail.app:AppHandler'
    default_engine_maker_spec = 'rattail.db.config:make_engine_from_config'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('appname', 'rattail')
        super().__init__(*args, **kwargs)

        # this is false, unless/until it becomes true
        self.versioning_has_been_enabled = False

        # configure session if applicable
        from rattail.db import Session
        if Session:

            # nb. wutta configures its own Session but we must
            # configure ours separately (albeit with same engine)
            if hasattr(self, 'appdb_engine'):
                Session.configure(bind=self.appdb_engine)

            # TODO: eventually this should not be needed (?)
            Session.configure(rattail_config=self)

    @property
    def rattail_engines(self):
        warnings.warn("config.rattail_engines is deprecated; "
                      "please use config.appdb_engines instead",
                      DeprecationWarning, stacklevel=2)
        return self.appdb_engines

    @property
    def rattail_engine(self):
        warnings.warn("config.rattail_engine is deprecated; "
                      "please use config.appdb_engine instead",
                      DeprecationWarning, stacklevel=2)
        return self.appdb_engine

    @property
    def prioritized_files(self):
        """
        Backward-compatible property which just calls
        :meth:`~wuttjamaican:wuttjamaican.conf.WuttaConfig.get_prioritized_files()`.

        New code should use ``get_prioritized_files()`` instead of
        this property.
        """
        return self.get_prioritized_files()

    def setdefault(self, *args):
        """
        We override this method to support different calling signatures.

        :meth:`wuttjamaican:wuttjamaican.conf.WuttaConfig.setdefault()`
        normally expects just ``(key, value)`` args, but we also (for
        now) support the older style of ``(section, option, value)`` -
        *eventually* that will go away but probably not in the near
        future.  However new code should pass ``(key, value)`` since
        that is now the preferred signature.
        """
        # figure out what sort of args were passed
        if len(args) == 2:
            key, value = args
        elif len(args) == 3:
            section, option, value = args
            key = f'{section}.{option}'
        else:
            raise ValueError("must pass either 2 args (key, value), "
                             "or 3 args (section, option, value)")

        # then do normal logic
        super().setdefault(key, value)

    def get(self, *args, **kwargs):
        """
        We override this method to support different calling signatures.

        :meth:`wuttjamaican:wuttjamaican.conf.WuttaConfig.get()`
        normally expects just ``(key, ...)`` args, but we also (for
        now) support the older style of ``(section, option, ...)`` -
        *eventually* that will go away but probably not in the near
        future.  However new code should pass ``(key, ...)`` since
        that is now the preferred signature.
        """
        # figure out what sort of args were passed
        if len(args) == 1:
            key = args[0]
        elif len(args) == 2:
            section, option = args
            key = f'{section}.{option}'
        else:
            raise ValueError("must pass either 1 arg (key), "
                             "or 2 args (section, option)")

        # then do normal logic
        return super().get(key, **kwargs)

    def getbool(self, *args, **kwargs):
        """
        Backward-compatible alias for
        :meth:`~wuttjamaican:wuttjamaican.conf.WuttaConfig.get_bool()`.

        New code should use ``get_bool()`` instead of this method.
        """
        # TODO: eventually
        # warnings.warn("config.getbool() method is deprecated; "
        #               "please use config.get_bool() instead",
        #               DeprecationWarning, stacklevel=2)
        return self.get_bool(*args, **kwargs)

    def get_date(self, *args, **kwargs):
        """
        Retrieve a date value from config.

        Accepts same params as :meth:`get()` but if a value is found,
        it will be coerced to date via
        :meth:`rattail.app.AppHandler.parse_date()`.
        """
        value = self.get(*args, **kwargs)
        app = self.get_app()
        return app.parse_date(value)

    def getdate(self, *args, **kwargs):
        """
        Backward-compatible alias for :meth:`get_date()`.

        New code should use ``get_date()`` instead of this method.
        """
        # TODO: eventually
        # warnings.warn("config.getbool() method is deprecated; "
        #               "please use config.get_bool() instead",
        #               DeprecationWarning, stacklevel=2)
        return self.get_date(*args, **kwargs)

    def getint(self, *args, **kwargs):
        """
        Backward-compatible alias for
        :meth:`~wuttjamaican:wuttjamaican.conf.WuttaConfig.get_int()`.

        New code should use ``get_int()`` instead of this method.
        """
        # TODO: eventually
        # warnings.warn("config.getint() method is deprecated; "
        #               "please use config.get_int() instead",
        #               DeprecationWarning, stacklevel=2)
        return self.get_int(*args, **kwargs)

    def getlist(self, *args, **kwargs):
        """
        Backward-compatible alias for
        :meth:`~wuttjamaican:wuttjamaican.conf.WuttaConfig.get_list()`.

        New code should use ``get_list()`` instead of this method.
        """
        # TODO: eventually
        # warnings.warn("config.getlist() method is deprecated; "
        #               "please use config.get_list() instead",
        #               DeprecationWarning, stacklevel=2)
        return self.get_list(*args, **kwargs)

    def parse_bool(self, value):
        """
        Convenience method around the
        :func:`~wuttjamaican:wuttjamaican.util.parse_bool()` function.
        """
        return wutta_parse_bool(value)

    def parse_list(self, value):
        """
        Convenience method around the
        :func:`~wuttjamaican:wuttjamaican.util.parse_list()` function.
        """
        return wutta_parse_list(value)

    def make_list_string(self, values):
        """
        Coerce the given list of values to a string, for config
        storage.  If this string is later parsed via
        :meth:`parse_list()` then it should return the same list of
        values.

        For example::

           string = config.make_list_string(['foo', 'bar'])

           assert string == 'foo, bar'

           values = config.parse_list(string)

           assert values == ['foo', 'bar']
        """
        final = []
        for value in values:
            if ' ' in value:
                quote = '"' if "'" in value else "'"
                value = f"{quote}{value}{quote}"
            final.append(value)
        return ', '.join(final)

    def beaker_invalidate_setting(self, name):
        """
        Deprecated method for unused Beaker caching logic.

        This method has no effect and should not be used.
        """
        # TODO: eventually
        # warnings.warn("config.beaker_invalidate_setting() method is deprecated",
        #               DeprecationWarning, stacklevel=2)

    def node_type(self, default=None):
        """
        Returns the "type" of current node as string.  What this means
        will generally depend on the app logic.  There is no default
        node type unless caller provides one.
        """
        try:
            return self.require('rattail', 'node_type', usedb=False)
        except WuttaConfigurationError:
            if default:
                return default
            raise

    def get_model(self):
        """
        DEPRECATED; use
        :attr:`~wuttjamaican:wuttjamaican.app.AppHandler.model`
        instead.
        """
        warnings.warn("RattailConfig.get_model() is deprecated; "
                      "please use AppHandler.model instead",
                      DeprecationWarning, stacklevel=2)
        app = self.get_app()
        return app.model

    def get_enum(self, **kwargs):
        """
        Returns a reference to configured "enum" module; defaults to
        :mod:`rattail.enum`.
        """
        kwargs.setdefault('usedb', False)
        spec = self.get('rattail', 'enum', default='rattail.enum', **kwargs)
        return importlib.import_module(spec)

    def get_trainwreck_model(self):
        """
        Returns a reference to the configured data 'model' module for
        Trainwreck.  Note that there is *not* a default value for
        this; it must be configured or else calling this method will
        result in an error.
        """
        spec = self.require('rattail.trainwreck', 'model', usedb=False)
        return importlib.import_module(spec)

    def versioning_enabled(self):
        """
        Returns boolean indicating whether data versioning is enabled.
        """
        return self.getbool('rattail.db', 'versioning.enabled', usedb=False,
                            default=False)

    def product_key(self, **kwargs): # pragma: no cover
        """ """
        warnings.warn("config.product_key() is deprecated; please "
                      "use app.get_product_key_field() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_field()

    def product_key_title(self, key=None): # pragma: no cover
        """ """
        warnings.warn("config.product_key_title() is deprecated; please "
                      "use app.get_product_key_label() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_label(field=key)

    def app_package(self, default=None, warn=True):
        """ """
        if warn:
            warnings.warn("config.app_package() method is deprecated; "
                          "please use app.get_distribution() instead",
                          DeprecationWarning, stacklevel=2)
        if not default:
            return self.require('rattail', 'app_package')
        return self.get('rattail', 'app_package', default=default)

    def app_title(self, **kwargs):
        """ """
        warnings.warn("config.app_title() method is deprecated; "
                      "please use app.get_title() instead",
                      DeprecationWarning, stacklevel=2)
        app = self.get_app()
        return app.get_title(**kwargs)

    def node_title(self, **kwargs):
        """ """
        warnings.warn("config.node_title() method is deprecated; "
                      "please use app.get_node_title() instead",
                      DeprecationWarning, stacklevel=2)
        app = self.get_app()
        return app.get_node_title(**kwargs)

    def running_from_source(self):
        """
        Returns boolean indicating whether the app is running from
        source, as opposed to official release.

        .. warning::

           The utility of this method is questionable and it ideally
           will go away in the future.
        """
        return self.getbool('rattail', 'running_from_source', default=False)

    def demo(self):
        """
        Returns boolean indicating whether the app is running in demo mode

        .. warning::

           The utility of this method is questionable and it ideally
           will go away in the future.
        """
        return self.getbool('rattail', 'demo', default=False)

    def appdir(self, require=True, **kwargs):
        """
        Returns path to the local 'app' dir.
        """
        if require:
            path = os.path.join(sys.prefix, 'app')
            kwargs.setdefault('default', path)
        kwargs.setdefault('usedb', False)
        return self.get('rattail', 'appdir', **kwargs)

    def datadir(self, require=True):
        """
        Returns path to the 'data' dir, if known.
        """
        get = self.require if require else self.get
        return get('rattail', 'datadir')

    def workdir(self, require=True):
        """
        Returns path to the 'work' dir, if known.
        """
        get = self.require if require else self.get
        return get('rattail', 'workdir')

    def batch_filedir(self, key=None):
        """
        Returns path to root folder where batches (optionally of type
        ``key``) are stored.
        """
        path = os.path.abspath(self.require('rattail', 'batch.files'))
        if key:
            return os.path.join(path, key)
        return path

    def batch_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to a batch's data folder, with optional
        filename appended.  If ``makedirs`` is set, the batch data
        folder will be created if it does not already exist.
        """
        rootdir = self.batch_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def export_filedir(self, key=None):
        """
        Returns path to root folder where exports (optionally of type
        'key') are stored.
        """
        path = self.get('rattail', 'export.files')
        if not path:
            path = os.path.join(self.appdir(), 'data', 'exports')
        path = os.path.abspath(path)
        if key:
            return os.path.join(path, key)
        return path

    def export_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to export data file, generated from the given args.
        """
        rootdir = self.export_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_filedir(self):
        """
        Returns path to root folder where upgrade files are stored.
        """
        path = os.path.abspath(self.require('rattail.upgrades', 'files'))
        return path

    def upgrade_filepath(self, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to upgrade data file, generated from the given args.
        """
        rootdir = self.upgrade_filedir()
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_command(self, default='/bin/sleep 30'):
        """
        Returns command to be used when performing upgrades.
        """
        # TODO: what were those reasons then..?
        # NOTE: we don't allow command to be specified in DB, for
        # security reasons..
        return self.getlist('rattail.upgrades', 'command', usedb=False,
                            default=default)

    def base_url(self):
        """
        Returns the configured "base" (root) URL for the web app.
        """
        # first try "generic" config option
        url = self.get('rattail', 'base_url')

        # or use tailbone as fallback, since it's most likely
        if url is None:
            url = self.get('tailbone', 'url.base')
            if not url:
                url = self.get('tailbone', 'url', ignore_ambiguous=True)
                if url:
                    warnings.warn(f"URGENT: instead of 'tailbone.url', "
                                  f"you should set 'tailbone.url.base'",
                                  DeprecationWarning, stacklevel=2)

        if url is not None:
            return url.rstrip('/')

    def datasync_url(self, **kwargs):
        """
        Returns configured URL for managing datasync daemon.
        """
        return self.get('rattail.datasync', 'url', **kwargs)

    def single_store(self):
        """
        Returns boolean indicating whether the system is configured to behave
        as if it belongs to a single Store.
        """
        return self.getbool('rattail', 'single_store', default=False)

    def get_store(self, session):
        """
        Returns a :class:`rattail.db.model.Store` instance
        corresponding to app config, or ``None``.
        """
        store = self.get('rattail', 'store')
        if store:
            app = self.get_app()
            org_handler = app.get_org_handler()
            return org_handler.get_store(session, store)


class ConfigExtension(WuttaConfigExtension):
    """
    DEPRECATED - use
    :class:`wuttjamaican:wuttjamaican.conf.WuttaConfigExtension`
    instead.

    See also :class:`RattailConfigExtension`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn(f"rattail.config.ConfigExtension (for '{self.key}') is deprecated; "
                      "please use wuttjamaican.conf.WuttaConfigExtension instead",
                      DeprecationWarning, stacklevel=2)


class RattailConfigExtension(WuttaConfigExtension):
    """
    The :term:`config extension` for Rattail.

    This is a subclass of
    :class:`wuttjamaican:wuttjamaican.conf.WuttaConfigExtension`.

    This primarily exists to add default config settings for sake of
    the various importers etc. contained in the ``rattail`` package.

    .. note::

       If you are adding a new config extension, **do not subclass
       this**, but rather subclass
       :class:`wuttjamaican:wuttjamaican.conf.WuttaConfigExtension`
       directly.
    """
    key = 'rattail.db'

    def configure(self, config):
        """ """

        # rattail export-csv
        config.setdefault('rattail.importing', 'to_csv.from_rattail.export.default_handler',
                          'rattail.importing.exporters:FromRattailToCSV')
        config.setdefault('rattail.importing', 'to_csv.from_rattail.export.default_cmd',
                          'rattail export-csv')
        config.setdefault('rattail.importing', 'to_csv.from_rattail.export.legacy_handler_setting',
                          'rattail.exporting, csv.handler')

        # rattail export-rattail
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.default_handler',
                          'rattail.importing.rattail:FromRattailToRattailExport')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.default_cmd',
                          'rattail export-rattail')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.legacy_handler_setting',
                          'rattail.exporting, rattail.handler')

        # rattail import-csv
        config.setdefault('rattail.importing', 'to_rattail.from_csv.import.default_handler',
                          'rattail.importing.csv:FromCSVToRattail')
        config.setdefault('rattail.importing', 'to_rattail.from_csv.import.default_cmd',
                          'rattail import-csv')
        config.setdefault('rattail.importing', 'to_rattail.from_csv.import.legacy_handler_setting',
                          'rattail.importing, csv.handler')

        # rattail import-ifps
        config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.default_handler',
                          'rattail.importing.ifps:FromIFPSToRattail')
        config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.default_cmd',
                          'rattail import-ifps')
        config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.legacy_handler_setting',
                          'rattail.importing, ifps.handler')

        # rattail import-rattail
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.default_handler',
                          'rattail.importing.rattail:FromRattailToRattailImport')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.default_cmd',
                          'rattail import-rattail')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.legacy_handler_setting',
                          'rattail.importing, rattail.handler')

        # rattail import-rattail-bulk
        config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.default_handler',
                          'rattail.importing.rattail_bulk:BulkFromRattailToRattail')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.default_cmd',
                          'rattail import-rattail-bulk')
        config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.legacy_handler_setting',
                          'rattail.importing, rattail_bulk.handler')

        # rattail import-sample
        config.setdefault('rattail.importing', 'to_rattail.from_sample.import.default_handler',
                          'rattail.importing.sample:FromSampleToRattail')
        config.setdefault('rattail.importing', 'to_rattail.from_sample.import.default_cmd',
                          'rattail import-sample')
        config.setdefault('rattail.importing', 'to_rattail.from_sample.import.legacy_handler_setting',
                          'rattail.importing, sample.handler')

        # rattail import-versions
        config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.default_handler',
                          'rattail.importing.versions:FromRattailToRattailVersions')
        config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.default_cmd',
                          'rattail import-versions')
        config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.legacy_handler_setting',
                          'rattail.importing, versions.handler')

        # trainwreck export-trainwreck
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.default_handler',
                          'rattail.trainwreck.importing.trainwreck:FromTrainwreckToTrainwreckExport')
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.default_cmd',
                          'trainwreck export-trainwreck')
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.legacy_handler_setting',
                          'trainwreck.exporting, trainwreck.handler')

        # trainwreck import-self
        config.setdefault('rattail.importing', 'to_trainwreck.from_self.import.default_cmd',
                          'trainwreck import-self')

        # trainwreck import-trainwreck
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.default_handler',
                          'rattail.trainwreck.importing.trainwreck:FromTrainwreckToTrainwreckImport')
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.default_cmd',
                          'trainwreck import-trainwreck')
        config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.legacy_handler_setting',
                          'trainwreck.importing, trainwreck.handler')

        # nb. cannot fetch DB settings during init
        appdir = config.appdir(require=False, usedb=False)
        if not appdir:
            appdir = os.path.join(sys.prefix, 'app')

        poser = config.get('rattail', 'poser', usedb=False,
                           default=os.path.join(appdir, 'poser'))

        # add poser to path if it exists
        if os.path.isdir(poser) and poser not in sys.path:
            sys.path.append(poser)

    def startup(self, config):
        from rattail.db import Session
        if Session:

            # TODO: this should be removed, it sets 'record changes' globally
            from rattail.db.config import configure_session
            configure_session(config, Session)


def rattail_default_files(appname):
    """
    This is used in place of upstream
    :func:`wuttjamaican:wuttjamaican.conf.generic_default_files()` to
    customize the default files when none are specified at startup.

    Rattail has traditionally used
    e.g. ``/path/to/venv/app/quiet.conf`` as its "preferred default
    file" when running ad-hoc commands.  So this function will look
    for that file and return it if found; otherwise it just calls the
    upstream function.
    """
    # try to guess a default config path
    # TODO: for now, prefer app/quiet.conf if present, but
    # probably we should look for adhoc.conf instead, since
    # the point of this magic is to make running ad-hoc
    # commands easier..
    quiet = os.path.join(sys.prefix, 'app', 'quiet.conf')
    if os.path.exists(quiet):
        # this config is definitely app-specific
        return [quiet]

    return generic_default_files(appname)


def make_config(
        files=None,
        plus_files=None,
        versioning=None,
        **kwargs):
    """
    Make a new config object (presumably for global use), initialized
    per the given parameters and (usually) further modified by all
    registered config extensions.

    This is a wrapper around upstream
    :func:`wuttjamaican:wuttjamaican.conf.make_config()`; see those
    docs for most of the param descriptions.  Rattail customizes the
    logic as follows:

    :param versioning: Controls whether or not the versioning system
       is configured with the new config object.  If ``True``,
       versioning will be configured.  If ``False`` then it will not
       be configured.  If ``None`` (the default) then versioning will
       be configured only if the config values say that it should be.

    :returns: An instance of :class:`RattailConfig`.
    """
    # turn on display of rattail deprecation warnings by default
    # TODO: this should be configurable, and possibly live elsewhere?
    warnings.filterwarnings('default', category=DeprecationWarning,
                            module=r'^rattail')
    warnings.filterwarnings('default', category=DeprecationWarning,
                            module=r'^tailbone')
    warnings.filterwarnings('default', category=DeprecationWarning,
                            module=r'^wutt')

    # prep kwargs
    kwargs.setdefault('appname', 'rattail')
    kwargs.setdefault('default_files', rattail_default_files)
    kwargs.setdefault('factory', RattailConfig)

    # remove deprecated args
    kwargs.pop('use_wuttaconfig', None)

    # make config object
    config = wutta_make_config(files=files, plus_files=plus_files, **kwargs)

    if config.get_bool('rattail.suppress_psycopg2_wheel_warning', usedb=False):
        # TODO: revisit this, does it require action from us?
        # suppress this warning about psycopg2 wheel; not sure what it means yet
        # exactly but it's causing frequent noise for us...
        warnings.filterwarnings(
            'ignore',
            r'^The psycopg2 wheel package will be renamed from release 2\.8; in order to keep '
            r'installing from binary please use "pip install psycopg2-binary" instead\. For details '
            r'see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>\.',
            UserWarning,
            r'^psycopg2$',
        )

    # maybe configure versioning
    if versioning is None:
        versioning = config.versioning_enabled()
    if versioning:
        from rattail.db.config import configure_versioning
        configure_versioning(config)

        # must import all sqlalchemy models before things get rolling,
        # otherwise can have errors about continuum TransactionMeta
        # class not yet mapped, when relevant pages are first requested
        # cf. https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models
        # hat tip to https://stackoverflow.com/a/59241485
        if getattr(config, 'trainwreck_engines', None):
            app = config.get_app()
            trainwreck = app.get_trainwreck_handler()
            try:
                trainwreck_model = trainwreck.get_model()
            except WuttaConfigurationError:
                pass
            else:
                trainwreck_session = trainwreck.make_session()
                trainwreck_session.query(trainwreck_model.Transaction).first()
                trainwreck_session.close()

    # maybe set "future" behavior for SQLAlchemy
    if config.get_bool('rattail.db.sqlalchemy_future_mode', usedb=False):
        from rattail.db import Session
        if Session:
            Session.configure(future=True)

    return config


def get_user_dir(create=False):
    """
    Returns a path to the "preferred" user-level folder, in which additional
    config files (etc.) may be placed as needed.  This essentially returns a
    platform-specific variation of ``~/.rattail/``.

    If ``create`` is ``True``, then the folder will be created if it does not
    already exist.
    """
    if sys.platform == 'win32':

        # Use the Windows Extensions libraries to fetch official defaults.
        try:
            from win32com.shell import shell, shellcon
        except ImportError:
            raise WindowsExtensionsNotInstalled
        else:
            path = os.path.join(shell.SHGetSpecialFolderPath(
                0, shellcon.CSIDL_APPDATA), 'rattail')

    else:
        path = os.path.expanduser('~/.rattail')

    if create and not os.path.exists(path):
        os.mkdir(path)
    return path


def get_user_file(filename, createdir=False):
    """
    Returns a full path to a user-level config file location.  This is obtained
    by first calling :func:`get_user_dir()` and then joining the result with
    ``filename``.

    The ``createdir`` argument will be passed to :func:`get_user_dir()` as its
    ``create`` arg, and may be used to ensure the user-level folder exists.
    """
    return os.path.join(get_user_dir(create=createdir), filename)


class ConfigProfile(object):
    """
    Generic class to represent a config "profile", as used by the filemon and
    datasync daemons, etc.

    .. todo::

       This clearly needs more documentation.

    .. attribute:: config

       Reference to the primary Rattail config object for the running app.

    .. attribute:: key

       String identifier unique to this profile, within the broader
       config section.
    """

    def __init__(self, config, key, **kwargs):
        self.config = config
        self.app = self.config.get_app()
        self.model = self.app.model
        self.enum = self.config.get_enum()
        self.key = key
        self.prefix = kwargs.pop('prefix', key)
        self.load()

    def load(self):
        """
        Read all relevant settings etc. from the config object,
        setting attributes on this profile instance as needed.
        """

    def load_defaults(self):
        """
        Read all "default" (common) settings from config, for the
        current profile.
        """
        self.workdir = self._config_string('workdir')
        self.stop_on_error = self._config_boolean('stop_on_error', False)

    def load_actions(self):
        """
        Read the "actions" from config, for the current profile, and
        assign the result to ``self.actions``.
        """
        self.actions = []
        for action in self._config_list('actions'):
            self.actions.append(self._config_action(action))

    @property
    def section(self):
        """
        Each subclass of ``ConfigProfile`` must define this.
        """
        raise NotImplementedError

    def _config_string(self, option, **kwargs):
        return self.config.get(self.section,
                               '{}.{}'.format(self.prefix, option),
                               **kwargs)

    def _config_boolean(self, option, default=None):
        return self.config.getbool(self.section,
                                   '{}.{}'.format(self.prefix, option),
                                   default=default)

    def _config_int(self, option, minimum=1, default=None):
        """
        Retrieve the *integer* value for the given option.
        """
        option = '{}.{}'.format(self.prefix, option)

        # try to read value from config
        value = self.config.getint(self.section, option)
        if value is not None:

            # found a value; validate it
            if value < minimum:
                log.warning("config value %s is too small; falling back to minimum "
                            "of %s for option: %s", value, minimum, option)
                value = minimum

        # or, use default value, if valid
        elif default is not None and default >= minimum:
            value = default

        # or, just use minimum value
        else:
            value = minimum

        return value

    def _config_list(self, option, default=None, **kwargs):
        value = self._config_string(option, **kwargs)
        if value:
            return self.config.parse_list(value)

        if isinstance(default, list):
            return default

        return []

    def _config_action(self, name):
        """
        Retrieve an "action" value from config, for the current
        profile.  This returns a :class:`ConfigProfileAction`
        instance.
        """
        from rattail.monitoring import CommandAction

        function = self._config_string('action.{}.func'.format(name))
        class_ = self._config_string('action.{}.class'.format(name))
        cmd = self._config_string('action.{}.cmd'.format(name))

        specs = [1 if spec else 0 for spec in (function, class_, cmd)]
        if sum(specs) != 1:
            raise ConfigurationError(
                "Monitor profile '{}' (action '{}') must have exactly one of: "
                "function, class, command".format(self.prefix, name))

        action = ConfigProfileAction()
        action.config = self.config

        if function:
            action.spec = function
            action.action = self.app.load_object(action.spec)
        elif class_:
            action.spec = class_
            action.action = self.app.load_object(action.spec)(self.config)
        elif cmd:
            action.spec = cmd
            action.action = CommandAction(self.config, cmd)

        action.args = self._config_list('action.{}.args'.format(name))

        action.kwargs = {}
        pattern = re.compile(r'^{}\.action\.{}\.kwarg\.(?P<keyword>\w+)$'.format(self.prefix, name), re.IGNORECASE)
        settings = self.config.get_dict(self.section)
        for key in settings:
            match = pattern.match(key)
            if match:
                action.kwargs[match.group('keyword')] = settings[key]

        action.retry_attempts = self._config_int('action.{}.retry_attempts'.format(name), minimum=1)
        action.retry_delay = self._config_int('action.{}.retry_delay'.format(name), minimum=0)
        return action


class ConfigProfileAction(object):
    """
    Simple class to hold configuration for a particular "action"
    defined within a monitor :class:`ConfigProfile`.  Each instance
    has the following attributes:

    .. attribute:: spec

       The original "spec" string used to obtain the action callable.

    .. attribute:: action

       A reference to the action callable.

    .. attribute:: args

       A sequence of positional arguments to be passed to the callable
       (in addition to the file path) when invoking the action.

    .. attribute:: kwargs

       A dictionary of keyword arguments to be passed to the callable
       (in addition to the positional arguments) when invoking the
       action.

    .. attribute:: retry_attempts

       Number of attempts to make when invoking the action.  Defaults
       to ``1``, meaning the first attempt will be made but no retries
       will happen.

    .. attribute:: retry_delay

       Number of seconds to pause between retry attempts, if
       :attr:`retry_attempts` is greater than one.  Defaults to ``0``.
    """
    spec = None
    action = None
    args = []
    kwargs = {}
    retry_attempts = 1
    retry_delay = 0


class FreeTDSLoggingFilter(logging.Filter):
    """
    Custom logging filter, to suppress certain "write to server failed"
    messages relating to FreeTDS database connections.  They seem harmless and
    just cause unwanted error emails.
    """

    def __init__(self, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.pattern = re.compile(r'(?:Read from|Write to) the server failed')

    def filter(self, record):
        if (record.name == 'sqlalchemy.pool.QueuePool'
            and record.funcName == '_finalize_fairy'
            and record.levelno == logging.ERROR
            and record.msg == "Exception during reset or similar"
            and record.exc_info
            and self.pattern.search(str(record.exc_info[1]))):

            # Log this as a warning instead of error, to cut down on our noise.
            record.levelno = logging.WARNING
            record.levelname = 'WARNING'

        return True
