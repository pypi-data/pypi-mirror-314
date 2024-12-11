# -*- coding: utf-8; -*-

import os
from unittest import TestCase
from unittest.mock import Mock

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.db import model, Session, ConfigExtension
    from rattail.importing import model as import_model
    from .. import RattailTestCase
except ImportError:
    pass
else:

    class TestAdminUser(TestCase):

        def setUp(self):
            self.config = RattailConfig(defaults={
                'rattail.timezone.default': 'America/Chicago',
            })
            engine_url = os.environ.get('RATTAIL_TEST_ENGINE_URL', 'sqlite://')
            self.engine = sa.create_engine(engine_url)
            model.Base.metadata.create_all(bind=self.engine)
            Session.configure(bind=self.engine)
            self.app = self.config.get_app()
            self.session = self.app.make_session()

        def tearDown(self):
            self.session.close()
            model.Base.metadata.drop_all(bind=self.engine)
            Session.configure(bind=None)

        def make_importer(self, **kwargs):
            kwargs.setdefault('config', self.config)
            kwargs.setdefault('session', self.session)
            return import_model.AdminUserImporter(**kwargs)

        def get_admin(self):
            auth = self.app.get_auth_handler()
            return auth.get_role_administrator(self.session)

        def test_supported_fields(self):
            importer = import_model.UserImporter(self.config)
            standard_fields = importer.fields
            importer = self.make_importer()
            extra_fields = set(importer.fields) - set(standard_fields)
            self.assertEqual(len(extra_fields), 1)
            self.assertEqual(list(extra_fields)[0], 'admin')

        def test_normalize_local_object(self):
            importer = self.make_importer()
            importer.setup()

            user = model.User()
            user.username = 'fred'
            self.session.add(user)
            self.session.flush()

            data = importer.normalize_local_object(user)
            self.assertFalse(data['admin'])

            user.roles.append(self.get_admin())
            self.session.flush()
            data = importer.normalize_local_object(user)
            self.assertTrue(data['admin'])

        def test_update_object(self):
            importer = self.make_importer(fields=['uuid', 'admin'])
            data = {'uuid': 'ccb1915419e511e6a3ad3ca9f40bc550'}
            user = model.User(**data)
            admin = self.get_admin()
            self.assertNotIn(admin, user.roles)

            data['admin'] = True
            importer.update_object(user, data)
            self.assertIn(admin, user.roles)

            data['admin'] = False
            importer.update_object(user, data)
            self.assertNotIn(admin, user.roles)
