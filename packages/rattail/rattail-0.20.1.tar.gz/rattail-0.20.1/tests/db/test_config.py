# -*- coding: utf-8; -*-

from unittest import TestCase

try:
    from rattail.db import config as conf
except ImportError:
    pass
else:

    class TestMakeEngineFromConfig(TestCase):

        def test_record_changes(self):

            # no attribute is set by default
            engine = conf.make_engine_from_config({
                'sqlalchemy.url': 'sqlite://',
            })
            self.assertRaises(AttributeError, getattr, engine, 'rattail_record_changes')

            # but if flag is true, attr is set
            engine = conf.make_engine_from_config({
                'sqlalchemy.url': 'sqlite://',
                'sqlalchemy.record_changes': 'true'
            })
            self.assertTrue(engine.rattail_record_changes)

        def test_log_pool_status(self):

            # no attribute is set by default
            engine = conf.make_engine_from_config({
                'sqlalchemy.url': 'sqlite://',
            })
            self.assertRaises(AttributeError, getattr, engine, 'rattail_log_pool_status')

            # but if flag is true, attr is set
            engine = conf.make_engine_from_config({
                'sqlalchemy.url': 'sqlite://',
                'sqlalchemy.log_pool_status': 'true'
            })
            self.assertTrue(engine.rattail_log_pool_status)
