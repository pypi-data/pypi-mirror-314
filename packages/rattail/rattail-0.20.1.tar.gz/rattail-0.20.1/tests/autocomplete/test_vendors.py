# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.autocomplete import vendors as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestVendorAutocompleter(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.autocompleter = self.make_autocompleter()

        def make_autocompleter(self):
            return mod.VendorAutocompleter(self.config)

        def test_autocomplete(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # first create some vendors
            acme = model.Vendor(name='Acme Wholesale Foods')
            session.add(acme)
            bigboy = model.Vendor(name='Big Boy Distributors')
            session.add(bigboy)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'd' yields both vendors
            result = self.autocompleter.autocomplete(session, 'd')
            self.assertEqual(len(result), 2)

            # search for 'big' yields just Big Boy
            result = self.autocompleter.autocomplete(session, 'big')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['value'], bigboy.uuid)
