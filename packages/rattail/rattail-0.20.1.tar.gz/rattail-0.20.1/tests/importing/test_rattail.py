# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch

try:
    import sqlalchemy as sa
    from rattail.db import model, Session
    from rattail.db.sess import SessionBase
    from rattail.importing import rattail as rattail_importing
    from .. import RattailMixin, RattailTestCase
    from . import ImporterTester
except ImportError:
    pass
else:

    class DualRattailMixin(RattailMixin):

        def setup_rattail(self):
            super().setup_rattail()

            if 'host' not in self.config.appdb_engines:
                self.config.appdb_engines['host'] = sa.create_engine('sqlite://')

            self.host_engine = self.config.appdb_engines['host']
            self.config.setdefault('rattail', 'timezone.default', 'America/Chicago')
            self.config.setdefault('rattail.db', 'keys', 'default, host')
            self.config.setdefault('rattail.db', 'host.url', str(self.host_engine.url))
            model = self.get_rattail_model()
            model.Base.metadata.create_all(bind=self.host_engine)
            self.host_session = Session(bind=self.host_engine)

        def teardown_rattail(self):
            super().teardown_rattail()

            self.host_session.close()
            model = self.get_rattail_model()
            model.Base.metadata.drop_all(bind=self.config.appdb_engines['host'])

            if hasattr(self, 'tempio'):
                self.tempio = None


    class DualRattailTestCase(DualRattailMixin, TestCase):
        pass


    class TestFromRattailHandler(RattailTestCase, ImporterTester):
        handler_class = rattail_importing.FromRattailHandler

        def test_make_host_session(self):
            handler = self.make_handler()
            session = handler.make_host_session()
            self.assertIsInstance(session, SessionBase)
            self.assertIs(session.bind, self.config.appdb_engine)


    class TestFromRattailToRattail(DualRattailTestCase, ImporterTester):
        handler_class = rattail_importing.FromRattailToRattailImport
        # extend_config = False

        # def test_host_title(self):
        #     handler = self.make_handler(dbkey='host')
        #     self.assertEqual(handler.host_title, "Rattail (host)")

        # TODO
        def test_default_keys(self):
            handler = self.make_handler()
            handler.get_default_keys()

        def test_make_session(self):
            handler = self.make_handler()
            session = handler.make_session()
            self.assertIsInstance(session, SessionBase)
            self.assertIs(session.bind, self.config.appdb_engine)

        def test_make_host_session(self):

            # invalid dbkey
            handler = self.make_handler(dbkey='other')
            self.assertRaises(KeyError, handler.make_host_session)

            # alternate dbkey
            self.config.appdb_engines['other'] = self.config.appdb_engines['host']
            handler = self.make_handler(dbkey='other')
            session = handler.make_host_session()
            self.assertIsInstance(session, SessionBase)
            self.assertIs(session.bind, self.host_engine)


    class TestFromRattail(DualRattailTestCase):

        def make_importer(self, model_class=None, **kwargs):
            kwargs.setdefault('host_session', self.host_session)
            importer = rattail_importing.FromRattail(self.config, **kwargs)
            if model_class:
                importer.model_class = model_class
            return importer

        def test_host_model_class(self):
            importer = self.make_importer()
            self.assertIsNone(importer.model_class)
            self.assertIsNone(importer.host_model_class)
            importer = self.make_importer(model.Product)
            self.assertIs(importer.host_model_class, model.Product)

        def test_query(self):
            importer = self.make_importer(model.Product)
            importer.query()

        def test_normalize_host_object(self):
            importer = self.make_importer(model.Product)
            product = model.Product()
            with patch.object(importer, 'normalize_local_object') as normalize_local:
                normalize_local.return_value = {}
                data = importer.normalize_host_object(product)
                self.assertEqual(data, {})
                normalize_local.assert_called_once_with(product)
            self.assertEqual(data, importer.normalize_local_object(product))


    class TestAdminUser(DualRattailTestCase):

        importer_class = rattail_importing.AdminUserImporter

        def make_importer(self, **kwargs):
            kwargs.setdefault('config', self.config)
            kwargs.setdefault('session', self.session)
            return self.importer_class(**kwargs)

        def get_admin(self):
            app = self.config.get_app()
            auth = app.get_auth_handler()
            return auth.get_role_administrator(self.session)

        def test_normalize_host_object(self):
            importer = self.make_importer()
            importer.setup()

            user = model.User()
            user.username = 'fred'
            self.session.add(user)
            self.session.flush()

            data = importer.normalize_host_object(user)
            self.assertFalse(data['admin'])

            user.roles.append(self.get_admin())
            self.session.flush()
            data = importer.normalize_host_object(user)
            self.assertTrue(data['admin'])
