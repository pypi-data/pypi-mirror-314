# -*- coding: utf-8; -*-

import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from collections import OrderedDict

import pytz

from rattail.importing import handlers, Importer
from rattail.config import make_config
from . import ImporterTester
from .test_importers import MockImporter


class ImportHandlerBattery(ImporterTester):

    def make_config(self):
        config = make_config([], extend=False)
        config.setdefault('rattail', 'timezone.default', 'America/Chicago')
        return config

    def test_init(self):

        # vanilla
        handler = self.handler_class()
        self.assertEqual(handler.importers, {})
        self.assertEqual(handler.get_importers(), {})
        self.assertEqual(handler.get_importer_keys(), [])
        self.assertEqual(handler.get_default_keys(), [])
        self.assertFalse(handler.commit_host_partial)

        # with config
        handler = self.handler_class()
        self.assertIsNone(handler.config)
        config = self.make_config()
        handler = self.handler_class(config=config)
        self.assertIs(handler.config, config)

        # dry run
        handler = self.handler_class()
        self.assertFalse(handler.dry_run)
        handler = self.handler_class(dry_run=True)
        self.assertTrue(handler.dry_run)

        # extra kwarg
        handler = self.handler_class()
        self.assertRaises(AttributeError, getattr, handler, 'foo')
        handler = self.handler_class(foo='bar')
        self.assertEqual(handler.foo, 'bar')

    def test_get_importer(self):
        get_importers = Mock(return_value={'foo': Importer})

        # no importers
        handler = self.make_handler()
        self.assertIsNone(handler.get_importer('foo'))

        # with config
        config = self.make_config()
        with patch.object(self.handler_class, 'get_importers', get_importers):
            handler = self.handler_class(config)
        importer = handler.get_importer('foo')
        self.assertIs(type(importer), Importer)
        self.assertIs(importer.config, config)
        self.assertIs(importer.handler, handler)

        # # batch size
        # with patch.object(self.handler_class, 'get_importers', get_importers):
        #     handler = self.handler_class()
        # importer = handler.get_importer('foo')
        # self.assertEqual(importer.batch_size, 200)
        # with patch.object(self.handler_class, 'get_importers', get_importers):
        #     handler = self.handler_class(batch_size=42)
        # importer = handler.get_importer('foo')
        # self.assertEqual(importer.batch_size, 42)

        # dry run
        with patch.object(self.handler_class, 'get_importers', get_importers):
            handler = self.handler_class(config)
        importer = handler.get_importer('foo')
        self.assertFalse(importer.dry_run)
        with patch.object(self.handler_class, 'get_importers', get_importers):
            handler = self.handler_class(config, dry_run=True)
        importer = handler.get_importer('foo')
        self.assertTrue(handler.dry_run)

        # host title
        with patch.object(self.handler_class, 'get_importers', get_importers):
            handler = self.handler_class(config)
        importer = handler.get_importer('foo')
        self.assertIsNone(importer.host_system_title)
        handler.host_title = "Foo"
        importer = handler.get_importer('foo')
        self.assertEqual(importer.host_system_title, "Foo")

        # extra kwarg
        with patch.object(self.handler_class, 'get_importers', get_importers):
            handler = self.handler_class(config)
        importer = handler.get_importer('foo')
        self.assertRaises(AttributeError, getattr, importer, 'bar')
        importer = handler.get_importer('foo', bar='baz')
        self.assertEqual(importer.bar, 'baz')

    def test_get_importer_kwargs(self):

        # empty by default
        handler = self.make_handler()
        self.assertEqual(handler.get_importer_kwargs('foo'), {})

        # extra kwargs are preserved
        handler = self.make_handler()
        self.assertEqual(handler.get_importer_kwargs('foo', bar='baz'), {'bar': 'baz'})

    def test_begin_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'begin_host_transaction') as begin_host:
            with patch.object(handler, 'begin_local_transaction') as begin_local:
                handler.begin_transaction()
                begin_host.assert_called_once_with()
                begin_local.assert_called_once_with()

    def test_begin_host_transaction(self):
        handler = self.make_handler()
        handler.begin_host_transaction()

    def test_begin_local_transaction(self):
        handler = self.make_handler()
        handler.begin_local_transaction()

    def test_commit_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'commit_host_transaction') as commit_host:
            with patch.object(handler, 'commit_local_transaction') as commit_local:
                handler.commit_transaction()
                commit_host.assert_called_once_with()
                commit_local.assert_called_once_with()

    def test_commit_host_transaction(self):
        handler = self.make_handler()
        handler.commit_host_transaction()

    def test_commit_local_transaction(self):
        handler = self.make_handler()
        handler.commit_local_transaction()

    def test_rollback_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'rollback_host_transaction') as rollback_host:
            with patch.object(handler, 'rollback_local_transaction') as rollback_local:
                handler.rollback_transaction()
                rollback_host.assert_called_once_with()
                rollback_local.assert_called_once_with()

    def test_rollback_host_transaction(self):
        handler = self.make_handler()
        handler.rollback_host_transaction()

    def test_rollback_local_transaction(self):
        handler = self.make_handler()
        handler.rollback_local_transaction()

    def test_import_data(self):
        self.config = self.make_config()
        handler = self.make_handler()
        result = handler.import_data()
        self.assertEqual(result, {})

    def test_import_data_dry_run(self):
        self.config = self.make_config()

        # as init kwarg
        handler = self.make_handler(dry_run=True)
        with patch.object(handler, 'commit_transaction') as commit:
            with patch.object(handler, 'rollback_transaction') as rollback:
                handler.import_data()
                self.assertFalse(commit.called)
                rollback.assert_called_once_with()
        self.assertTrue(handler.dry_run)

        # as import kwarg
        handler = self.make_handler()
        with patch.object(handler, 'commit_transaction') as commit:
            with patch.object(handler, 'rollback_transaction') as rollback:
                handler.import_data(dry_run=True)
                self.assertFalse(commit.called)
                rollback.assert_called_once_with()
        self.assertTrue(handler.dry_run)

    def test_import_data_invalid_model(self):
        handler = self.make_handler()
        importer = Mock()
        importer.import_data.return_value = [], [], []
        FooImporter = Mock(return_value=importer)
        handler.importers = {'Foo': FooImporter}

        handler.import_data('Foo')
        self.assertEqual(FooImporter.call_count, 1)
        importer.import_data.assert_called_once_with()

        FooImporter.reset_mock()
        importer.reset_mock()

        handler.import_data('Missing')
        self.assertFalse(FooImporter.called)
        self.assertFalse(importer.called)

    def test_import_data_with_changes(self):
        handler = self.make_handler()
        importer = Mock()
        FooImporter = Mock(return_value=importer)
        handler.importers = {'Foo': FooImporter}

        importer.import_data.return_value = [], [], []
        with patch.object(handler, 'process_changes') as process:
            handler.import_data('Foo')
            self.assertFalse(process.called)

        importer.import_data.return_value = [1], [2], [3]
        with patch.object(handler, 'process_changes') as process:
            handler.import_data('Foo')
            process.assert_called_once_with({'Foo': ([1], [2], [3])})

    def test_import_data_commit_host_partial(self):
        self.config = self.make_config()
        handler = self.make_handler()
        importer = Mock()
        importer.import_data.side_effect = ValueError
        FooImporter = Mock(return_value=importer)
        handler.importers = {'Foo': FooImporter}

        handler.commit_host_partial = False
        with patch.object(handler, 'commit_host_transaction') as commit:
            self.assertRaises(ValueError, handler.import_data, 'Foo')
            self.assertFalse(commit.called)

        handler.commit_host_partial = True
        with patch.object(handler, 'commit_host_transaction') as commit:
            self.assertRaises(ValueError, handler.import_data, 'Foo')
            commit.assert_called_once_with()


class BulkImportHandlerBattery(ImportHandlerBattery):

    def test_import_data_invalid_model(self):
        self.config = self.make_config()
        handler = self.make_handler()
        importer = Mock()
        importer.import_data.return_value = 0
        FooImporter = Mock(return_value=importer)
        handler.importers = {'Foo': FooImporter}

        handler.import_data('Foo')
        self.assertEqual(FooImporter.call_count, 1)
        importer.import_data.assert_called_once_with()

        FooImporter.reset_mock()
        importer.reset_mock()

        handler.import_data('Missing')
        self.assertFalse(FooImporter.called)
        self.assertFalse(importer.called)

    def test_import_data_with_changes(self):
        self.config = self.make_config()
        handler = self.make_handler()
        importer = Mock()
        FooImporter = Mock(return_value=importer)
        handler.importers = {'Foo': FooImporter}

        importer.import_data.return_value = 0
        with patch.object(handler, 'process_changes') as process:
            handler.import_data('Foo')
            self.assertFalse(process.called)

        importer.import_data.return_value = 3
        with patch.object(handler, 'process_changes') as process:
            handler.import_data('Foo')
            self.assertFalse(process.called)


class TestImportHandler(TestCase, ImportHandlerBattery):
    handler_class = handlers.ImportHandler

    def setUp(self):
        self.config = self.make_config()

    def test_batch_size_kwarg(self):
        with patch.object(handlers.ImportHandler, 'get_importers', Mock(return_value={'Foo': Importer})):

            # handler has no batch size by default
            handler = handlers.ImportHandler(self.config)
            self.assertFalse(hasattr(handler, 'batch_size'))

            # but can override with kwarg
            handler = handlers.ImportHandler(self.config, batch_size=42)
            self.assertEqual(handler.batch_size, 42)

            # importer default is 200
            handler = handlers.ImportHandler(self.config)
            importer = handler.get_importer('Foo')
            self.assertEqual(importer.batch_size, 200)

            # but can override with handler init kwarg
            handler = handlers.ImportHandler(self.config, batch_size=37)
            importer = handler.get_importer('Foo')
            self.assertEqual(importer.batch_size, 37)

            # can also override with get_importer kwarg
            handler = handlers.ImportHandler(self.config)
            importer = handler.get_importer('Foo', batch_size=98)
            self.assertEqual(importer.batch_size, 98)

    # TODO: must mock out AppHandler.send_email() instead
    # @patch('rattail.importing.handlers.send_email')
    # def test_process_changes_sends_email(self, send_email):
    #     handler = handlers.ImportHandler()
    #     handler.import_began = pytz.utc.localize(datetime.datetime.utcnow())
    #     changes = [], [], []

    #     # warnings disabled
    #     handler.warnings = False
    #     handler.process_changes(changes)
    #     self.assertFalse(send_email.called)

    #     # warnings enabled
    #     handler.warnings = True
    #     handler.process_changes(changes)
    #     self.assertEqual(send_email.call_count, 1)

    #     send_email.reset_mock()

    #     # warnings enabled, with command (just for coverage..)
    #     handler.warnings = True
    #     handler.command = Mock(name='import-testing', parent=Mock(name='rattail'))
    #     handler.process_changes(changes)
    #     self.assertEqual(send_email.call_count, 1)


class TestBulkImportHandler(TestCase, BulkImportHandlerBattery):
    handler_class = handlers.BulkImportHandler


######################################################################
# fake import handler, tested mostly for basic coverage
######################################################################

class MockImportHandler(handlers.ImportHandler):

    def get_importers(self):
        return {'Product': MockImporter}

    def import_data(self, *keys, **kwargs):
        result = super(MockImportHandler, self).import_data(*keys, **kwargs)
        self._result = result
        return result


class TestImportHandlerImportData(ImporterTester, TestCase):

    sample_data = OrderedDict([
        ('16oz', {'upc': '00074305001161', 'description': "Apple Cider Vinegar 16oz"}),
        ('32oz', {'upc': '00074305001321', 'description': "Apple Cider Vinegar 32oz"}),
        ('1gal', {'upc': '00074305011283', 'description': "Apple Cider Vinegar 1gal"}),
    ])

    def setUp(self):
        self.config = self.make_config()
        self.handler = MockImportHandler(config=self.config)
        self.importer = MockImporter(config=self.config)
        self.importer.handler = self.handler

    def make_config(self):
        config = make_config([], extend=False)
        config.setdefault('rattail', 'timezone.default', 'America/Chicago')
        return config

    def import_data(self, **kwargs):
        # must modify our importer in-place since we need the handler to return
        # that specific instance, below (because the host/local data context
        # managers reference that instance directly)
        self.importer._setup(**kwargs)
        with patch.object(self.handler, 'get_importer', Mock(return_value=self.importer)):
            result = self.handler.import_data('Product', **kwargs)
        if result:
            self.result = result['Product']
        else:
            self.result = [], [], []

    def test_invalid_importer_key_is_ignored(self):
        handler = handlers.ImportHandler(self.config)
        self.assertNotIn('InvalidKey', handler.importers)
        self.assertEqual(handler.import_data('InvalidKey'), {})

    def test_create(self):
        local = self.copy_data()
        del local['32oz']
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data()
        self.assert_import_created('32oz')
        self.assert_import_updated()
        self.assert_import_deleted()

    def test_update(self):
        local = self.copy_data()
        local['16oz']['description'] = "wrong description"
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data()
        self.assert_import_created()
        self.assert_import_updated('16oz')
        self.assert_import_deleted()

    def test_delete(self):
        local = self.copy_data()
        local['bogus'] = {'upc': '00000000000000', 'description': "Delete Me"}
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(delete=True)
        self.assert_import_created()
        self.assert_import_updated()
        self.assert_import_deleted('bogus')

    def test_duplicate(self):
        host = self.copy_data()
        host['32oz-dupe'] = host['32oz']
        with self.host_data(host):
            with self.local_data(self.sample_data):
                self.import_data()
        self.assert_import_created()
        self.assert_import_updated()
        self.assert_import_deleted()

    def test_max_create(self):
        local = self.copy_data()
        del local['16oz']
        del local['1gal']
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(max_create=1)
        self.assert_import_created('16oz')
        self.assert_import_updated()
        self.assert_import_deleted()

    def test_max_total_create(self):
        local = self.copy_data()
        del local['16oz']
        del local['1gal']
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(max_total=1)
        self.assert_import_created('16oz')
        self.assert_import_updated()
        self.assert_import_deleted()

    def test_max_update(self):
        local = self.copy_data()
        local['16oz']['description'] = "wrong"
        local['1gal']['description'] = "wrong"
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(max_update=1)
        self.assert_import_created()
        self.assert_import_updated('16oz')
        self.assert_import_deleted()

    def test_max_total_update(self):
        local = self.copy_data()
        local['16oz']['description'] = "wrong"
        local['1gal']['description'] = "wrong"
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(max_total=1)
        self.assert_import_created()
        self.assert_import_updated('16oz')
        self.assert_import_deleted()

    def test_max_delete(self):
        local = self.copy_data()
        local['bogus1'] = {'upc': '00000000000001', 'description': "Delete Me"}
        local['bogus2'] = {'upc': '00000000000002', 'description': "Delete Me"}
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(delete=True, max_delete=1)
        self.assert_import_created()
        self.assert_import_updated()
        self.assert_import_deleted('bogus1')

    def test_max_total_delete(self):
        local = self.copy_data()
        local['bogus1'] = {'upc': '00000000000001', 'description': "Delete Me"}
        local['bogus2'] = {'upc': '00000000000002', 'description': "Delete Me"}
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(delete=True, max_total=1)
        self.assert_import_created()
        self.assert_import_updated()
        self.assert_import_deleted('bogus1')

    def test_dry_run(self):
        local = self.copy_data()
        del local['32oz']
        local['16oz']['description'] = "wrong description"
        local['bogus'] = {'upc': '00000000000000', 'description': "Delete Me"}
        with self.host_data(self.sample_data):
            with self.local_data(local):
                self.import_data(delete=True, dry_run=True)
        # TODO: maybe need a way to confirm no changes actually made due to dry
        # run; currently results still reflect "proposed" changes.  this rather
        # bogus test is here just for coverage sake
        self.assert_import_created('32oz')
        self.assert_import_updated('16oz')
        self.assert_import_deleted('bogus')

    # TODO: must mock out AppHandler.send_email() instead
    # def test_warnings_run(self):
    #     local = self.copy_data()
    #     del local['32oz']
    #     local['16oz']['description'] = "wrong description"
    #     local['bogus'] = {'upc': '00000000000000', 'description': "Delete Me"}
    #     with self.host_data(self.sample_data):
    #         with self.local_data(local):
    #             with patch('rattail.importing.handlers.send_email') as send_email:
    #                 self.assertEqual(send_email.call_count, 0)
    #                 self.import_data(delete=True, warnings=True, dry_run=True)
    #                 self.assertEqual(send_email.call_count, 1)
    #     # second time is just for more coverage...
    #     with self.host_data(self.sample_data):
    #         with self.local_data(local):
    #             with patch('rattail.importing.handlers.send_email') as send_email:
    #                 self.handler.command = Mock()
    #                 self.assertEqual(send_email.call_count, 0)
    #                 self.import_data(delete=True, warnings=True)
    #                 self.assertEqual(send_email.call_count, 1)
    #     # TODO: maybe need a way to confirm no changes actually made due to dry
    #     # run; currently results still reflect "proposed" changes.  this rather
    #     # bogus test is here just for coverage sake
    #     self.assert_import_created('32oz')
    #     self.assert_import_updated('16oz')
    #     self.assert_import_deleted('bogus')


try:
    from sqlalchemy import orm
    from .test_postgresql import MockBulkImporter
except ImportError:
    pass
else:

    Session = orm.sessionmaker()


    class MockFromSQLAlchemyHandler(handlers.FromSQLAlchemyHandler):

        def make_host_session(self):
            return Session()


    class MockToSQLAlchemyHandler(handlers.ToSQLAlchemyHandler):

        def make_session(self):
            return Session()


    class TestFromSQLAlchemyHandler(TestCase):

        def test_init(self):
            handler = handlers.FromSQLAlchemyHandler()
            self.assertRaises(NotImplementedError, handler.make_host_session)

        def test_get_importer_kwargs(self):
            session = object()
            handler = handlers.FromSQLAlchemyHandler(host_session=session)
            kwargs = handler.get_importer_kwargs(None)
            self.assertEqual(list(kwargs.keys()), ['host_session'])
            self.assertIs(kwargs['host_session'], session)

        def test_begin_host_transaction(self):
            handler = MockFromSQLAlchemyHandler()
            self.assertIsNone(handler.host_session)
            handler.begin_host_transaction()
            self.assertIsInstance(handler.host_session, orm.Session)
            handler.host_session.close()

        def test_commit_host_transaction(self):
            # TODO: test actual commit for data changes
            session = Session()
            handler = handlers.FromSQLAlchemyHandler(host_session=session)
            self.assertIs(handler.host_session, session)
            handler.commit_host_transaction()
            self.assertIsNone(handler.host_session)

        def test_rollback_host_transaction(self):
            # TODO: test actual rollback for data changes
            session = Session()
            handler = handlers.FromSQLAlchemyHandler(host_session=session)
            self.assertIs(handler.host_session, session)
            handler.rollback_host_transaction()
            self.assertIsNone(handler.host_session)


    class TestToSQLAlchemyHandler(TestCase):

        def test_init(self):
            handler = handlers.ToSQLAlchemyHandler()
            self.assertRaises(NotImplementedError, handler.make_session)

        def test_get_importer_kwargs(self):
            session = object()
            handler = handlers.ToSQLAlchemyHandler(session=session)
            kwargs = handler.get_importer_kwargs(None)
            self.assertEqual(list(kwargs.keys()), ['session'])
            self.assertIs(kwargs['session'], session)

        def test_begin_local_transaction(self):
            handler = MockToSQLAlchemyHandler()
            self.assertIsNone(handler.session)
            handler.begin_local_transaction()
            self.assertIsInstance(handler.session, orm.Session)
            handler.session.close()

        def test_commit_local_transaction(self):
            # TODO: test actual commit for data changes
            session = Session()
            handler = handlers.ToSQLAlchemyHandler(session=session)
            self.assertIs(handler.session, session)
            with patch.object(handler, 'session') as session:
                handler.commit_local_transaction()
                session.commit.assert_called_once_with()
                self.assertFalse(session.rollback.called)
            # self.assertIsNone(handler.session)

        def test_rollback_local_transaction(self):
            # TODO: test actual rollback for data changes
            session = Session()
            handler = handlers.ToSQLAlchemyHandler(session=session)
            self.assertIs(handler.session, session)
            with patch.object(handler, 'session') as session:
                handler.rollback_local_transaction()
                session.rollback.assert_called_once_with()
                self.assertFalse(session.commit.called)
            # self.assertIsNone(handler.session)
