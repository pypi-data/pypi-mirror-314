# -*- coding: utf-8; -*-

import configparser
import datetime
import os
import sys
import tempfile
from unittest import TestCase
from unittest.mock import patch

import pytest

from wuttjamaican.testing import FileConfigTestCase
from wuttjamaican.exc import ConfigurationError

from rattail import config as mod, db
from rattail.app import AppHandler


class TestRattailConfig(FileConfigTestCase):

    def make_config(self, **kwargs):
        return mod.RattailConfig(**kwargs)

    def test_constructor(self):

        # no db by default
        config = self.make_config()
        if db.Session:
            session = db.Session()
            self.assertIsNone(session.bind)
            # nb. session also has our config now
            self.assertIs(session.rattail_config, config)
        else:
            # no sqlalchemy, so no rattail engines
            self.assertFalse(hasattr(config, 'appdb_engines'))
            self.assertFalse(hasattr(config, 'appdb_engine'))

        # default db
        config = self.make_config(defaults={
            'rattail.db.default.url': 'sqlite://',
        })
        if db.Session:
            session = db.Session()
            self.assertEqual(str(session.bind.url), 'sqlite://')

    def test_prioritized_files(self):
        first = self.write_file('first.conf', """\
[foo]
bar = 1
""")

        second = self.write_file('second.conf', """\
[rattail.config]
require = %(here)s/first.conf
""")

        myconfig = self.make_config(files=[second])
        files = myconfig.prioritized_files
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], second)
        self.assertEqual(files[1], first)

    def test_get_engine_maker(self):
        try:
            from rattail.db.config import make_engine_from_config
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # default func
        myconfig = self.make_config()
        self.assertEqual(myconfig.default_engine_maker_spec, 'rattail.db.config:make_engine_from_config')
        make_engine = myconfig.get_engine_maker()
        self.assertIs(make_engine, make_engine_from_config)

    def test_setdefault(self):
        myconfig = self.make_config()

        # nb. the tests below are effectively testing the custom get()
        # method in addition to setdefault()

        # value is empty by default
        self.assertIsNone(myconfig.get('foo.bar'))
        self.assertIsNone(myconfig.get('foo', 'bar'))

        # but we can change that by setting default
        myconfig.setdefault('foo.bar', 'baz')
        self.assertEqual(myconfig.get('foo.bar'), 'baz')
        self.assertEqual(myconfig.get('foo', 'bar'), 'baz')

        # also can set a default via section, option (as well as key)
        self.assertIsNone(myconfig.get('foo.blarg'))
        myconfig.setdefault('foo' ,'blarg', 'blast')
        self.assertEqual(myconfig.get('foo.blarg'), 'blast')
        self.assertEqual(myconfig.get('foo', 'blarg'), 'blast')

        # error is raised if args are ambiguous
        self.assertRaises(ValueError, myconfig.setdefault, 'foo', 'bar', 'blarg', 'blast')

        # try that for get() too
        self.assertRaises(ValueError, myconfig.get, 'foo', 'bar', 'blarg', 'blast')

    def test_get(self):
        myconfig = self.make_config()
        myconfig.setdefault('foo.bar', 'baz')

        # can pass section + option
        self.assertEqual(myconfig.get('foo', 'bar'), 'baz')

        # or can pass just a key
        self.assertEqual(myconfig.get('foo.bar'), 'baz')

        # so 1 or 2 args required, otherwise error
        self.assertRaises(ValueError, myconfig.get, 'foo', 'bar', 'baz')
        self.assertRaises(ValueError, myconfig.get)

    def test_getbool(self):
        myconfig = self.make_config()
        self.assertFalse(myconfig.getbool('foo.bar'))
        myconfig.setdefault('foo.bar', 'true')
        self.assertTrue(myconfig.getbool('foo.bar'))

    def test_get_date(self):
        myconfig = self.make_config()
        self.assertIsNone(myconfig.get_date('foo.date'))
        myconfig.setdefault('foo.date', '2023-11-20')
        value = myconfig.get_date('foo.date')
        self.assertIsInstance(value, datetime.date)
        self.assertEqual(value, datetime.date(2023, 11, 20))

    def test_getdate(self):
        myconfig = self.make_config()
        self.assertIsNone(myconfig.getdate('foo.date'))
        myconfig.setdefault('foo.date', '2023-11-20')
        value = myconfig.getdate('foo.date')
        self.assertIsInstance(value, datetime.date)
        self.assertEqual(value, datetime.date(2023, 11, 20))

    def test_getint(self):
        myconfig = self.make_config()
        self.assertIsNone(myconfig.getint('foo.bar'))
        myconfig.setdefault('foo.bar', '42')
        self.assertEqual(myconfig.getint('foo.bar'), 42)

    def test_getlist(self):
        myconfig = self.make_config()
        self.assertIsNone(myconfig.getlist('foo.bar'))
        myconfig.setdefault('foo.bar', 'hello world')
        self.assertEqual(myconfig.getlist('foo.bar'), ['hello', 'world'])

    def test_parse_bool(self):
        myconfig = self.make_config()
        self.assertTrue(myconfig.parse_bool('true'))
        self.assertFalse(myconfig.parse_bool('false'))

    def test_parse_list(self):
        myconfig = self.make_config()
        self.assertEqual(myconfig.parse_list(None), [])
        self.assertEqual(myconfig.parse_list('hello world'), ['hello', 'world'])

    def test_make_list_string(self):
        myconfig = self.make_config()

        value = myconfig.make_list_string(['foo', 'bar'])
        self.assertEqual(value, 'foo, bar')

        value = myconfig.make_list_string(['hello world', 'how are you'])
        self.assertEqual(value, "'hello world', 'how are you'")

        value = myconfig.make_list_string(["you don't", 'say'])
        self.assertEqual(value, "\"you don't\", say")

    def test_get_app(self):
        myconfig = self.make_config()
        app = myconfig.get_app()
        self.assertIsInstance(app, AppHandler)
        self.assertIs(type(app), AppHandler)

    def test_beaker_invalidate_setting(self):
        # TODO: this doesn't really test anything, just gives coverage
        myconfig = self.make_config()
        myconfig.beaker_invalidate_setting('foo')

    def test_node_type(self):
        myconfig = self.make_config()

        # error if node type not defined
        self.assertRaises(ConfigurationError, myconfig.node_type)

        # unless default is provided
        self.assertEqual(myconfig.node_type(default='foo'), 'foo')

        # or config contains the definition
        myconfig.setdefault('rattail.node_type', 'bar')
        self.assertEqual(myconfig.node_type(), 'bar')

    def test_get_model(self):
        try:
            import sqlalchemy
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # default is rattail.db.model
        myconfig = self.make_config()
        model = myconfig.get_model()
        self.assertIs(model, sys.modules['rattail.db.model'])

        # or config may specify
        myconfig = self.make_config()
        myconfig.setdefault('rattail.model', 'rattail.trainwreck.db.model')
        model = myconfig.get_model()
        self.assertIs(model, sys.modules['rattail.trainwreck.db.model'])

    def test_get_enum(self):
        myconfig = self.make_config()

        # default is rattail.enum
        enum = myconfig.get_enum()
        self.assertIs(enum, sys.modules['rattail.enum'])

        # or config may specify
        # (nb. using bogus example module here)
        myconfig.setdefault('rattail.enum', 'rattail.util')
        enum = myconfig.get_enum()
        self.assertIs(enum, sys.modules['rattail.util'])

    def test_get_trainwreck_model(self):
        try:
            import sqlalchemy
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        myconfig = self.make_config()

        # error if not defined
        self.assertRaises(ConfigurationError, myconfig.get_trainwreck_model)

        # but config may specify
        myconfig.setdefault('rattail.trainwreck.model', 'rattail.trainwreck.db.model')
        model = myconfig.get_trainwreck_model()
        self.assertIs(model, sys.modules['rattail.trainwreck.db.model'])

    def test_versioning_enabled(self):
        myconfig = self.make_config()

        # false by default
        self.assertFalse(myconfig.versioning_enabled())

        # but config may enable
        myconfig.setdefault('rattail.db.versioning.enabled', 'true')
        self.assertTrue(myconfig.versioning_enabled())

    def test_app_package(self):
        myconfig = self.make_config()

        # error if not defined
        self.assertRaises(ConfigurationError, myconfig.app_package)

        # unless default is provided
        self.assertEqual(myconfig.app_package(default='foo'), 'foo')

        # but config may specify
        myconfig.setdefault('rattail.app_package', 'bar')
        self.assertEqual(myconfig.app_package(), 'bar')

    def test_app_title(self):
        myconfig = self.make_config()

        # default title
        self.assertEqual(myconfig.app_title(), 'Rattail')

        # but config may specify
        myconfig.setdefault('rattail.app_title', 'Foo')
        self.assertEqual(myconfig.app_title(), 'Foo')

    def test_node_title(self):
        myconfig = self.make_config()

        # default title
        self.assertEqual(myconfig.app_title(), 'Rattail')

        # but config may specify
        myconfig.setdefault('rattail.node_title', 'Foo (node)')
        self.assertEqual(myconfig.node_title(), 'Foo (node)')

    def test_running_from_source(self):
        myconfig = self.make_config()

        # false by default
        self.assertFalse(myconfig.running_from_source())

        # but config may enable
        myconfig.setdefault('rattail.running_from_source', 'true')
        self.assertTrue(myconfig.running_from_source())

    def test_demo(self):
        myconfig = self.make_config()

        # false by default
        self.assertFalse(myconfig.demo())

        # but config may enable
        myconfig.setdefault('rattail.demo', 'true')
        self.assertTrue(myconfig.demo())

    def test_appdir(self):
        myconfig = self.make_config()

        # can be none if required is false
        self.assertIsNone(myconfig.appdir(require=False))

        # otherwise sane fallback is used
        with patch('rattail.config.sys') as sys:
            sys.prefix = 'foo'
            path = os.path.join('foo', 'app')
            self.assertEqual(myconfig.appdir(), path)

        # or config may specify
        myconfig.setdefault('rattail.appdir', '/foo/bar/baz')
        self.assertEqual(myconfig.appdir(), '/foo/bar/baz')

    def test_datadir(self):
        myconfig = self.make_config()

        # error if not defined
        self.assertRaises(ConfigurationError, myconfig.datadir)

        # but can avoid error if not required
        self.assertIsNone(myconfig.datadir(require=False))

        # or config may specify
        myconfig.setdefault('rattail.datadir', '/foo/bar/baz')
        self.assertEqual(myconfig.datadir(), '/foo/bar/baz')

    def test_workdir(self):
        myconfig = self.make_config()

        # error if not defined
        self.assertRaises(ConfigurationError, myconfig.workdir)

        # but can avoid error if not required
        self.assertIsNone(myconfig.workdir(require=False))

        # or config may specify
        myconfig.setdefault('rattail.workdir', '/foo/bar/baz')
        self.assertEqual(myconfig.workdir(), '/foo/bar/baz')

    def test_batch_filedir(self):
        myconfig = self.make_config()

        # error if not defined
        self.assertRaises(ConfigurationError, myconfig.batch_filedir)

        # config may specify
        path = os.path.join(os.sep, 'foo', 'files')
        myconfig.setdefault('rattail.batch.files', path)
        self.assertEqual(myconfig.batch_filedir(), path)

        # caller may specify a key
        self.assertEqual(myconfig.batch_filedir(key='bar'), os.path.join(path, 'bar'))


class TestLegacyConfigExtensionBase(TestCase):

    def test_basic(self):
        # sanity / coverage check
        ext = mod.ConfigExtension()


class TestRattailConfigExtension(TestCase):

    def make_config(self, **kwargs):
        return mod.RattailConfig(**kwargs)

    def make_extension(self):
        return mod.RattailConfigExtension()

    def test_configure(self):

        # no import config yet
        config = self.make_config()
        self.assertEqual(config.defaults, {})
        self.assertIsNone(config.get('rattail.importing.to_rattail.from_csv.import.default_handler'))

        # extension adds import config
        ext = self.make_extension()
        ext.configure(config)
        spec = config.get('rattail.importing.to_rattail.from_csv.import.default_handler')
        self.assertIsNotNone(spec)

        # poser dir added to path
        self.assertNotIn('/tmp/foo', sys.path)
        tempdir = tempfile.mkdtemp()
        config.setdefault('rattail.poser', tempdir)
        ext.configure(config)
        self.assertIn(tempdir, sys.path)
        sys.path.remove(tempdir)
        os.rmdir(tempdir)


class TestRattailDefaultFiles(FileConfigTestCase):

    def test_quiet_conf(self):
        generic = self.write_file('generic.conf', '')
        quiet = self.write_file('quiet.conf', '')

        with patch('rattail.config.generic_default_files') as generic_default_files:
            generic_default_files.return_value = [generic]

            with patch('rattail.config.os') as mockos:
                mockos.path.join.return_value = quiet

                # generic files by default
                mockos.path.exists.return_value = False
                files = mod.rattail_default_files('rattail')
                generic_default_files.assert_called_once_with('rattail')
                self.assertEqual(files, [generic])

                # but if quiet.conf exists, will return that
                generic_default_files.reset_mock()
                mockos.path.exists.return_value = True
                files = mod.rattail_default_files('rattail')
                generic_default_files.assert_not_called()
                self.assertEqual(files, [quiet])


class TestMakeConfig(FileConfigTestCase):

    def test_files(self):
        generic = self.write_file('generic.conf', '')
        myfile = self.write_file('my.conf', '')

        # generic files by default
        myconfig = mod.make_config(default_files=[generic])
        self.assertEqual(myconfig.files_read, [generic])

        # can specify single primary file
        myconfig = mod.make_config(myfile, default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])

        # can specify primary files as list
        myconfig = mod.make_config([myfile], default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])

        # can specify primary files via env
        myconfig = mod.make_config(env={'RATTAIL_CONFIG_FILES': myfile},
                                   default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])
