# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock

from rattail.db import util


class TestFunctions(TestCase):

    def test_normalize_full_name(self):
        name = util.normalize_full_name(None, None)
        self.assertEqual(name, "")

        name = util.normalize_full_name("Fred", None)
        self.assertEqual(name, "Fred")

        name = util.normalize_full_name(None, "Flintstone")
        self.assertEqual(name, "Flintstone")

        name = util.normalize_full_name("Fred", "Flintstone")
        self.assertEqual(name, "Fred Flintstone")

        name = util.normalize_full_name("  Fred  ", "  Flintstone  ")
        self.assertEqual(name, "Fred Flintstone")

    def test_normalize_phone_number(self):
        number = util.normalize_phone_number(None)
        self.assertIsNone(number)

        number = util.normalize_phone_number('417-555-1234')
        self.assertEqual(number, '4175551234')

        number = util.normalize_phone_number('  (417) 555-1234  ')
        self.assertEqual(number, '4175551234')

    def test_format_phone_number(self):
        number = util.format_phone_number(None)
        self.assertIsNone(number)

        number = util.format_phone_number('417-555-1234')
        self.assertEqual(number, '(417) 555-1234')

        number = util.format_phone_number('  (417) 555-1234  ')
        self.assertEqual(number, '(417) 555-1234')


try:
    from sqlalchemy import orm
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestShortSession(TestCase):

        def test_none(self):
            with util.short_session() as s:
                self.assertIsInstance(s, Session.class_)

        def test_factory(self):
            TestSession = orm.sessionmaker()
            with util.short_session(factory=TestSession) as s:
                self.assertIsInstance(s, TestSession.class_)

        def test_Session(self):
            TestSession = orm.sessionmaker()
            with util.short_session(Session=TestSession) as s:
                self.assertIsInstance(s, TestSession.class_)

        def test_instance(self):
            # nb. nothing really happens if we provide the session instance
            session = MagicMock()
            with util.short_session(session=session) as s:
                pass
            session.commit.assert_not_called()
            session.close.assert_not_called()

        def test_config(self):
            config = MagicMock()
            TestSession = orm.sessionmaker()
            config.get_app.return_value.make_session = TestSession
            with util.short_session(config=config) as s:
                self.assertIsInstance(s, TestSession.class_)

        def test_without_commit(self):
            session = MagicMock()
            TestSession = MagicMock(return_value=session)
            with util.short_session(factory=TestSession, commit=False) as s:
                pass
            session.commit.assert_not_called()
            session.close.assert_called_once_with()

        def test_with_commit(self):
            session = MagicMock()
            TestSession = MagicMock(return_value=session)
            with util.short_session(factory=TestSession, commit=True) as s:
                pass
            session.commit.assert_called_once_with()
            session.close.assert_called_once_with()
