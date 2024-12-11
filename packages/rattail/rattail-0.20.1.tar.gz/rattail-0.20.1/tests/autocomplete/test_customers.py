# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.autocomplete import customers as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestCustomerAutocompleter(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.autocompleter = self.make_autocompleter()

        def make_autocompleter(self):
            return mod.CustomerAutocompleter(self.config)

        def test_autocomplete(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)
            enum = self.config.get_enum()

            # first create some customers
            alice = model.Customer(name='Alice Chalmers')
            session.add(alice)
            bob = model.Customer(name='Bob Loblaw')
            session.add(bob)
            charlie = model.Customer(name='Charlie Chaplin')
            session.add(charlie)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'l' yields all 3 customers
            result = self.autocompleter.autocomplete(session, 'l')
            self.assertEqual(len(result), 3)

            # search for 'cha' yields just 2 customers
            result = self.autocompleter.autocomplete(session, 'cha')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(alice.uuid, uuids)
            self.assertIn(charlie.uuid, uuids)
