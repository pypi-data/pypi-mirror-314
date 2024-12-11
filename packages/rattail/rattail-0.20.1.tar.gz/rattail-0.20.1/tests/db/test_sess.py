# -*- coding: utf-8; -*-

from unittest.mock import patch

from rattail import db
from rattail.testing import DataTestCase

try:
    import sqlalchemy as sa
    from rattail.db import sess as mod
except ImportError:
    pass
else:

    class TestSession(DataTestCase):

        def setUp(self):
            self.setup_db()

            model = self.app.model
            self.user = model.User(username='barney')
            self.session.add(self.user)
            self.session.commit()

        def test_init_rattail_config(self):
            mod.Session.configure(rattail_config=None)
            session = mod.Session()
            self.assertIsNone(session.rattail_config)
            session.close()

            config = object()
            session = mod.Session(rattail_config=config)
            self.assertIs(session.rattail_config, config)
            session.close()

        def test_init_record_changes(self):
            if hasattr(mod.Session, 'kw'):
                self.assertIsNone(mod.Session.kw.get('rattail_record_changes'))

            session = mod.Session()
            self.assertFalse(session.rattail_record_changes)
            session.close()

            session = mod.Session(rattail_record_changes=True)
            self.assertTrue(session.rattail_record_changes)
            session.close()

            engine = sa.create_engine('sqlite://')
            engine.rattail_record_changes = True
            session = mod.Session(bind=engine)
            self.assertTrue(session.rattail_record_changes)
            session.close()

        def test_continuum_user_param(self):

            # null by default
            session = mod.Session()
            self.assertIsNone(session.continuum_user)

            # can pass user
            session = mod.Session(continuum_user=self.user)
            self.assertEqual(session.continuum_user.uuid, self.user.uuid)

            # can pass username
            session = mod.Session(continuum_user='barney')
            self.assertEqual(session.continuum_user.uuid, self.user.uuid)

        def test_log_pool_status(self):

            # sanity/coverage check
            self.config.appdb_engine.rattail_log_pool_status = True
            session = mod.Session()

        def test_set_continuum_user(self):
            session = mod.Session()

            # null by default
            self.assertIsNone(session.continuum_user)

            # can pass user
            session.set_continuum_user(self.user)
            self.assertEqual(session.continuum_user.uuid, self.user.uuid)

            # can pass username
            session.set_continuum_user('barney')
            self.assertEqual(session.continuum_user.uuid, self.user.uuid)

            # null if bad username
            session.set_continuum_user('doesnotexist')
            self.assertIsNone(session.continuum_user)

            # still works if session has no config
            # TODO: not sure why session actually has a config here?
            # (guessing it is an artifact of running other tests?)
            self.assertIsNotNone(session.rattail_config)
            with patch.object(session, 'rattail_config', new=None):
                self.assertIsNone(session.rattail_config)
                session.set_continuum_user('barney')
            self.assertEqual(session.continuum_user.uuid, self.user.uuid)
