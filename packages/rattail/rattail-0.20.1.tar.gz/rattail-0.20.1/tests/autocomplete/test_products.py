# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.autocomplete import products as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class AutocompleterTestCase(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.autocompleter = self.make_autocompleter()

            self.engine = sa.create_engine('sqlite://')
            self.model = self.app.model
            self.model.Base.metadata.create_all(bind=self.engine)
            self.session = Session(bind=self.engine)

        def tearDown(self):
            self.session.rollback()
            self.session.close()


    class TestProductAutocompleter(AutocompleterTestCase):

        def make_autocompleter(self):
            return mod.ProductAutocompleter(self.config)

        def test_autocomplete(self):
            session = self.session
            model = self.model

            # first create a few products
            vinegar = model.Product(description='Apple Cider Vinegar')
            session.add(vinegar)
            dressing = model.Product(description='Apple Cider Dressing')
            session.add(dressing)
            oats = model.Product(description='Bulk Oats')
            session.add(oats)
            deleted = model.Product(description='More Oats', deleted=True)
            session.add(deleted)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'apple' yields Vinegar, Dressing
            result = self.autocompleter.autocomplete(session, 'apple')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(vinegar.uuid, uuids)
            self.assertIn(dressing.uuid, uuids)

            # search for 'oats' yields just the undeleted product
            result = self.autocompleter.autocomplete(session, 'oats')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['value'], oats.uuid)


    class TestProductAllAutocompleter(AutocompleterTestCase):

        def make_autocompleter(self):
            return mod.ProductAllAutocompleter(self.config)

        def test_autocomplete(self):
            session = self.session
            model = self.model

            # first create a few products
            vinegar = model.Product(description='Apple Cider Vinegar')
            session.add(vinegar)
            dressing = model.Product(description='Apple Cider Dressing')
            session.add(dressing)
            oats = model.Product(description='Bulk Oats')
            session.add(oats)
            deleted = model.Product(description='More Oats', deleted=True)
            session.add(deleted)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'apple' yields Vinegar, Dressing
            result = self.autocompleter.autocomplete(session, 'apple')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(vinegar.uuid, uuids)
            self.assertIn(dressing.uuid, uuids)

            # search for 'oats' yields Bulk, More
            result = self.autocompleter.autocomplete(session, 'oats')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(oats.uuid, uuids)
            self.assertIn(deleted.uuid, uuids)


    class TestProductNewOrderAutocompleter(AutocompleterTestCase):

        def make_autocompleter(self):
            return mod.ProductNewOrderAutocompleter(self.config)

        def test_autocomplete(self):
            session = self.session
            model = self.model

            # first create a few products
            vinegar = model.Product(description='Apple Cider Vinegar',
                                    upc='074305001321')
            session.add(vinegar)
            dressing = model.Product(description='Apple Cider Dressing')
            session.add(dressing)
            oats = model.Product(description='Bulk Oats')
            session.add(oats)
            deleted = model.Product(description='More Oats', deleted=True)
            session.add(deleted)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'apple' yields Vinegar, Dressing
            result = self.autocompleter.autocomplete(session, 'apple')
            self.assertEqual(len(result), 2)
            uuids = [info['value'] for info in result]
            self.assertIn(vinegar.uuid, uuids)
            self.assertIn(dressing.uuid, uuids)

            # search for unknown upc yields no results
            result = self.autocompleter.autocomplete(session, '7430500116')
            self.assertEqual(len(result), 0)

            # search for known upc yields just that product
            result = self.autocompleter.autocomplete(session, '7430500132')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['value'], vinegar.uuid)
