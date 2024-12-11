# -*- coding: utf-8; -*-

from unittest import TestCase

import pytest

from rattail.vendors import handler as mod
from rattail.vendors.catalogs import CatalogParserNotFound
from rattail.config import make_config
from rattail.db import Session


class TestVendorHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.app = self.config.get_app()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config([], extend=False)

    def make_handler(self):
        return mod.VendorHandler(self.config)

    def test_choice_uses_dropdown(self):
        
        # do not use dropdown by default
        result = self.handler.choice_uses_dropdown()
        self.assertFalse(result)

        # but do use dropdown if so configured
        self.config.setdefault('rattail', 'vendors.choice_uses_dropdown',
                               'true')
        result = self.handler.choice_uses_dropdown()
        self.assertTrue(result)

    def test_get_vendor(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # no vendor if none exist yet!
        result = self.handler.get_vendor(session, 'acme')
        self.assertIsNone(result)

        # let's make the vendor and make sure uuid fetch works
        uuid = app.make_uuid()
        acme = model.Vendor(uuid=uuid, name="Acme")
        session.add(acme)
        result = self.handler.get_vendor(session, uuid)
        self.assertIs(result, acme)

        # if we search by key it still does not work
        result = self.handler.get_vendor(session, 'acme')
        self.assertIsNone(result)

        # but we can configure the key reference, then it will
        setting = model.Setting(name='rattail.vendor.acme', value=uuid)
        session.add(setting)
        result = self.handler.get_vendor(session, 'acme')
        self.assertIs(result, acme)

    def test_get_all_catalog_parsers(self):

        # some are always installed; make sure they come back
        Parsers = self.handler.get_all_catalog_parsers()
        self.assertTrue(len(Parsers))

    def test_get_supported_catalog_parsers(self):

        # by default all parsers are considered supported, so these
        # calls should effectively yield the same result
        all_parsers = self.handler.get_all_catalog_parsers()
        supported = self.handler.get_supported_catalog_parsers()
        self.assertEqual(len(all_parsers), len(supported))

        # now pretend only one is supported, using legacy setting
        self.config.setdefault('tailbone', 'batch.vendorcatalog.supported_parsers',
                               'rattail.contrib.generic')
        supported = self.handler.get_supported_catalog_parsers()
        self.assertEqual(len(supported), 1)
        Parser = supported[0]
        self.assertEqual(Parser.key, 'rattail.contrib.generic')

        # now pretend two are supported, using preferred setting
        self.config.setdefault('rattail', 'vendors.supported_catalog_parsers',
                               'rattail.contrib.generic, rattail.contrib.kehe')
        supported = self.handler.get_supported_catalog_parsers()
        self.assertEqual(len(supported), 2)
        keys = [Parser.key for Parser in supported]
        self.assertEqual(keys, ['rattail.contrib.generic', 'rattail.contrib.kehe'])

    def test_get_catalog_parser(self):
        
        # generic parser comes back fine
        parser = self.handler.get_catalog_parser('rattail.contrib.generic')
        self.assertIsNotNone(parser)
        self.assertEqual(parser.key, 'rattail.contrib.generic')

        # unknown key returns nothing
        parser = self.handler.get_catalog_parser('this_should_not_exist')
        self.assertIsNone(parser)

        # and can raise an error if we require
        self.assertRaises(CatalogParserNotFound, self.handler.get_catalog_parser,
                          'this_should_not_exist', require=True)
