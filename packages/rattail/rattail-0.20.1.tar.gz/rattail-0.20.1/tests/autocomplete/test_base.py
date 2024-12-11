# -*- coding: utf-8; -*-

from unittest import TestCase

import pytest

from rattail.config import RattailConfig
from rattail.autocomplete import base as mod
from rattail.db import Session


class TestAutocompleter(TestCase):

    def setUp(self):
        self.config = RattailConfig()
        self.app = self.config.get_app()

    def test_constructor(self):

        # cannot instantiate autocompleter with no key
        class BadAutocompleter(mod.Autocompleter):
            pass
        self.assertRaises(NotImplementedError, BadAutocompleter, self.config)

        # but works okay if key is defined
        class GoodAutocompleter(mod.Autocompleter):
            autocompleter_key = 'stores'
        autocompleter = GoodAutocompleter(self.config)
        self.assertIsNotNone(autocompleter)

    def test_get_model_class(self):
        try:
            model = self.app.model
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # no model class by default; hence error
        class BadAutocompleter(mod.Autocompleter):
            autocompleter_key = 'stores'
        autocompleter = BadAutocompleter(self.config)
        self.assertRaises(AttributeError, autocompleter.get_model_class)

        # but if one is set, it is returned
        class GoodAutocompleter(mod.Autocompleter):
            autocompleter_key = 'stores'
            model_class = model.Store
        autocompleter = GoodAutocompleter(self.config)
        result = autocompleter.get_model_class()
        self.assertIs(result, model.Store)

    def test_autocomplete_fieldname(self):

        # no fieldname by default; hence error
        class BadAutocompleter(mod.Autocompleter):
            autocompleter_key = 'stores'
        autocompleter = BadAutocompleter(self.config)
        self.assertRaises(NotImplementedError, getattr,
                          autocompleter, 'autocomplete_fieldname')

        # but works okay if class defines it
        class GoodAutocompleter(mod.Autocompleter):
            autocompleter_key = 'stores'
            autocomplete_fieldname = 'name'
        autocompleter = GoodAutocompleter(self.config)
        self.assertEqual(autocompleter.autocomplete_fieldname, 'name')

    def test_autocomplete(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        class StoreAutocompleter(mod.Autocompleter):
            autocompleter_key = 'store'
            model_class = model.Store
            autocomplete_fieldname = 'name'

        # first create a few stores
        store001 = model.Store(id='001', name="Acme Store #1")
        session.add(store001)
        store002 = model.Store(id='002', name="Acme Store #2")
        session.add(store002)
        store999 = model.Store(id='999', name="Warehouse")
        session.add(store999)

        # and our autocompleter
        autocompleter = StoreAutocompleter(self.config)

        # searching for nothing yields no results
        result = autocompleter.autocomplete(session, '')
        self.assertEqual(len(result), 0)

        # search for 'acme' yields stores 1, 2
        result = autocompleter.autocomplete(session, 'acme')
        self.assertEqual(len(result), 2)
        uuids = [info['value'] for info in result]
        self.assertIn(store001.uuid, uuids)
        self.assertIn(store002.uuid, uuids)

        # search for 'warehouse' yields store 999
        result = autocompleter.autocomplete(session, 'warehouse')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], store999.uuid)

        # search for 'bogus' yields no results
        result = autocompleter.autocomplete(session, 'bogus')
        self.assertEqual(len(result), 0)

        # search for 's' yields all 3 stores
        result = autocompleter.autocomplete(session, 's')
        self.assertEqual(len(result), 3)

        # unless we cap the max results
        autocompleter.max_results = 2
        result = autocompleter.autocomplete(session, 's')
        self.assertEqual(len(result), 2)

        # removing cap should get all 3 again
        autocompleter.max_results = None
        result = autocompleter.autocomplete(session, 's')
        self.assertEqual(len(result), 3)


class TestPhoneMagicMixin(TestCase):

    def setUp(self):
        self.config = RattailConfig()
        self.app = self.config.get_app()

    def test_autocomplete(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        class StoreMagicAutocompleter(mod.PhoneMagicMixin, mod.Autocompleter):
            autocompleter_key = 'store'
            model_class = model.Store
            autocomplete_fieldname = 'name'
            phone_model_class = model.StorePhoneNumber

        # first create a few stores, with phones
        store001 = model.Store(id='001', name="Acme Store #1")
        store001.add_phone_number('417-555-0001')
        session.add(store001)
        store002 = model.Store(id='002', name="Acme Store #2")
        store002.add_phone_number('417-555-0002')
        session.add(store002)
        store999 = model.Store(id='999', name="Warehouse")
        session.add(store999)

        # and our autocompleter
        autocompleter = StoreMagicAutocompleter(self.config)

        # searching for nothing yields no results
        result = autocompleter.autocomplete(session, '')
        self.assertEqual(len(result), 0)

        # search for 'acme' yields stores 1, 2
        result = autocompleter.autocomplete(session, 'acme')
        self.assertEqual(len(result), 2)
        uuids = [info['value'] for info in result]
        self.assertIn(store001.uuid, uuids)
        self.assertIn(store002.uuid, uuids)

        # search for 'warehouse' yields store 999
        result = autocompleter.autocomplete(session, 'warehouse')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], store999.uuid)

        # TODO: need to test the actual phone number magic, but sqlite
        # does not have a regexp_replace() function built-in.  so
        # either need to code some workaround, or require the 're'
        # extension be loaded for sqlite, etc.
