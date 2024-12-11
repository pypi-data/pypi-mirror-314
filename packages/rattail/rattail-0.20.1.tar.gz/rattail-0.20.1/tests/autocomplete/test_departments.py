# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.autocomplete import departments as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestDepartmentAutocompleter(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.autocompleter = self.make_autocompleter()

        def make_autocompleter(self):
            return mod.DepartmentAutocompleter(self.config)

        def test_autocomplete(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # first create a few departments
            grocery = model.Department(name='Grocery')
            session.add(grocery)
            wellness = model.Department(name='Wellness')
            session.add(wellness)
            bulk = model.Department(name='Bulk')
            session.add(bulk)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'l' yields Wellness, Bulk
            result = self.autocompleter.autocomplete(session, 'l')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(wellness.uuid, uuids)
            self.assertIn(bulk.uuid, uuids)

            # search for 'grocery' yields just that department
            result = self.autocompleter.autocomplete(session, 'grocery')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['value'], grocery.uuid)
