# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail import auth as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestAuthHandler(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.handler = self.make_handler()

        def make_handler(self):
            return mod.AuthHandler(self.config)

        def test_delete_user(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # make a user, then delete - it should work
            user = model.User(username='foobar')
            session.add(user)
            session.commit()
            self.assertIn(user, session)
            self.handler.delete_user(user)
            session.commit()
            self.assertNotIn(user, session)

        def test_user_is_admin(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # no user
            self.assertFalse(self.handler.user_is_admin(None))

            # real user but not an admin
            user = model.User(username='barney')
            session.add(user)
            session.commit()
            self.assertFalse(self.handler.user_is_admin(user))

            # but if they are admin, it shows
            admin = self.handler.get_role_administrator(session)
            user.roles.append(admin)
            session.commit()
            self.assertTrue(self.handler.user_is_admin(user))

            session.close()
