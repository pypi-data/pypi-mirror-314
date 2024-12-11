# -*- coding: utf-8; -*-

import datetime
import warnings
from collections import OrderedDict
from unittest import TestCase

import pytest

from rattail.trainwreck import handler as mod
from rattail.config import make_config


class TestTrainwreckHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config(files=[])

    def make_handler(self):
        return mod.TrainwreckHandler(self.config)

    def test_get_trainwreck_engines(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # first let's configure 3 engines, 1 of which is hidden
        self.config.trainwreck_engines = OrderedDict([
            ('default', sa.create_engine('sqlite://')),
            ('2022', sa.create_engine('sqlite://')),
            ('2021', sa.create_engine('sqlite://')),
        ])
        self.config.setdefault('trainwreck.db', 'hide', '2022')

        # all 3 are returned by default
        engines = self.handler.get_trainwreck_engines()
        self.assertEqual(len(engines), 3)

        # but only 2 if we omit hidden
        engines = self.handler.get_trainwreck_engines(include_hidden=False)
        self.assertEqual(len(engines), 2)
        self.assertIn('default', engines)
        self.assertIn('2021', engines)
        self.assertNotIn('2022', engines)

    def test_get_hidden_engine_keys(self):
        
        # empty list returned by default
        result = self.handler.get_hidden_engine_keys()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # try the "legacy" setting first, to make testing simpler
        self.config.setdefault('tailbone', 'engines.trainwreck.hidden',
                               '2020, 2019, 2018')
        with warnings.catch_warnings(record=True):
            hidden = self.handler.get_hidden_engine_keys()
        self.assertEqual(hidden, ['2020', '2019', '2018'])

        # now try the "proper" setting
        self.config.setdefault('trainwreck.db', 'hide',
                               '2023, 2022, 2021')
        hidden = self.handler.get_hidden_engine_keys()
        self.assertEqual(hidden, ['2023', '2022', '2021'])

    def test_engine_is_hidden(self):
        
        # all engines are *not* hidden by default
        self.assertFalse(self.handler.engine_is_hidden('foobar'))

        # but any we explicitly hide should be reflected in call
        self.config.setdefault('trainwreck.db', 'hide',
                               '2023, 2022, 2021')
        self.assertTrue(self.handler.engine_is_hidden('2023'))
        self.assertTrue(self.handler.engine_is_hidden('2021'))
        self.assertFalse(self.handler.engine_is_hidden('2020'))
        
    def test_get_oldest_transaction_date(self):
        try:
            import sqlalchemy as sa
            from rattail.trainwreck.db import Session as TrainwreckSession
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        self.config.setdefault('rattail', 'timezone.default',
                               'America/Chicago')
        self.config.setdefault('rattail.trainwreck', 'model',
                               'rattail.trainwreck.db.model.defaults')
        trainwreck = self.config.get_trainwreck_model()
        trainwreck.Base.metadata.create_all(bind=engine)
        session = TrainwreckSession(bind=engine)

        # empty db means oldest date is null
        result = self.handler.get_oldest_transaction_date(session)
        self.assertIsNone(result)

        # but if we insert a transaction, that date should be oldest
        dt = datetime.datetime(2022, 1, 1, 8)
        dt = self.handler.app.localtime(dt)
        txn = trainwreck.Transaction(end_time=dt)
        session.add(txn)
        result = self.handler.get_oldest_transaction_date(session)
        self.assertEqual(result, datetime.date(2022, 1, 1))

        # unless of course we add an older one..
        dt = datetime.datetime(2019, 6, 3, 12)
        dt = self.handler.app.localtime(dt)
        txn = trainwreck.Transaction(end_time=dt)
        session.add(txn)
        result = self.handler.get_oldest_transaction_date(session)
        self.assertEqual(result, datetime.date(2019, 6, 3))

    def test_get_newest_transaction_date(self):
        try:
            import sqlalchemy as sa
            from rattail.trainwreck.db import Session as TrainwreckSession
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        self.config.setdefault('rattail', 'timezone.default',
                               'America/Chicago')
        self.config.setdefault('rattail.trainwreck', 'model',
                               'rattail.trainwreck.db.model.defaults')
        trainwreck = self.config.get_trainwreck_model()
        trainwreck.Base.metadata.create_all(bind=engine)
        session = TrainwreckSession(bind=engine)

        # empty db means newest date is null
        result = self.handler.get_newest_transaction_date(session)
        self.assertIsNone(result)

        # but if we insert a transaction, that date should be newest
        dt = datetime.datetime(2019, 6, 3, 12)
        dt = self.handler.app.localtime(dt)
        txn = trainwreck.Transaction(end_time=dt)
        session.add(txn)
        result = self.handler.get_newest_transaction_date(session)
        self.assertEqual(result, datetime.date(2019, 6, 3))

        # unless of course we add an newer one..
        dt = datetime.datetime(2022, 1, 1, 8)
        dt = self.handler.app.localtime(dt)
        txn = trainwreck.Transaction(end_time=dt)
        session.add(txn)
        result = self.handler.get_newest_transaction_date(session)
        self.assertEqual(result, datetime.date(2022, 1, 1))
